PYTEST_CMD=TESTING=true pytest tests -n 4 -vv

SHELL := /bin/bash # Use bash syntax

# dev aliases format and lint
RUFF=ruff app tests
BLACK=black app tests
MYPY=mypy app tests

install: ## install poetry and pip + all deps for the project
	pip install -U pip poetry
	poetry install

format: ## Reformat project code.
	${RUFF} --fix
	${BLACK}

lint: ## Lint project code
	${RUFF}
	${BLACK} --check
	${MYPY}

test: ## to run tests
	${PYTEST_CMD}

docker-build: ## docker-build to build the bot app
	docker build -t lamap-bot:latest -f Dockerfile .

compose-run: ## compose-run
	docker-compose up -d --build

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install docker-build lint format test help
