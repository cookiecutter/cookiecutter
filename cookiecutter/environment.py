# -*- coding: utf-8 -*-

"""Jinja2 environment and extensions loading."""

from jinja2 import Environment, StrictUndefined
from jinja2.utils import import_string

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
        context = kwargs.pop('context', {})

        default_extensions = [
            'jinja2_time.TimeExtension',
        ]
        function_extensions = [
            'cookiecutter.extensions.jsonify_extension',
        ]
        extensions = default_extensions + self._read_extensions(context) + \
            self._load_extension_functions(function_extensions)

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

    def _load_extension_functions(self, extension_strs):
        """Load custom extensions that have been written as functions.

        At runtime, this imports the relevant extension and sets an
        identifier attribute which is required by to be run by jinja2
        via the load_extensions function

        Returns list of loaded extensions.
        """
        extensions = []
        for extension_str in extension_strs:
            extension = import_string(extension_str)
            setattr(extension, 'identifier', extension_str)
            extensions.append(extension)
        return extensions


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
