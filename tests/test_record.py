import unittest
import os
import sys
import io
import pyaudio

sys.path.append(os.path.abspath("../"))
from unittest.mock import patch
from game_translator.audio.record import Detector


def contains_substring(string, substring):
    return substring in string


class TestRecord(unittest.TestCase):
    @patch('pyaudio.PyAudio')
    def test_detect_audio(self, mock_pyaudio):
        mock_data = bytes([0] * 1024)
        mock_flag = 30
        mock_pyaudio.open(format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024).read.return_value = mock_data
        
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            detector = Detector(pyaudio_instance=mock_pyaudio, max_low_audio_flag=mock_flag, recording=False)
            detector.detect_audio()

        self.assertIn("detecting finished...", fake_out.getvalue().strip())
        self.assertEqual(len(detector.audio_frames), mock_flag)



if __name__ == "__main__":
    unittest.main()
