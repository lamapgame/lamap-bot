PYTEST_CMD=TESTING=true poetry run pytest test -n 4 -vv

SHELL := /bin/bash # Use bash syntax

# dev aliases format and lint
RUFF=poetry run ruff app test
BLACK=poetry run black app test
MYPY=poetry run mypy app test

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
