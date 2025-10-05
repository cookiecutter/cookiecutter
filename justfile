# List all the justfile recipes
list:
    just -l

# Generate Sphinx HTML documentation, including API docs
docs: 
    uv run --python=3.13 --isolated --group docs -- sphinx-build docs docs/_build
    open docs/_build/index.html

# Host the docs locally and rebuild on changes
servedocs:
    uv run --python=3.13 --isolated --group docs -- \
        sphinx-autobuild -Wa docs/ docs/_build/html --open-browser --port 9812 \
            --watch cookiecutter

# lint with ruff
lint:
    uv run --python=3.13 --isolated --group test -- ruff check . --fix

# lint check with ruff
lint-check:
    uv run --python=3.13 --isolated --group test -- ruff check --no-fix .    

# Run all the tests for all the supported Python versions
test-all:
    uv run --python=3.9 --isolated --group test -- pytest
    uv run --python=3.10 --isolated --group test -- pytest
    uv run --python=3.11 --isolated --group test -- pytest
    uv run --python=3.12 --isolated --group test -- pytest
    uv run --python=3.13 --isolated --group test -- pytest

# Run all tests with coverage
coverage:
    uv run --python=3.13 --isolated --group test -- \
        pytest --cov-report=html --cov-report=xml --cov-branch --cov-fail-under=100
