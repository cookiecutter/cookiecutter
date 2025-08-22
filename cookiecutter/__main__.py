"""
Allow Cookiecutter to be executable through `python -m cookiecutter`.

This script allows the Cookiecutter CLI to be invoked directly using the
`python -m cookiecutter` command.
"""

from cookiecutter.cli import main

if __name__ == "__main__":
    main(prog_name="cookiecutter")
