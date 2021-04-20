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

.PHONY: clean
clean: clean-tox clean-build clean-pyc ## Remove all file artifacts

.PHONY: lint
lint: ## Check code style
	@echo "+ $@"
	@tox -e lint

.PHONY: test
test: ## Run tests quickly with the default Python
	@echo "+ $@"
	@tox -e py

.PHONY: test-all
test-all: ## Run tests on every Python version with tox
	@echo "+ $@"
	@tox

.PHONY: coverage
coverage: ## Check code coverage quickly with the default Python
	@echo "+ $@"
	@tox -e cov-report
	@$(BROWSER) htmlcov/index.html

.PHONY: docs
docs: ## Generate Sphinx HTML documentation, including API docs
	@echo "+ $@"
	@rm -f docs/cookiecutter.rst
	@sphinx-apidoc -o docs/ cookiecutter
	@rm -f docs/modules.rst
	@$(MAKE) -C docs clean
	@$(MAKE) -C docs html
	@$(BROWSER) docs/_build/html/index.html

.PHONY: servedocs
servedocs: docs ## Rebuild docs automatically
	@echo "+ $@"
	@watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

.PHONY: submodules
submodules: ## Pull and update git submodules recursively
	@echo "+ $@"
	@git pull --recurse-submodules
	@git submodule update --init --recursive

.PHONY: release
release: clean ## Package and upload release
	@echo "+ $@"
	@python setup.py sdist bdist_wheel
	@twine upload -r $(PYPI_SERVER) dist/*

.PHONY: sdist
sdist: clean ## Build sdist distribution
	@echo "+ $@"
	@python setup.py sdist
	@ls -l dist

.PHONY: wheel
wheel: clean ## Build bdist_wheel distribution
	@echo "+ $@"
	@python setup.py bdist_wheel
	@ls -l dist

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
