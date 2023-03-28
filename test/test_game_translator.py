import os 
import sys
import io
import unittest
import requests

from unittest.mock import patch

sys.path.append(os.path.abspath('../'))

from game_translator import translator

def contains_substring(string, substring):
    return substring in string

class TranslatorTest(unittest.TestCase):
    def test_xunfei_openai(self): 
        translator1 = translator("xunfei", filepath="../audio/audio_sample_little.wav", xunfei_appid=self.appid, 
                                 xunfei_apikey=self.apikey, xunfei_apisecret=self.apisecret, prerecorded=1, 
                                 output_language="English")

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            res = translator1.openai_translation()
            self.assertIsNotNone(res)
            self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'transcription success...'))
            self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'translation success...'))

    def test_aws_live_openai(self):
        translator2 = translator("aws_live", prerecorded=0, 
                                 output_language="English")

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            res = translator2.openai_translation()
            self.assertIsNotNone(res)
            self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'transcription success...'))
            self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'translation success...'))

    def test_aws_pre_openai(self):
        translator3 = translator("aws_pre", prerecorded=1, filepath="../audio/test1.wav",
                                 output_language="English")

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            res = translator3.openai_translation()
            self.assertIsNotNone(res)
            self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'transcription success...'))
            self.assertTrue(contains_substring(fake_out.getvalue().strip(), 'translation success...'))

