# reference: https://github.com/awslabs/amazon-transcribe-streaming-sdk
# document:  https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
# aws transcription supported languages: https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html
"""
default installation requires aws-crt~=0.14 but 0.14 can not be installed
    - install manually by cloning the sdk and change setup.py and setup.cfg 's awscrt requiremente to >= 0.14
    - 0.16 works
"""
import asyncio

# This example uses aiofile for asynchronous file reads.
# It's not a dependency of the project but can be installed
# with `pip install aiofile`.
import aiofile

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from amazon_transcribe.utils import apply_realtime_delay
from .settings import *


class PrerecordedEventHandler(TranscriptResultStreamHandler):
    def __init__(self, output_stream):
        super().__init__(output_stream)
        self.all_results = []
        self.last = "***"

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                if self.last in alt.transcript:
                    self.all_results[-1] = alt.transcript
                else:
                    self.all_results.append(alt.transcript)
                self.last = alt.transcript


async def prerecorded_transcribe(audio_path: str, input_language: str):
    # Setup up our client with our chosen AWS region
    client = TranscribeStreamingClient(region=REGION)

    # Start transcription to generate our async stream
    stream = await client.start_stream_transcription(
        language_code=LANGUAGE_MAPPING[input_language],
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm",
    )

    async def write_chunks():
        # NOTE: For pre-recorded files longer than 5 minutes, the sent audio
        # chunks should be rate limited to match the realtime bitrate of the
        # audio stream to avoid signing issues.
        async with aiofile.AIOFile(audio_path, "rb") as afp:
            reader = aiofile.Reader(afp, chunk_size=CHUNK_SIZE)
            await apply_realtime_delay(
                stream, reader, BYTES_PER_SAMPLE, SAMPLE_RATE, CHANNEL_NUMS
            )
        await stream.input_stream.end_stream()

    # Instantiate our handler and start processing events
    handler = PrerecordedEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())

    s = select_result(handler.all_results)
    print("transcription success...")
    print(s)

    return s
