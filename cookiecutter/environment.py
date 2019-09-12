# -*- coding: utf-8 -*-

"""Jinja2 environment and extensions loading."""

import os

from jinja2 import Environment, StrictUndefined

from .exceptions import UnknownExtension


class ExtensionLoaderMixin(object):
    """Mixin providing sane loading of extensions specified in a given context.

    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    """

    def __init__(self, **kwargs):
        """Initialize the Jinja2 Environment object while loading extensions.

        Does the following:

        1. Establishes default_extensions (currently just a Time feature)
        2. Reads extensions set in the cookiecutter.json _extensions key.
        3. Attempts to load the extensions. Provides useful error if fails.
        """
        context = kwargs.get('context', {})

        default_extensions = [
            'cookiecutter.extensions.JsonifyExtension',
            'jinja2_time.TimeExtension',
        ]
        extensions = default_extensions + self._read_extensions(context)

        try:
            super(ExtensionLoaderMixin, self).__init__(
                extensions=extensions,
                **kwargs
            )
        except ImportError as err:
            raise UnknownExtension('Unable to load extension: {}'.format(err))

    def _read_extensions(self, context):
        """Return list of extensions as str to be passed on to the Jinja2 env.

        If context does not contain the relevant info, return an empty
        list instead.
        """
        try:
            extensions = context['cookiecutter']['_extensions']
        except KeyError:
            return []
        else:
            return [str(ext) for ext in extensions]

class CustomDelimiterConfigurerMixin(object):
    """Mixin to initialize the Jinja2 Environment with custom delimiters
    """
    def __init__(self, **kwargs):
        """Initialize the Jinja2 Environment with custom delimiters
        """
        context = kwargs.pop('context', {})

        kwargs.update(self._read_delimiters(context))

        super(CustomDelimiterConfigurerMixin, self).__init__(
            **kwargs
        )

    def _read_delimiters(self, context):
        """Return dict of delimiters to be used to configure the Jinja2 env.
        """
        delimiters = {}

        j2_delimiter_params = [
            'variable_start_string', 'variable_end_string',
            'block_start_string', 'block_end_string',
            'comment_start_string', 'comment_end_string'
        ]

        for param in j2_delimiter_params:
            env_key = 'J2_' + param.upper()
            delimiter = os.environ.get(env_key)
            if delimiter:
                delimiters[param] = delimiter

        return delimiters

class StrictEnvironment(ExtensionLoaderMixin, CustomDelimiterConfigurerMixin, Environment):
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
