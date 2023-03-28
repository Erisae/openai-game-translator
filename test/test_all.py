import unittest
import coverage
import argparse
import openai

from test_xunfei import TestXFTranscriptor
from test_aws_live import TestLiveStream
from test_aws_pre import TestPrerecorded
from test_openai import TestOpenai
from test_record import TestRecord

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('--xunfei_appid', required=True, type=str, help='xunfei transcription appid')
parser.add_argument('--xunfei_apikey', required=True, type=str, help='xunfei transcription apikey')
parser.add_argument('--xunfei_apisecret', required=True, type=str, help='xunfei transccription api secret')
parser.add_argument('--openai_key', required=True, type=str, help='open ai translatio api key')
args = parser.parse_args()
openai.api_key = args.openai_key

if __name__== "__main__":
    # define overall testsuite
    test_suite = unittest.TestSuite()

    # add testsuites
    TestXFTranscriptor.appid = args.xunfei_appid
    TestXFTranscriptor.apikey = args.xunfei_apikey
    TestXFTranscriptor.apisecret = args.xunfei_apisecret
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestXFTranscriptor))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPrerecorded))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLiveStream))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestOpenai))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRecord))

    # run all tests and generate coverage report
    cov = coverage.Coverage()
    cov.start()

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

    cov.stop()
    cov.report()
