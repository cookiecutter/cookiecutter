# -*- coding: utf-8 -*-

"""Provides custom extension, exposing a ``hello`` command."""

from jinja2 import nodes
from jinja2.ext import Extension


class HelloExtension(Extension):
    """Simple jinja2 extension for cookiecutter test purposes."""

    tags = set(['hello'])

    def __init__(self, environment):
        """Hello Extension Constructor."""
        super(HelloExtension, self).__init__(environment)

    def _hello(self, name):
        """Do actual tag replace when invoked by parser."""
        return 'Hello {name}!'.format(name=name)

    def parse(self, parser):
        """Work when something match `tags` variable."""
        lineno = next(parser.stream).lineno
        node = parser.parse_expression()
        call_method = self.call_method('_hello', [node], lineno=lineno)
        return nodes.Output([call_method], lineno=lineno)
