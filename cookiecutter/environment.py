# -*- coding: utf-8 -*-

from jinja2 import Environment, StrictUndefined

from .exceptions import UnknownExtension


class StrictEnvironment(Environment):
    """Jinja2 environment that raises an error when it hits a variable
    which is not defined in the context used to render a template.
    """
    def __init__(self, context, **kwargs):
        extensions = context.get('_extensions', [])

        try:
            super(StrictEnvironment, self).__init__(
                undefined=StrictUndefined,
                extensions=extensions,
                **kwargs
            )
        except ImportError as err:
            raise UnknownExtension('Unable to load extension: {}'.format(err))
