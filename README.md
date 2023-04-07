# openai-game-translator
ChatGPT API based video game audio translator application and web service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub issues](https://img.shields.io/github/issues/Erisae/openai-game-translator)](https://github.com/Erisae/openai-game-translator/issues)
[![build](https://github.com/Erisae/openai-game-translator/actions/workflows/build.yml/badge.svg)](https://github.com/A-Chaudhary/age3d/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/Erisae/openai-game-translator/branch/main/graph/badge.svg?token=NI2HGVWMKI)](https://codecov.io/gh/Erisae/openai-game-translator)
[![PyPI](https://img.shields.io/pypi/v/openai-game-translator)](https://pypi.org/project/openai-game-translator/)


## Overview
A game translation app that uses the ChatGPT API to recognize in-game speech (and even game visuals) and provide smooth text translations on platforms like Switch and PS5, thanks to the powerful language abilities of GPT.

## Installation
```shell
pip install openai-game-translator
```

## Quick Start
In terminal, run
```shell
translate --xunfei_appid <appid> --xunfei_apikey  <apikey> --xunfei_apisecret <apisecret> --openai_key <key> -t <model> -o <language> --pre_recorded <use_prerecored:0|1> --file <audio_path>
```
- `<model>`: transcription model, choose from `aws_pre`, `aws_live` and `xunfei`.
- `<language>`: translation target language, for example "English"
- `<use_prerecored>`: whether to use prerecorded audio, 0 no, 1 yes
- `<audio_path>`: prerecorded or transcription related audio file path

In script, use
```python
import openai
from game_translator import  gameTranslator

openai.api_key = "<openai_key>"
translator = gameTranslator("aws_live")
translator.openai_translation()
```


