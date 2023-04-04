# openai-game-translator
ChatGPT API based video game audio translator application and web service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub issues](https://img.shields.io/github/issues/Erisae/openai-game-translator)
![build and test](https://github.com/Erisae/openai-game-translator/actions/workflows/test_and_coverage.yml/badge.svg)
![coverage](./test/coverage.svg)


## Overview
A game translation app that uses the ChatGPT API to recognize in-game speech (and even game visuals) and provide smooth text translations on platforms like Switch and PS5, thanks to the powerful language abilities of GPT.

## Installation
```shell
pip install openai-game-translator==0.0.5
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


