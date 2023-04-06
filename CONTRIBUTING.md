# Contributing to openai-game-translator

## Get Started
1. required python version: 3.7, 3.8, 3.9, 3.10
2. clone openai-game-translator from git
```shell
git clone https://github.com/Erisae/openai-game-translator.git
```
3. install development dependencies
```shell
make dependencies
```

## Pull requests
1. prepare for testing and linting enviroment
```shell
make test-dev
```
2. test with coverage, pass all test and coverage, replace `<appid>`, `<apikey>`, `<apisecret>`, `<openaikey>` with yours.
```shell
make coverage xunfei_appid=<appid> xunfei_apikey=<apikey> xunfei_apisecret=<apisecret> openai_key=<openaikey>
```

3. pass linting
```shell
make lint
```
4. fix formmating
```shell
make format
```

## Other
Please add tests for any new features



