import asyncio
import pyaudio
import audioop

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from .settings import *


class LiveEventHandler(TranscriptResultStreamHandler):
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


async def live_transcribe(
    input_language: str,
    audio_min_rms=AUDIO_MIN_RMS,
    max_low_audio_flag=MAX_LOW_AUDIO_FLAG,
):
    client = TranscribeStreamingClient(region=REGION)

    stream = await client.start_stream_transcription(
        language_code=LANGUAGE_MAPPING[input_language],
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm",
    )

    async def write_chunks():
        low_audio_flag = 0
        record_stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=CHANNEL_NUMS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )
        print("start detecting audio...")

        while True:
            data = record_stream.read(CHUNK_SIZE)
            rms = audioop.rms(data, 2)

            low_audio_flag = 0 if rms > audio_min_rms else low_audio_flag + 1

            show_realtime_rms(rms, audio_min_rms=audio_min_rms)
            if low_audio_flag > max_low_audio_flag:
                print("\ndetecting finished...")
                break

            # convert the audio frame to byte stream and send it to service.
            await stream.input_stream.send_audio_event(audio_chunk=data)  # tobytes()

        await stream.input_stream.end_stream()

    handler = LiveEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())

    s = select_result(handler.all_results)
    print("transcription success...")
    print(s)

    return s
