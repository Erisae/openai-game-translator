# Examples

## Import Library and Set OpenAI
```python
import openai
from game_translator import gameTranslator
openai.api_key = "sk-xxxx"
```

## AWS live version
```python
translator = gameTranslator("aws_live", output_language="Chinese")
translator.openai_translation()
```

```shell
transcription success...
Eh, weather is nice today.
translation success...
嗯，今天天气不错。
```

## AWS prerecorded version 
- not using a prerecorded audio file
    ```python
    translator = gameTranslator("aws_pre", file_path="./audio/temp.wav", prerecorded=False, output_language="Chinese")
    translator.openai_translation()
    ```

    ```shell
    start detecting audio ... 
    detecting finished ... 
    transcription success...
    Eh, weather is nice today.
    translation success...
    嗯，今天天气不错。
    ```
- using a prerecorded ausio file
    ```python
    translator = gameTranslator("aws_pre", file_path="./audio/temp.wav", prerecorded=True, output_language="Chinese")
    translator.openai_translation()
    ```

    ```shell
    transcription success...
    Eh, weather is nice today.
    translation success...
    嗯，今天天气不错。
    ```

## Xunfei version
- using a prerecorded audio file
    ```python
    translator = gameTranslator("xunfei", xunfei_appid="xxx", xunfei_apikey="xxx", xunfei_apisecret="xxx", filepath="./audio/audio_sample_little.wav", prerecorded=True, output_language="English")
    translator.openai_translaion()
    ```

    ```shell
    transcription success...
    科大讯飞是中国最大的智能语音技术提供商。
    translation success...
    iFlytek is the largest intelligent voice technology provider in China.
    ```
- not using a prerecorded audio file
    ```python
    translator = gameTranslator("xunfei", xunfei_appid="xxx", xunfei_apikey="xxx", xunfei_apisecret="xxx", filepath="./audio/temp.wav", prerecorded=False, output_language="English")
    translator.openai_translaion()
    ```

    ```shell
    start detecting audio ... 
    detecting finished ... 
    transcription success...
    科大讯飞是中国最大的智能语音技术提供商。
    translation success...
    iFlytek is the largest intelligent voice technology provider in China.
    ```