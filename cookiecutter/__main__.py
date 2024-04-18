"""Allow cookiecutter to be executable through `python -m cookiecutter`."""

from cookiecutter.cli import main

if __name__ == "__main__":
    main(prog_name="cookiecutter")
