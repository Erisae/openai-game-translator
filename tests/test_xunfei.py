import unittest
import io
import sys
import os

sys.path.append(os.path.abspath("../"))

from unittest.mock import patch
from xunfei_speed_transcription.ost_fast import xf_transcriptor


def contains_substring(string, substring):
    return substring in string


class TestXFTranscriptor(unittest.TestCase):
    def setUp(self):  #
        self.file_path = "../audio/audio_sample_little.wav"
        self.transcriptor = xf_transcriptor(
            self.appid, self.apikey, self.apisecret, self.file_path
        )

    # def test_task_create(self):
    #     task_id = self.transcriptor.task_create()
    #     self.assertIsNotNone(task_id)

    def test_get_result(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.transcriptor.get_fileurl()
            result = self.transcriptor.get_result()
            self.assertIsNotNone(result)
            self.assertEqual(result, "科大讯飞是中国最大的智能语音技术提供商。")
            self.assertTrue(
                contains_substring(
                    fake_out.getvalue().strip(), "transcription success..."
                )
            )


if __name__ == "__main__":
    unittest.main()
