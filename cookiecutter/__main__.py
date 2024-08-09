"""
Allow cookiecutter to be executable through `python -m cookiecutter`.

Thi script facilitates the CLI for Cookiecutter, allowing users to execute the
tool directly via the `python -m cookiecutter` command.This entry point invokes
the main function from the Cookiecutter CLI module.
"""

from cookiecutter.cli import main

if __name__ == "__main__":
    main(prog_name="cookiecutter")
