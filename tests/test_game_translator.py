import os
import sys
import io
import unittest

from unittest.mock import patch
sys.path.append(os.path.abspath("../"))
from game_translator.game_translator import gameTranslator


def contains_substring(string, substring):
    return substring in string


class TranslatorTest(unittest.TestCase):
    def test_xunfei_openai(self):
        translator1 = gameTranslator(
            "xunfei",
            filepath="../game_translator/audio/audio_sample_little.wav",
            xunfei_appid=self.appid,
            xunfei_apikey=self.apikey,
            xunfei_apisecret=self.apisecret,
            prerecorded=True,
            input_language="chinese",
            output_language="english",
            
        )

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            res = translator1.openai_translation()
            self.assertIsNotNone(res)
            self.assertTrue(
                contains_substring(
                    fake_out.getvalue().strip(), "transcription success..."
                )
            )
            self.assertTrue(
                contains_substring(
                    fake_out.getvalue().strip(), "translation success..."
                )
            )

    def test_aws_pre_openai(self):
        translator3 = gameTranslator(
            "aws_pre",
            prerecorded=True,
            filepath="../game_translator/audio/audio_sample_little.wav",
            output_language="english",
        )

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            res = translator3.openai_translation()
            self.assertIsNotNone(res)
            self.assertTrue(
                contains_substring(
                    fake_out.getvalue().strip(), "transcription success..."
                )
            )
            self.assertTrue(
                contains_substring(
                    fake_out.getvalue().strip(), "translation success..."
                )
            )

    # def test_aws_live_openai(self):
    #     translator2 = translator("aws_live", prerecorded=0,
    #                              output_language="English")

    #     with patch('sys.stdout', new=io.StringIO()) as fake_out:
    #         res = translator2.openai_translation()
    #         self.assertIsNotNone(res)
    #         self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'transcription success...'))
    #         self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'translation success...'))
