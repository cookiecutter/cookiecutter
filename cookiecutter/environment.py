# -*- coding: utf-8 -*-

from jinja2 import Environment, StrictUndefined


class StrictEnvironment(Environment):
    """Jinja2 environment that raises an error when it hits a variable
    which is not defined in the context used to render a template.
    """
    def __init__(self, **kwargs):
        super(StrictEnvironment, self).__init__(
            undefined=StrictUndefined,
            **kwargs
        )
