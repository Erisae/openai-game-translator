import unittest
import asyncio
import os
import sys
import io

sys.path.append(os.path.abspath("../"))
from unittest.mock import patch
from game_translator.aws_streaming_transcription.prerecorded_stream import prerecorded_transcribe
from game_translator.aws_streaming_transcription.settings import select_result


class TestPrerecorded(unittest.TestCase):
    def setUp(self):
        self.filepath = "../game_translator/audio/audio_sample_little.wav"

    def test_transcription(self):
        # Set up mock audio data
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            # Run the function under test and get the result
            loop1 = asyncio.get_event_loop()
            result = loop1.run_until_complete(prerecorded_transcribe(input_language="english", audio_path=self.filepath))

            # Check that the result is as expected
            self.assertIsNotNone(result)
            self.assertIn("transcription success...", fake_out.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
