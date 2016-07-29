"""Allow cookiecutter to be executable through `python -m cookiecutter`."""
from __future__ import absolute_import

from .cli import main


if __name__ == "__main__":
    main()
