# -*- coding: utf-8 -*-

"""Jinja2 environment and extensions loading."""

from jinja2 import Environment, StrictUndefined

from .exceptions import UnknownExtension


class ExtensionLoaderMixin(object):
    """Mixin providing sane loading of extensions specified in a given context.

    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    """
    default_extensions = [
        'cookiecutter.extensions.JsonifyExtension',
        'jinja2_time.TimeExtension',
    ]

    def __init__(self, **kwargs):
        """Initialize the Jinja2 Environment object while loading extensions.

        Does the following:

        1. Establishes default_extensions (currently just a Time feature)
        2. Reads extensions set in the cookiecutter.json _extensions key.
        3. Attempts to load the extensions. Provides useful error if fails.
        """
        kwargs.setdefault('extensions', [])
        kwargs['extensions'] += self.default_extensions

        context = kwargs.pop('context', {}).get('cookiecutter')
        if context:
            extensions = context.get('_extensions')
            if extensions:
                kwargs['extensions'] += extensions
            environment = context.get('_environment')
            if environment:
                kwargs.update(**environment)

        try:
            super(ExtensionLoaderMixin, self).__init__(**kwargs)
        except ImportError as err:
            raise UnknownExtension('Unable to load extension: {}'.format(err))


class StrictEnvironment(ExtensionLoaderMixin, Environment):
    """Create strict Jinja2 environment.

    Jinja2 environment will raise error on undefined variable in template-
    rendering context.
    """

    def __init__(self, **kwargs):
        """Set the standard Cookiecutter StrictEnvironment.

        Also loading extensions defined in cookiecutter.json's _extensions key.
        """
        super(StrictEnvironment, self).__init__(
            undefined=StrictUndefined,
            **kwargs
        )
