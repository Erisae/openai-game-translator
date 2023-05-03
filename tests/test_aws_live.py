import unittest
import asyncio
import os
import sys
import io
import numpy as np

sys.path.append(os.path.abspath("../"))
from unittest.mock import patch
from game_translator.aws_streaming_transcription.live_stream import live_transcribe
from game_translator.aws_streaming_transcription.settings import select_result, CHUNK_SIZE


class TestLiveStream(unittest.TestCase):
    @patch("sounddevice.rec")
    def test_transcription_success(self, mock_rec):
        # Set up mock audio data
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            mock_rec.return_value = np.array([[1] * CHUNK_SIZE])

            # Run the function under test and get the result
            self.loop = asyncio.get_event_loop()
            result = self.loop.run_until_complete(
                live_transcribe(input_language="english")
            )

            # Check that the result is as expected
            self.assertIsNotNone(result)
            self.assertEqual(fake_out.getvalue().strip(), "transcription success...")

    def test_select_result(self):
        # Set up test cases for select_result function
        test_cases = [
            (["hello", "world"], "helloworld"),
            (["goodbye", " world", "worldok"], "goodbyeworldok"),
            (["hello.", "hello", "world"], "hello.world"),
            (["hello", "world", "hello ", "world"], "helloworldhello world"),
        ]
        for sentences, expected in test_cases:
            with self.subTest(sentences=sentences):
                # Call the function under test
                result = select_result(sentences)
                # Check that the result is as expected
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
