"""Provides custom extension, exposing a ``foobar`` filter."""

from jinja2 import Environment
from jinja2.ext import Extension

from cookiecutter.utils import simple_filter


class FoobarExtension(Extension):
    """Simple jinja2 extension for cookiecutter test purposes."""

    def __init__(self, environment: Environment) -> None:
        """Foobar Extension Constructor."""
        super().__init__(environment)
        environment.filters['foobar'] = lambda v: v * 2


@simple_filter
def simplefilterextension(v: str) -> str:
    """Provide a simple function-based filter extension."""
    return v.upper()
