"""
Main package for Cookiecutter.

This module initializes the package and retrieves the version information from
the VERSION.txt file.
"""

from pathlib import Path


def _get_version() -> str:
    """Read VERSION.txt and return its contents."""
    path = Path(__file__).parent.resolve()
    version_file = path / "VERSION.txt"
    return version_file.read_text(encoding="utf-8").strip()


__version__ = _get_version()
