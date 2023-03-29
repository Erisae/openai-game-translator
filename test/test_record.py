import unittest
import os
import sys
import io

sys.path.append(os.path.abspath("../"))

from unittest.mock import patch
from audio.record import Detector


def contains_substring(string, substring):
    return substring in string


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.filepath = "../audio/test.wav"
        self.detector = Detector(recording_file=self.filepath)

    def test_detect_audio(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.detector.detect_audio()
            file_stat = os.stat(self.filepath)
            self.assertTrue(
                contains_substring(
                    fake_out.getvalue().strip(), "detecting finished ..."
                )
            )
            self.assertTrue(os.path.isfile(self.filepath))
            self.assertTrue(file_stat.st_size > 0)


if __name__ == "__main__":
    unittest.main()
