# openai-game-translator
ChatGPT API based video game audio translator application and web service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub issues](https://img.shields.io/github/issues/Erisae/openai-game-translator)](https://github.com/Erisae/openai-game-translator/issues)
[![build](https://github.com/Erisae/openai-game-translator/actions/workflows/build.yml/badge.svg)](https://github.com/A-Chaudhary/age3d/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/Erisae/openai-game-translator/branch/main/graph/badge.svg?token=NI2HGVWMKI)](https://codecov.io/gh/Erisae/openai-game-translator)
[![PyPI](https://img.shields.io/pypi/v/openai-game-translator)](https://pypi.org/project/openai-game-translator/)


## Overview
A game translation app that uses the ChatGPT API to recognize in-game speech (and even game visuals) and provide smooth text translations on platforms like Switch and PS5, thanks to the powerful language abilities of GPT.

## Prerequisites
If you don't already have local credentials setup for your AWS account, you can follow this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for configuring them using the AWS CLI.

- Since we use amazon-transcribe SDK, which is built on top of the [AWS Common Runtime (CRT)](<https://github.com/awslabs/aws-crt-python>), non-standard operating systems may need to compile these libraries themselves.
- Should at least set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables and in `[default]` profile `~/.aws/credentials`.
  
Also, ensure that you have portaudio
```shell
sudo apt install portaudio19-dev # linux
brew install portaudio # macos
```

## Installation
Install the latest version from pip
```shell
pip install openai-game-translator
```
Install from github repository
```shell
git clone https://github.com/Erisae/openai-game-translator
make build
make install
```

## Quick Start
In terminal, run command `translate` to get audio translated to text.
```shell
translate --xunfei_appid <xf_appid> --xunfei_apikey  <xf_apikey> --xunfei_apisecret <xf_apisecret> --openai_key <openai_key> -t <model> -o <language> --pre_recorded <use_prerecored> --file <audio_path>
```
- `<xf_appid>`, `<xf_apikey>`, `<xf_apisecret>`: audio transcription api tokens from [xunfei](https://www.xfyun.cn/).
- `<openai_key>`: [openai api key](https://platform.openai.com/account/api-keys) is required for inferencing GPT model to translate.
- `<model>`: audio transcription model to choose, select from `aws_pre`, `aws_live`, `xunfei`.
- `<language>`: translation target language, default is English.
- `<use_prerecorded>`: whether to use prerecorded audio (1: yes, 0:no). When not using prerecorded audio, should ensure your device has sound card and the will detect and record audio for you.
- `<audio_path>`: the path for prerecorded audio or to store the detected audio.

In script, use the simplest `aws_live` transcription model and openai translation to defaultly translate to English.
```python
import openai
from game_translator import  gameTranslator

openai.api_key = "<openai_key>"
translator = gameTranslator("aws_live")
translator.openai_translation()
```

## Contributing
See more at [CONTRIBUTING.md](./CONTRIBUTING.md)


