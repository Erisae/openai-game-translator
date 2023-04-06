#########
# BUILD #
#########
develop:  ## install dependencies
	python -m pip install aiofile
	python -m pip install amazon_transcribe
	python -m pip install numpy
	python -m pip install openai
	python -m pip install pyaudio
	python -m pip install requests
	python -m pip install sounddevice
	python -m pip install urllib3

test-dev:
	python -m pip install coverage
	python -m pip install black
	python -m pip install flake8

#########
# TESTS #
#########
coverage: ## test with coverage 
	cd tests && coverage run --rcfile=.coveragerc test_all.py --xunfei_appid $(xunfei_appid) --xunfei_apikey $(xunfei_apikey) --xunfei_apisecret $(xunfei_apisecret) --openai_key $(openai_key)
	cd tests && coverage xml -o coverage.xml

test: ## test
	cd tests && python test_all.py --xunfei_appid $(xunfei_appid) --xunfei_apikey $(xunfei_apikey) --xunfei_apisecret $(xunfei_apisecret) --openai_key $(openai_key)

tests: test


#########
# LINTS #
#########
lint: ## omiting E501: line too long and F401 imported but unused
	python -m black --check game_translator
	python -m flake8 --extend-ignore=E501,F401 game_translator  

lints: lint

format:  ## run autoformatting with black
	python -m black game_translator

#########
# CLEAN #
#########
clean: ## clean the repository
	rm -rf tests/.coverage tests/coverage.xml
	rm -rf dist *.egg-info


