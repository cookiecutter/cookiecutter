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
    uv run --python=3.13 --isolated --group lint -- ruff check . --fix

# lint check with ruff
lint-check:
    uv run --python=3.13 --isolated --group lint -- ruff check --no-fix .

# Run all the tests for all the supported Python versions
test-all:
    uv run --python=3.10 --isolated --group test -- pytest
    uv run --python=3.11 --isolated --group test -- pytest
    uv run --python=3.12 --isolated --group test -- pytest
    uv run --python=3.13 --isolated --group test -- pytest
    uv run --python=3.14 --isolated --group test -- pytest

VERSION := `grep -m1 '^version' pyproject.toml | sed -E 's/version = "(.*)"/\1/'`

# Print the current version of the project
version:
    @echo "Current version is {{VERSION}}"

# Tag the current version and push to GitHub
tag:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ "$(git branch --show-current)" != "main" ]; then
        echo "Error: not on main branch" >&2
        exit 1
    fi
    if [ -n "$(git status --porcelain)" ]; then
        echo "Error: working tree is not clean" >&2
        exit 1
    fi
    if [ ! -f "CHANGELOG/{{VERSION}}.md" ]; then
        echo "Error: CHANGELOG/{{VERSION}}.md not found" >&2
        exit 1
    fi
    echo "Tagging v{{VERSION}}"
    git tag -a v{{VERSION}} -m "Release {{VERSION}}"
    git push origin main
    git push origin v{{VERSION}}

# Run all tests with coverage
coverage:
    uv run --python=3.13 --isolated --group test -- \
        pytest --cov-report=html --cov-report=xml --cov-branch --cov-fail-under=100
