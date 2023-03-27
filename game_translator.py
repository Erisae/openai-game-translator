from xunfei_speed_transcription.ost_fast import xf_transcriptor
from openai_translation.chat import tranlate_sentence
from audio.record import Detector

import aws_streaming_transcription.live_stream as live_stream
import aws_streaming_transcription.prerecorded_stream as prerecorded_stream

import openai
import asyncio
import argparse


parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('--file', type=str, default='./audio/test.wav', help='prerecorded file path')
parser.add_argument('--xunfei_appid', type=str, help='xunfei transcription appid')
parser.add_argument('--xunfei_apikey', type=str, help='xunfei transcription apikey')
parser.add_argument('--xunfei_apisecret', type=str, help='xunfei transccription api secret')
parser.add_argument('--openai_key', required=True, type=str, help='open ai translatio api key')
parser.add_argument('-t', '--transcription_model', required=True, type=str, choices=['xunfei', 'aws_pre', 'aws_live'], help='3 ways of transcription are provided, xunfei and aws_pre need prerecorded audios, aws_live not')
# parser.add_argument('-i', '--input_language', required=True, type=str, choices=['en', 'cn', 'jp'], help='input audio\'s language')
parser.add_argument('-o', '--output_language', required=True, type=str, help='output text\'s language')
parser.add_argument('--pre_recorded', required=True, type=int, choices=[0, 1], default=0, help='when select 1, use audio that already exist')

args = parser.parse_args()
openai.api_key = args.openai_key

class translator(object):
    def __init__(self):
        self.filepath = ""
        if args.transcription_model == 'xunfei':
            self.appid = args.xunfei_appid
            self.apikey = args.xunfei_apikey
            self.apisecret = args.xunfei_apisecret
            self.filepath = args.file

        if args.transcription_model == 'aws_pre':
            self.filepath = args.file
        
        self.target_language = args.output_language
        self.pre_recorded = args.pre_recorded


    def record_audio(self):
        recorder = Detector(recording_file=self.filepath)
        recorder.detect_audio()

    def xunfei_transcription(self):
        if not self.pre_recorded:
            self.record_audio()
        gClass = xf_transcriptor(self.appid, self.apikey, self.apisecret, self.filepath)
        gClass.get_fileurl()
        s = gClass.get_result()
        return s

    def aws_prerecored_transcription(self):
        if not self.pre_recorded:
            self.record_audio()
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(prerecorded_stream.basic_transcribe(self.filepath))
        loop.close()
        return results

    def aws_live_transcription(self):
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(live_stream.basic_transcribe())
        loop.close()
        return results

    def openai_translation(self):
        # first do transcription then translation
        if args.transcription_model == 'xunfei':
            text = self.xunfei_transcription()
        elif args.transcription_model == 'aws_pre':
            text = self.aws_prerecored_transcription()
        elif args.transcription_model == 'aws_live':
            text = self.aws_live_transcription()

        res = tranlate_sentence(text, self.target_language)
        return res

if __name__== "__main__":
    new_translator = translator()
    new_translator.openai_translation()


# todo: language change
# todo: precision
# todo: audio transmitting