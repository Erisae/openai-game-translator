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
    An audio game translator class,

    This class provides functinalities for ...

    Attributes:
        filepath(str): file path for prerecorded audio file or to be recorded.
        transcription_model(str): choose from "aws_pre", "aws_live" and "xunfei".
        appid(str): xunfei transcription appid.
        apikey(str): xunfei transcription apikey.
        apisecret(str): xunfei transcription apisecret.
        pre_recorded(bool): whether needs prerecorded audio file.
        target_language(str): translation output language.
    """

    def __init__(
        self,
        transcription_model,
        filepath="",
        xunfei_appid="",
        xunfei_apikey="",
        xunfei_apisecret="",
        prerecorded=True,
        input_language="chinese",
        output_language="english",
    ):
        """
        Initialize a new instance of gameTranslator.

        Args:
            transcription_model(str): choose from "aws_pre", "aws_live" and "xunfei".
            filepath(str): file path for prerecorded audio file or to be recorded.
            xunfei_appid(str): xunfei transcription appid.
            xunfei_apikey(str): xunfei transcription apikey.
            xunfei_apisecret(str): xunfei transcription apisecret.
            prerecorded(bool): whether needs prerecorded audio file.
            input_language(str): transcription input language.
            output_language(str): translation output language.
        """
        self.filepath = ""
        self.transcription_model = transcription_model
        if self.transcription_model == "xunfei":
            self.appid = xunfei_appid
            self.apikey = xunfei_apikey
            self.apisecret = xunfei_apisecret
            self.filepath = filepath

        if self.transcription_model == "aws_pre":
            self.filepath = filepath
        self.input_language = input_language
        self.output_language = output_language
        self.pre_recorded = prerecorded

    def record_audio(self):
        """
        Detects and records audio using pyaudio, saves at self.filepath.

        Args:
            None
        Returns:
            None
        """
        recorder = Detector(recording_file=self.filepath)
        recorder.detect_audio()

    def xunfei_transcription(self):
        """
        Transcripts audio file with xunfei speed transcription, if not self.pre_recorded, record() first.

        Args:
            None
        Returns:
            str: transcription result.
        """
        if not self.pre_recorded:
            self.record_audio()
        transcriptor = xf_transcriptor(
            self.appid, self.apikey, self.apisecret, self.filepath, self.input_language
        )
        transcriptor.get_fileurl()
        content = transcriptor.get_result()
        return content

    def aws_prerecored_transcription(self):
        """
        Transcripts audio file with awd_prerecorded transcription, if not self.pre_recorded, record() first.

        Args:
            None
        Returns:
            str: transcription result.
        """
        if not self.pre_recorded:
            self.record_audio()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            prerecorded_stream.prerecorded_transcribe(self.filepath, self.input_language)
        )
        # loop.close()
        return result

    def aws_live_transcription(self):
        """
        Transcripts audio file with aws_live transcription. Record with sounddevice and send stream to aws simultaneously.

        Args:
            None
        Returns:
            str: transcription result.
        """
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(live_stream.live_transcribe(self.input_language))
        # loop.close()
        return result

    def openai_translation(self):
        """
        Translates text to target language using openai.

        Args:
            None
        Returns:
            str: translation result.
        """
        # first do transcription then translation
        if self.transcription_model == "xunfei":
            text = self.xunfei_transcription()
        elif self.transcription_model == "aws_pre":
            text = self.aws_prerecored_transcription()
        elif self.transcription_model == "aws_live":
            text = self.aws_live_transcription()

        res = translate_sentence(text, self.output_language)
        return res


def main():
    """
    main() function that takes cmd line input to instantiate and run a translator.
    """
    parser = argparse.ArgumentParser(description="audio based openai game translator")
    parser.add_argument(
        "--file", type=str, default="./audio/test.wav", help="file path"
    )
    parser.add_argument("--xunfei_appid", type=str, help="xunfei appid")
    parser.add_argument("--xunfei_apikey", type=str, help="xunfei apikey")
    parser.add_argument("--xunfei_apisecret", type=str, help="xunfei api secret")
    parser.add_argument("--openai_key", required=True, type=str, help="openai api key")
    parser.add_argument(
        "-t",
        "--transcription_model",
        required=True,
        type=str,
        choices=["xunfei", "aws_pre", "aws_live"],
        help="[xunfei] and [aws_pre] need prerecorded audio, [aws_live] not",
    )
    parser.add_argument(
        "-i",
        "--input_language",
        required=True,
        type=str,
        help="audio input language",
    )
    parser.add_argument(
        "-o",
        "--output_language",
        required=True,
        type=str,
        help="target translation language",
    )
    parser.add_argument(
        "--pre_recorded",
        required=True,
        type=int,
        choices=[0, 1],
        default=0,
        help="[1]use prerecorded audio, [0]record audio",
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
        input_language=args.input_language,
        output_language=args.output_language,
    )
    new_translator.openai_translation()


if __name__ == "__main__":
    main()


# todo: precision
# todo: audio transmitting
# todo: add chat context [currently unavailable]
