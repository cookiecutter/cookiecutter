# -*- coding: utf-8 -*-

"""Provides custom extension, exposing a ``foobar`` filter."""

from jinja2.ext import Extension


class FoobarExtension(Extension):
    """Simple jinja2 extension for cookiecutter test purposes."""

    def __init__(self, environment):
        """Foobar Extension Constructor."""
        super(FoobarExtension, self).__init__(environment)
        environment.filters['foobar'] = lambda v: v * 2
