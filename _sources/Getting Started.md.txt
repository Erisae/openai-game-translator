# Getting Started

## Prerequisites
If you don't already have local credentials setup for your AWS account, you can follow this [guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for configuring them using the AWS CLI.

```eval_rst
.. note::
   * Since we use amazon-transcribe SDK, which is built on top of the `AWS Common Runtime (CRT) <https://github.com/awslabs/aws-crt-python>`_, non-standard operating systems may need to compile these libraries themselves.
   * Should at least set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables and in `[default]` profile `~/.aws/credentials`.
```

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

## Uninstallation
Uninstall the latest version from pip
```shell
pip uninstall openai-game-translator
```
Uninstall from github repository
```shell
make uninstall
```

## Terminal Usage
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

```eval_rst
.. note::
   * `<openai_key>`, `<model>`, `<use_prerecorded>` are required parameters.
```

## Script Usage
In Python script, first import library
```python
import openai
from game_translator import gameTranslator
```
Then fill in openai api key for global usage
```python
openai.api_key = "<openai_key>"
```
You can initialize multiple types of translators, using different transcription techniques
- Initialize a translation model with amazon live transcription
    ```python
    translator1 = gameTranslator("aws_live")
    ```
- Initialize a translation model with amazon prerecorded transcription and no prerecorded audio file,
    ```python
    translator2 = gameTranslator("aws_pre", filepath="path_to_store", prerecorded=False)
    ```
- Initialize a translation model with amazon prerecorded transcription and prerecorded audio file,
    ```python
    translator3 = gameTranslator("aws_pre", filepath="path_to_prerecorded", prerecorded=True)
    ```
- Initialize a translation model with xunfei speed transcription and no prerecorded audio file,
    ```python
    translator4 = gameTranslator("xunfei", xunfei_appid="xunfei_appid", xunfei_apikey="xunfei_apikey", xunfei_apisecret="xunfei_apisecret", filepath="path_to_store", prerecorded=False)
    ```
- Initialize a translation model with xunfei speed transcription and prerecorded audio file,
    ```python
    translator5 = gameTranslator("xunfei", xunfei_appid="xunfei_appid", xunfei_apikey="xunfei_apikey", xunfei_apisecret="xunfei_apisecret",  filepath="path_to_prerecorded", prerecorded=True)
    ```
Finally, call `openai_translation()` to translate,
```python
translator.openai_translation()
```
This will output the transcription and translation result to terminal.

You can also call to only transcribe,
```python
translator1.aws_live_transcription()
translator2.aws_prerecored_transcription()
translator3.aws_prerecored_transcription()
translator4.xunfei_transcription()
translator5.xunfei_transcription()
```