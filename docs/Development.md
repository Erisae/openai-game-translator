# Development

## Develop dependencies
- Required python version: >=3.7, <3.11.
- Clone openai-game-translator from git.
    ```shell
    git clone https://github.com/Erisae/openai-game-translator.git
    ```
- Ensure that you have local credentials setup for your AWS account.
- Ensure that you have portaudio.
    ```shell
    sudo apt install portaudio19-dev # linux
    brew install portaudio # macos
    ```
- Install development dependencies.
    ```shell
    cd openai-game-translator
    make develop
    ```

## Pull requests
- Test with coverage, pass all test and coverage, replace `<appid>`, `<apikey>`, `<apisecret>`, `<openaikey>` with yours.
    ```shell
    make coverage xunfei_appid=<appid> xunfei_apikey=<apikey> xunfei_apisecret=<apisecret> openai_key=<openaikey>
    ```

- Pass linting.
    ```shell
    make lint
    ```
- Fix formmating if neccessary.
    ```shell
    make format
    ```