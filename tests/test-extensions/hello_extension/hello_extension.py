"""Provides custom extension, exposing a ``hello`` command."""

from jinja2 import Environment, nodes
from jinja2.ext import Extension
from jinja2.parser import Parser


class HelloExtension(Extension):
    """Simple jinja2 extension for cookiecutter test purposes."""

    tags = {'hello'}

    def __init__(self, environment: Environment) -> None:
        """Hello Extension Constructor."""
        super().__init__(environment)

    def _hello(self, name: str) -> str:
        """Do actual tag replace when invoked by parser."""
        return f'Hello {name}!'

    def parse(self, parser: Parser) -> nodes.Output:
        """Work when something match `tags` variable."""
        lineno = next(parser.stream).lineno
        node = parser.parse_expression()
        call_method = self.call_method('_hello', [node], lineno=lineno)
        return nodes.Output([call_method], lineno=lineno)
