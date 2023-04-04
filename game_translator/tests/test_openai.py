import unittest
import os
import sys
import io
sys.path.append(os.path.abspath("../"))
from unittest.mock import patch
from openai_translation.chat import translate_sentence


def contains_substring(string, substring):
    return substring in string


class TestOpenai(unittest.TestCase):
    def setUp(self):
        self.language = "Japanese"

    def test_translation(self):
        test_cases = [
            "this is the first time i do an oss project",
            "helloworld",
            "hello world",
            "",
        ]
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                # Call the function under test
                with patch("sys.stdout", new=io.StringIO()) as fake_out:
                    result = translate_sentence(sentence, self.language)
                    # Check that the result is as expected
                    self.assertTrue(
                        contains_substring(
                            fake_out.getvalue().strip(), "translation success..."
                        )
                    )
                    self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
