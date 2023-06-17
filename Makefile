PYPI_SERVER = pypitest

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

.DEFAULT_GOAL := help


.PHONY: clean-tox
clean-tox: ## Remove tox testing artifacts
	@echo "+ $@"
	@rm -rf .tox/

.PHONY: clean-coverage
clean-coverage: ## Remove coverage reports
	@echo "+ $@"
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf coverage.xml

.PHONY: clean-pytest
clean-pytest: ## Remove pytest cache
	@echo "+ $@"
	@rm -rf .pytest_cache/

.PHONY: clean-docs-build
clean-docs-build: ## Remove local docs
	@echo "+ $@"
	@rm -rf docs/_build

.PHONY: clean-build
clean-build: ## Remove build artifacts
	@echo "+ $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean ## Remove all file artifacts
clean: clean-build clean-pyc clean-tox clean-coverage clean-pytest clean-docs-build

.PHONY: lint
lint: ## Check code style
	@echo "+ $@"
	@tox -e lint

.PHONY: test
test: ## Run tests quickly with the default Python
	@echo "+ $@"
	@tox -e py310

.PHONY: test-all
test-all: ## Run tests on every Python version
	@echo "+ $@"
	@tox

.PHONY: coverage
coverage: ## Check code coverage quickly with the default Python
	@echo "+ $@"
	@tox -e py310
	@$(BROWSER) htmlcov/index.html

.PHONY: docs
docs: ## Generate Sphinx HTML documentation, including API docs
	@echo "+ $@"
	@tox -e docs
	@$(BROWSER) docs/_build/html/index.html

.PHONY: servedocs
servedocs: ## Rebuild docs automatically
	@echo "+ $@"
	@tox -e servedocs

.PHONY: submodules
submodules: ## Pull and update git submodules recursively
	@echo "+ $@"
	@git pull --recurse-submodules
	@git submodule update --init --recursive

.PHONY: release
release: clean ## Package and upload release
	@echo "+ $@"
	@python -m build
	@twine upload -r $(PYPI_SERVER) dist/*

.PHONY: sdist
sdist: clean ## Build sdist distribution
	@echo "+ $@"
	@python -m build --sdist
	@ls -l dist

.PHONY: wheel
wheel: clean ## Build wheel distribution
	@echo "+ $@"
	@python -m build --wheel
	@ls -l dist

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
