# Contributing to openai-game-translator

## Get Started
1. Required python version: >=3.7, <3.11.
2. Clone openai-game-translator from git.
    ```shell
    git clone https://github.com/Erisae/openai-game-translator.git
    ```
3. Ensure that you have local credentials setup for your AWS account.
4. Ensure that you have portaudio.
    ```shell
    sudo apt install portaudio19-dev # linux
    brew install portaudio # macos
    ```
5. Install development dependencies.
    ```shell
    make develop
    ```

## Pull requests
1. Test with coverage, pass all test and coverage, replace `<appid>`, `<apikey>`, `<apisecret>`, `<openaikey>` with yours.
    ```shell
    make coverage xunfei_appid=<appid> xunfei_apikey=<apikey> xunfei_apisecret=<apisecret> openai_key=<openaikey>
    ```

2. Pass linting.
    ```shell
    make lint
    ```
3. Fix formmating if neccessary.
    ```shell
    make format
    ```

## Other
Please add tests for any new features.



