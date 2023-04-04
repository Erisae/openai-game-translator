"""
This module provides translator main function.

Classes:
- translator: a self designed translaor

Author: Yuhan Xia
Copyright: Copyright (c) 2023
License: Apache-2.0
Version: 2.0
"""
import asyncio
import argparse
import openai

from .xunfei_speed_transcription.ost_fast import xf_transcriptor
from .openai_translation.chat import translate_sentence
from .audio.record import Detector
from .aws_streaming_transcription import live_stream
from .aws_streaming_transcription import prerecorded_stream


class gameTranslator:
    """
    A class representing a translator.

    Attributes:
    """

    def __init__(
        self,
        transcription_model,
        filepath="",
        xunfei_appid="",
        xunfei_apikey="",
        xunfei_apisecret="",
        prerecorded=True,
        output_language="English",
    ):
        self.filepath = ""
        self.transcription_model = transcription_model
        if self.transcription_model == "xunfei":
            self.appid = xunfei_appid
            self.apikey = xunfei_apikey
            self.apisecret = xunfei_apisecret
            self.filepath = filepath

        if self.transcription_model == "aws_pre":
            self.filepath = filepath
        self.target_language = output_language
        self.pre_recorded = prerecorded

    def record_audio(self):
        """
        A function to record video.

        """
        recorder = Detector(recording_file=self.filepath)
        recorder.detect_audio()

    def xunfei_transcription(self):
        """
        A function to call xunfei transcription

        """
        if not self.pre_recorded:
            self.record_audio()
        transcriptor = xf_transcriptor(
            self.appid, self.apikey, self.apisecret, self.filepath
        )
        transcriptor.get_fileurl()
        content = transcriptor.get_result()
        return content

    def aws_prerecored_transcription(self):
        """
        A function to call aws prerecorded transcription

        """
        if not self.pre_recorded:
            self.record_audio()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            prerecorded_stream.basic_transcribe(self.filepath)
        )
        # loop.close()
        return result

    def aws_live_transcription(self):
        """
        A function to call aws live transcription

        """
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(live_stream.basic_transcribe())
        # loop.close()
        return result

    def openai_translation(self):
        """
        A function to do translation

        """
        # first do transcription then translation
        if self.transcription_model == "xunfei":
            text = self.xunfei_transcription()
        elif self.transcription_model == "aws_pre":
            text = self.aws_prerecored_transcription()
        elif self.transcription_model == "aws_live":
            text = self.aws_live_transcription()

        res = translate_sentence(text, self.target_language)
        return res
    
def main():
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument(
        "--file", type=str, default="./audio/test.wav", help="prerecorded file path"
    )
    parser.add_argument("--xunfei_appid", type=str, help="xunfei transcription appid")
    parser.add_argument("--xunfei_apikey", type=str, help="xunfei transcription apikey")
    parser.add_argument(
        "--xunfei_apisecret", type=str, help="xunfei transccription api secret"
    )
    parser.add_argument(
        "--openai_key", required=True, type=str, help="open ai translatio api key"
    )
    parser.add_argument(
        "-t",
        "--transcription_model",
        required=True,
        type=str,
        choices=["xunfei", "aws_pre", "aws_live"],
        help="xunfei and aws_pre need prerecorded audios, aws_live not",
    )
    parser.add_argument(
        "-o",
        "--output_language",
        required=True,
        type=str,
        help="output text's language",
    )
    parser.add_argument(
        "--pre_recorded",
        required=True,
        type=int,
        choices=[0, 1],
        default=0,
        help="when select 1, use audio that already exist",
    )

    args = parser.parse_args()
    openai.api_key = args.openai_key

    new_translator = gameTranslator(
        args.transcription_model,
        filepath=args.file,
        xunfei_appid=args.xunfei_appid,
        xunfei_apikey=args.xunfei_apikey,
        xunfei_apisecret=args.xunfei_apisecret,
        prerecorded=args.pre_recorded,
        output_language=args.output_language,
    )
    new_translator.openai_translation()


if __name__ == "__main__":
    main()




# todo: language change
# todo: precision
# todo: audio transmitting
