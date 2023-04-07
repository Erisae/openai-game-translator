#########
# BUILD #
#########
develop:  ## install develop dependencies -- package along with all dependencies
	python -m pip install .[develop]

build: ## build libary and place bin in ./build
	python setup.py build

install:  ## install library
	python -m pip install .

uninstall:
	pip uninstall openai-game-translator

########
# DIST #
########
dist-build:  # create source and wheel distribution in ./dist
	python setup.py sdist bdist_wheel 

dist-check: # check if distribution suits PyPi
	python -m twine check dist/*

dist: clean build dist-build dist-check  ## Build dists

publish-test: # Upload python assets to PyPi test
	python -m twine upload --repository testpypi dist/*

publish:  # Upload python assets
	python -m twine upload dist/*

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
	python -m black --check game_translator setup.py
	python -m flake8 --extend-ignore=E501,F401 game_translator setup.py

lints: lint

format:  ## run autoformatting with black
	python -m black game_translator setup.py

###########
# VERSION #
###########
show-version:
	bump2version --dry-run --allow-dirty setup.py --list | grep current | awk -F= '{print $2}'

bump:
	bump2version --current-version $(current_version) --new-version $(new_version) game_translator/_version.py pyproject.toml --allow-dirty	

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major

#########
# CLEAN #
#########
clean: ## clean the repository
	rm -rf tests/.coverage tests/coverage.xml
	rm -rf dist *.egg-info build


