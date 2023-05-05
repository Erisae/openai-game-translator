# openai-game-translator
ChatGPT API based video game audio translator application and web service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub issues](https://img.shields.io/github/issues/Erisae/openai-game-translator)](https://github.com/Erisae/openai-game-translator/issues)
[![build](https://github.com/Erisae/openai-game-translator/actions/workflows/build.yml/badge.svg)](https://github.com/A-Chaudhary/age3d/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/Erisae/openai-game-translator/branch/main/graph/badge.svg?token=NI2HGVWMKI)](https://codecov.io/gh/Erisae/openai-game-translator)
[![PyPI](https://img.shields.io/pypi/v/openai-game-translator)](https://pypi.org/project/openai-game-translator/)
[![Documentation Status](https://readthedocs.org/projects/openai-game-translator/badge/?version=latest)](https://openai-game-translator.readthedocs.io/en/latest/?badge=latest)
[![Doc](https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=GitHub%20Pages&logoColor=white)](https://erisae.github.io/openai-game-translator/)


## Overview
A game translation app that uses the ChatGPT API to recognize in-game speech (TODO: and even game visuals) and provide smooth text translations on platforms like Switch and PS5, thanks to the powerful language abilities of GPT.

## Prerequisites
If you don't already have local credentials setup for your AWS account, you can follow this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for configuring them using the AWS CLI.

- Since we use amazon-transcribe SDK, which is built on top of the [AWS Common Runtime (CRT)](<https://github.com/awslabs/aws-crt-python>), non-standard operating systems may need to compile these libraries themselves.
- Should at least set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables and in `[default]` profile `~/.aws/credentials`.
  
Also, ensure that you have `portaudio`, which is a prerequisite for `pyAudio`
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
cd openai-game-translator
make install
```

## Quick Start

### Terminal Usage
To translate audio to text in the terminal, use the command `translate`. The simplest way to achieve this is through `AWS`'s real-time media transcription and `GPT`-based translation, as shown below:
```shell
translate --openai_key <openai_key> -i <input_language> -o <output_language> aws_live
```
- `<openai_key>`: A valid [OpenAI API key](https://platform.openai.com/account/api-keys) is required for inferencing GPT model to translate.
- `<input_language>`: Language of the audio to be transcribed.
- `<output_language>`: Target language for the translation.
- `aws_live`: This option uses the AWS live stream transcription model, allowing the voice data stream to be uploaded to AWS services using the AWS SDK while recording the voice. Other available audio transcription models include `aws_pre` and `xunfei`, but they require additional arguments such as `--file`, `--pre_recorded`, and audio transcription API tokens from [xunfei](https://www.xfyun.cn/).
- Note that `aws_live`, `aws_pre`, `xunfei` work as subcommands. Ensure that `openai_key`, `input_language` and `output_language` are assigned before running these subcommands, as otherwise the argument values might not be recognized correctly.  For more information about how to use the package in command line, refer to the [documentation](https://erisae.github.io/openai-game-translator/). 

### Script Usage
In script, simply pass `aws_live` to initialize a `gameTranslator`, `translator.openai_translation()` will translate Chinese audio to English text.
```python
import openai
from game_translator import gameTranslator

openai.api_key = "<openai_key>"
translator = gameTranslator("aws_live", input_language="chinese", output_language="english")
translator.openai_translation()
```

## Contributing
See more at [CONTRIBUTING.md](./CONTRIBUTING.md)


