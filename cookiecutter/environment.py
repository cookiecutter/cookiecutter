"""Jinja2 environment and extensions loading."""

from __future__ import annotations

from typing import Any

from jinja2 import Environment, StrictUndefined

from cookiecutter.exceptions import UnknownExtension


DEFAULT_EXTENSIONS = [
    'cookiecutter.extensions.JsonifyExtension',
    'cookiecutter.extensions.RandomStringExtension',
    'cookiecutter.extensions.SlugifyExtension',
    'cookiecutter.extensions.TimeExtension',
    'cookiecutter.extensions.UUIDExtension',
]


def read_extensions(context: dict[str, Any]) -> list[str]:
    """Read and return list of Jinja2 extensions from the given context.

    Extracts the ``_extensions`` key from the cookiecutter context dict.
    If context does not contain the relevant info, return an empty
    list instead.

    :param context: cookiecutter context dict containing project configuration.
    :returns: List of extension strings to be passed to the Jinja2 environment.
    """
    try:
        extensions = context['cookiecutter']['_extensions']
    except KeyError:
        return []
    else:
        return [str(ext) for ext in extensions]


class ExtensionLoaderMixin:
    """Mixin providing sane loading of extensions specified in a given context.

    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    """

    def __init__(self, *, context: dict[str, Any] | None = None, **kwargs: Any) -> None:
        """Initialize the Jinja2 Environment object while loading extensions.

        Does the following:

        1. Establishes default_extensions (currently just a Time feature)
        2. Reads extensions set in the cookiecutter.json _extensions key.
        3. Attempts to load the extensions. Provides useful error if fails.
        """
        context = context or {}

        # Use the module-level read_extensions function instead of instance method
        extensions = DEFAULT_EXTENSIONS + read_extensions(context)

        try:
            super().__init__(extensions=extensions, **kwargs)  # type: ignore[call-arg]
        except ImportError as err:
            msg = f'Unable to load extension: {err}'
            raise UnknownExtension(msg) from err


class StrictEnvironment(ExtensionLoaderMixin, Environment):
    """Create strict Jinja2 environment.

    Jinja2 environment will raise error on undefined variable in template-
    rendering context.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Set the standard Cookiecutter StrictEnvironment.

        Also loading extensions defined in cookiecutter.json's _extensions key.
        """
        super().__init__(undefined=StrictUndefined, **kwargs)