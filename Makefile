.PHONY: clean clean-build clean-pyc clean-test lint format typecheck test coverage docs help install

.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-20s %s\n", $$1, $$2}'

clean: clean-build clean-pyc clean-test ## Remove all build, test, coverage and Python artifacts

clean-build: ## Remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## Remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
	rm -fr .ruff_cache

lint: ## Check style with ruff
	ruff check step_motor_28byj_48 tests

format: ## Format code with ruff
	ruff format step_motor_28byj_48 tests

typecheck: ## Run mypy type checking
	mypy --strict step_motor_28byj_48

test: ## Run tests with pytest
	pytest

coverage: ## Run tests with coverage
	pytest --cov=step_motor_28byj_48 --cov-report=term-missing --cov-fail-under=90

docs: ## Generate Sphinx HTML documentation
	rm -f docs/step_motor_28byj_48.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ step_motor_28byj_48
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

install: clean ## Install the package in development mode
	pip install -e ".[dev]"
