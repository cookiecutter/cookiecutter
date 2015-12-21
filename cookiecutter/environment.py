# -*- coding: utf-8 -*-

from jinja2 import Environment, StrictUndefined

from .exceptions import UnknownExtension


class ExtensionLoaderMixin(object):
    """Mixin that provides a sane way of loading extensions that are specified
    in a given context.

    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    """
    def __init__(self, **kwargs):
        context = kwargs.pop('context', {})
        try:
            super(ExtensionLoaderMixin, self).__init__(
                extensions=context.get('_extensions', []),
                **kwargs
            )
        except ImportError as err:
            raise UnknownExtension('Unable to load extension: {}'.format(err))


class StrictEnvironment(ExtensionLoaderMixin, Environment):
    """Jinja2 environment that raises an error when it hits a variable
    which is not defined in the context used to render a template.
    """
    def __init__(self, **kwargs):
        super(StrictEnvironment, self).__init__(
            undefined=StrictUndefined,
            **kwargs
        )
