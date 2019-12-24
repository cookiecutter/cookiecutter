# -*- coding: utf-8 -*-

"""
hello_extension.

----------------
"""

from jinja2 import nodes
from jinja2.ext import Extension


class HelloExtension(Extension):
    """A hello extension based on jinja2 Extension."""

    tags = set(['hello'])

    def __init__(self, environment):
        """__init__."""
        super(HelloExtension, self).__init__(environment)

    def _hello(self, name):
        """Method greets with Hello <name>!."""
        return 'Hello {name}!'.format(name=name)

    def parse(self, parser):
        """parse."""
        lineno = next(parser.stream).lineno
        node = parser.parse_expression()
        call_method = self.call_method('_hello', [node], lineno=lineno)
        return nodes.Output([call_method], lineno=lineno)
