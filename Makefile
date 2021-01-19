ifeq (, $(shell which poetry))
$(error "No poetry found in PATH, check out: https://github.com/python-poetry/poetry#installation")
endif

.PHONY: lint clean publish install check test

help:
	@echo "\n%% nagios_aws dev tools %%"
	@echo - install: create venv and install dependencies
	@echo - update: update dependencies
	@echo - shell: activate virtual environment
	@echo - test: run tests
	@echo - export: generate requirements.txt from pyproject
	@echo - clean: remove cache and bytecode files
	@echo - lint: check code formatting
	@echo - reformat: reformat
	@echo ""

update:
	poetry update

install:
	poetry update

shell:
	poetry shell

test:
	poetry run python -m pytest

export:
	poetry export --dev -f requirements.txt > requirements.txt

clean:
	rm -rf dist .mypy_cache .pytest_cache .coverage
	find nagios_aws -type d -name __pycache__ -exec rm -rv {} +
	find nagios_aws -type f -name "*.py[co]" -delete

lint:
	poetry run mypy nagios_aws
	poetry run autoflake --recursive nagios_aws tests
	poetry run black nagios_aws tests --check

reformat:
	poetry run autoflake --in-place --recursive nagios_aws tests
	poetry run black nagios_aws tests
	poetry run isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 nagios_aws tests