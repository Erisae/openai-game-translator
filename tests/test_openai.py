import unittest
import os
import sys
import io
sys.path.append(os.path.abspath("../"))
from unittest.mock import patch
from game_translator.openai_translation.chat import translate_sentence


def contains_substring(string, substring):
    return substring in string


class TestOpenai(unittest.TestCase):
    def setUp(self):
        self.language = "Japanese"

    def test_translation(self):
        test_cases = [
            "this is the first time i do an oss project",
            # "",
        ] # 3 per min
        for sentence in test_cases:
            with self.subTest(sentence=sentence):
                # Call the function under test
                with patch("sys.stdout", new=io.StringIO()) as fake_out:
                    result = translate_sentence(sentence, self.language)

                    # Check that the result is as expected
                    self.assertIn("translation success...", fake_out.getvalue().strip())
                    self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
