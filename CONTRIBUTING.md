# Contributing to openai-game-translator

## Get Started
1. required python version: 3.9, 3.10
2. clone openai-game-translator from git
```shell
git clone https://github.com/Erisae/openai-game-translator.git
```
1. ensure that you have portaudio
```shell
sudo apt install portaudio19-dev # linux
brew install portaudio # macos
```
1. install development dependencies
```shell
make develop
```

## Pull requests
1. test with coverage, pass all test and coverage, replace `<appid>`, `<apikey>`, `<apisecret>`, `<openaikey>` with yours.
```shell
make coverage xunfei_appid=<appid> xunfei_apikey=<apikey> xunfei_apisecret=<apisecret> openai_key=<openaikey>
```

2. pass linting
```shell
make lint
```
3. fix formmating
```shell
make format
```

## Other
Please add tests for any new features



