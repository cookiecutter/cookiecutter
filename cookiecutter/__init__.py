"""Main package for Cookiecutter."""

import importlib.resources


def _get_version() -> str:
    """Read VERSION.txt and return its contents."""

    return (
        importlib.resources.read_text(__package__, 'VERSION.txt').strip()
        if importlib.resources.is_resource(__package__, 'VERSION.txt')
        else 'unknown'
    )


__version__ = _get_version()
