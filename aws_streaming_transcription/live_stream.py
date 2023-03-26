import asyncio
import sounddevice as sd
import numpy as np

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

'''
https://python-sounddevice.readthedocs.io/en/0.3.7/
sd.decault.device = #
'''

audio_min_rms = 100
max_low_audio_flag = 20

class MyEventHandler(TranscriptResultStreamHandler):
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
                


async def basic_transcribe():
    client = TranscribeStreamingClient(region="us-east-2")

    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )

    async def write_chunks():
        low_audio_flag = 0
        while True:
           
            data = sd.rec(1024*8, samplerate=16000, channels=1, blocking=True, dtype='int16')

            data[np.isnan(data)]=0
            rms  = np.sqrt(np.mean(np.square(data)))

            # print(low_audio_flag)

            low_audio_flag = 0 if rms > audio_min_rms else low_audio_flag + 1

            # 100 consecutive samples of low audio
            if low_audio_flag > max_low_audio_flag:
                break

            # convert the audio frame to a byte stream and send it to the transcription service.
            await stream.input_stream.send_audio_event(audio_chunk=data.tobytes())
        
        await stream.input_stream.end_stream()
            


    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())

    return handler.all_results


