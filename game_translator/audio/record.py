"""
reference: https://github.com/dylanz666/pyaudio-learning
"""
import audioop
import wave
import pyaudio
import sys


class Detector:
    """
    A class representing a audio recorder.

    Attributes:
    """

    def __init__(
        self,
        channels=1,
        rate=44100,
        chunk=1024,
        audio_min_rms=1000,
        max_low_audio_flag=100,
        recording=True,
        recording_file="test.wav",
        stream_format=pyaudio.paInt16,
        pyaudio_instance=pyaudio.PyAudio(),
    ):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.audio_min_rms = audio_min_rms
        self.max_low_audio_flag = max_low_audio_flag
        self.recording = recording
        self.recording_file = recording_file
        self.audio_frames = []
        self.stream_format = stream_format
        self.pyaudio_instance = pyaudio_instance
        self.sample_width = self.pyaudio_instance.get_sample_size(stream_format)

    def show_realtime_rms(self, rms, audio_min_rms=1000):
        step = 40 / 2000  # 50#s for rms=2000
        sep = int(audio_min_rms * step)
        show = int(rms * step)
        print("\r", end="")
        progress = "current rms: "
        if show < sep:
            progress += "#" * show + " " * (sep - show)
        else:
            progress += "#" * sep
        progress += "|"

        if show > sep:
            progress += "#" * (show - sep)

        print(progress, end="")
        print("\033[K", end="")
        sys.stdout.flush()

    def detect_audio(self):
        """
        A function to detect audio.

        """

        print("start detecting audio...")
        # print(self.pyaudio_instance.open.read(1024))
        stream = self.pyaudio_instance.open(
            format=self.stream_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )
        low_audio_flag = 0
        detect_count = 0
        while True:
            detect_count += 1
            stream_data = stream.read(self.chunk)
            rms = audioop.rms(stream_data, 2)

            if rms > self.audio_min_rms:
                low_audio_flag = 0
            else:
                low_audio_flag += 1

            self.show_realtime_rms(rms, self.audio_min_rms)

            # 100 consecutive samples of low audio
            if low_audio_flag > self.max_low_audio_flag:
                print("\ndetecting finished...")
                break
            self.audio_frames.append(stream_data)
        stream.stop_stream()
        stream.close()
        self.pyaudio_instance.terminate()
        if self.recording:
            self.record()
        return self

    def record(self):
        """
        A function to record audio.

        """

        waveframe = wave.open(self.recording_file, "wb")
        waveframe.setnchannels(self.channels)
        waveframe.setsampwidth(self.sample_width)
        waveframe.setframerate(self.rate)
        waveframe.writeframes(b"".join(self.audio_frames))
        waveframe.close()
        return self
