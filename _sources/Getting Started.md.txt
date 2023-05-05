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
cd openai-game-translator
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
In terminal, run command `translate` to get audio translated to text. Multiple ways are provided:
- `aws_live` transcription **(best currently)**:
    ```shell
    translate --openai_key <openai_key> -i <input_language> -o <output_language> aws_live
    ```
    - `<openai_key>`: A valid [OpenAI API key](https://platform.openai.com/account/api-keys) is required for inferencing GPT model to translate.
    - `<input_language>`: Language of the audio to be transcribed.
    - `<output_language>`: Target language for the translation.
    - `aws_live`: This option uses the AWS live stream transcription model, allowing the voice data stream to be uploaded to AWS services using the AWS SDK while recording the voice. This process does not require the generation of temporary audio files or the use of prerecorded files. 

- `aws_pre` transcription with prerecorded media:
    ```shell
    translate --openai_key <openai_key> -i <input_language> -o <output_language> aws_pre --file <file_path> --pre_recorded
    ```
    - `aws_pre`: This option uses AWS pre-recorded stream transcription model. Prerecorded file is uploaded to AWS service using AWS SDK.
    - `<file_path>`: Path for the prerecorded media.
    - `--pre_recorded`: Token specifying prerecorded media is needed.
- `aws_pre` transcription without prerecorded media:
    ```shell
    translate --openai_key <openai_key> -i <input_language> -o <output_language> aws_pre --file <file_path>
    ```
    - `<file_path>`: Path to store temporary audio file while translating.
- `xunfei` transcription with prerecorded media:
    ```shell
    translate --openai_key <openai_key> -i <input_language> -o <output_language> xunfei --xunfei_appid <xf_appid> --xunfei_apikey  <xf_apikey> --xunfei_apisecret <xf_apisecret> --file <file_path> --pre_recorded 
    ```
    - `xunfei`: This option uses xunfei's transcription model.
    - `<xf_appid>`, `<xf_apikey>`, `<xf_apisecret>`: audio transcription api tokens from [xunfei](https://www.xfyun.cn/).
- `xunfei` transcription without prerecorded media:
    ```shell
    translate --openai_key <openai_key> -i <input_language> -o <output_language> xunfei --xunfei_appid <xf_appid> --xunfei_apikey  <xf_apikey> --xunfei_apisecret <xf_apisecret> --file <file_path>
    ```

```eval_rst
.. note::
   * `aws_live`, `aws_pre` and `xunfei` are subcommands, whether `--file`, `--pre_recorded` and the xunfei tokens are required are constrained by these subcommands. 
   * Ensure that `openai_key`, `input_language` and `output_language` are assigned before running these subcommands, as otherwise the argument values might not be recognized correctly.
   * In terms of transcription accuracy, I would recommend to use `aws_live` as `aws_pre` and `xunfei` have high requirements for the quality of audio files (prominent human voice, no significant noise). The latter two actually performs well in ideal conditions (and is a substitute for those who can not access AWS). 
```

## Script Usage
In Python script, first import library
```python
import openai
from game_translator import gameTranslator
```
Then fill in OpenAI API key for global usage
```python
openai.api_key = "<openai_key>"
```
You can initialize multiple types of translators, using different transcription techniques
- Initialize a translation model with Amazon live transcription
    ```python
    translator1 = gameTranslator("aws_live") # by default, input language is Chinese and output language is English
    ```
- Initialize a translation model with Amazon prerecorded transcription and no prerecorded audio file,
    ```python
    translator2 = gameTranslator("aws_pre", filepath="path_to_store", prerecorded=False)
    ```
- Initialize a translation model with Amazon prerecorded transcription and prerecorded audio file,
    ```python
    translator3 = gameTranslator("aws_pre", filepath="path_to_prerecorded", prerecorded=True)
    ```
- Initialize a translation model with xunfei speed transcription and no prerecorded audio file,
    ```python
    translator4 = gameTranslator("xunfei", xunfei_appid="xunfei_appid", xunfei_apikey="xunfei_apikey", xunfei_apisecret="xunfei_apisecret", filepath="path_to_store", prerecorded=False)
    ```
```eval_rst
.. note::
   * xunfei generally only transcribe Chinese and English (for free).
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