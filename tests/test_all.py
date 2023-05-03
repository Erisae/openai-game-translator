import unittest
import argparse
import openai

from test_xunfei import TestXFTranscriptor
from test_aws_live import TestLiveStream
from test_aws_pre import TestPrerecorded
from test_openai import TestOpenai
from test_record import TestRecord
from test_game_translator import TranslatorTest

def main():
    parser_test = argparse.ArgumentParser(description="Test openai-game-translator")
    parser_test.add_argument(
        "--xunfei_appid", required=True, type=str, help="xunfei transcription appid"
    )
    parser_test.add_argument(
        "--xunfei_apikey", required=True, type=str, help="xunfei transcription apikey"
    )
    parser_test.add_argument(
        "--xunfei_apisecret",
        required=True,
        type=str,
        help="xunfei transccription api secret",
    )
    parser_test.add_argument(
        "--openai_key", required=True, type=str, help="openai api key"
    )
    args_test = parser_test.parse_args()
    openai.api_key = args_test.openai_key
     # define overall testsuite
    test_suite = unittest.TestSuite()

    # add testsuites
    TestXFTranscriptor.appid = args_test.xunfei_appid
    TestXFTranscriptor.apikey = args_test.xunfei_apikey
    TestXFTranscriptor.apisecret = args_test.xunfei_apisecret
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestXFTranscriptor))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPrerecorded))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLiveStream))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestOpenai))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRecord))

    # add integration test
    TranslatorTest.appid = args_test.xunfei_appid
    TranslatorTest.apikey = args_test.xunfei_apikey
    TranslatorTest.apisecret = args_test.xunfei_apisecret
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TranslatorTest))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == "__main__":
   main()
