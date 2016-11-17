# -*- coding: utf-8 -*-
"""Allow cookiecutter to be executable through `python -m cookiecutter`."""
from __future__ import absolute_import

from .cli import main


if __name__ == "__main__":  # pragma: no cover
    main(prog_name="cookiecutter")
