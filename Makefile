GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# help
TARGET_MAX_CHAR_NUM=20
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)


# build python package
build:
	python setup.py sdist

# deploy package to pypi
deploy:
	twine upload dist/*

# test pypi deployment
deploy-test:
	twine upload -r testpypi dist/*

# run all tests
run-tests:
	pytest tests/*

# run unit tests
run-unit-tests:
	pytest tests/unit/*

# run api tests
run-api-tests:
	pytest tests/api/*

# type check python
type-check:
	mypy .

# lint
lint:
	flake8 rest_api_tester tests

# install dev dependencies
install-dev:
	pip install -r requirements.dev.txt

# enable commit hook for python linter
install-linter:
	pre-commit install
