# List all the justfile recipes
list:
    just -l

# Run all the tests for all the supported Python versions
test-all:
    uv run --python=3.8 --isolated --group test -- pytest
    uv run --python=3.9 --isolated --group test -- pytest
    uv run --python=3.10 --isolated --group test -- pytest
    uv run --python=3.11 --isolated --group test -- pytest
    uv run --python=3.12 --isolated --group test -- pytest

# lint with ruff
lint:
    uv run --python=3.12 --isolated --group test -- ruff check --no-fix .    