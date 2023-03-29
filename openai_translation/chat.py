"""
This module provides openai translation

Classes:
- translate_sentence:

Author: Yuhan Xia
Copyright: Copyright (c) 2023
License: Apache-2.0
Version: 2.0
"""

import openai


def translate_sentence(content, language):
    """
    A function to use openai to translate

    """

    prompt = "translate to " + language + " : " + content
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    print("translation success...")
    return completion.choices[0].message.content.lstrip()[1:]
