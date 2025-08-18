# List all the justfile recipes
list:
    just -l

# Run all the tests for all the supported Python versions
test-all:
    uv run --python=3.9 --isolated --group test -- pytest
    uv run --python=3.10 --isolated --group test -- pytest
    uv run --python=3.11 --isolated --group test -- pytest
    uv run --python=3.12 --isolated --group test -- pytest
    uv run --python=3.13 --isolated --group test -- pytest

# lint check with ruff
lint-check:
    uv run --python=3.13 --isolated --group test -- ruff check --no-fix .    

# lint with ruff
lint:
    uv run --python=3.13 --isolated --group test -- ruff check . --fix