#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""All exceptions used in the Cookiecutter code base are defined here."""


class CookiecutterException(Exception):
    """Base exception class.

    All Cookiecutter-specific exceptions should subclass this class.
    """


class NonTemplatedInputDirException(CookiecutterException):
    """Raised when a project's input dir is not templated.

    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """


class UnknownTemplateDirException(CookiecutterException):
    """Raised when the project template directory cannot be determined.

    More than one dir appears to be a template dir.
    """


class MissingProjectDir(CookiecutterException):
    """Raised during cleanup stages when project directory appears missing.

    When remove_repo() cannot locate the generated project directory.
    """


class ConfigDoesNotExistException(CookiecutterException):
    """Raised when get_config() is passed a invalid config file path."""


class InvalidConfiguration(CookiecutterException):
    """Raised if the global configuration file is not valid.

    Invalid YAML or the configuration file is badly constructed.
    """


class UnknownRepoType(CookiecutterException):
    """Raised if a repo's type cannot be determined."""


class VCSNotInstalled(CookiecutterException):
    """Raised if the version control system (git or hg) is not installed."""


class ContextDecodingException(CookiecutterException):
    """Raised when a project's JSON context file can not be decoded."""


class OutputDirExistsException(CookiecutterException):
    """Raised when the output directory of the project exists already."""


class InvalidModeException(CookiecutterException):
    """Raised when `no_input==True` and `replay==True` used at same time."""


class FailedHookException(CookiecutterException):
    """Raised when a hook script fails."""


class UndefinedVariableInTemplate(CookiecutterException):
    """Raised when template uses an undefined variable in the context."""

    def __init__(self, message, error, context):
        """Initialize instance of UndefinedVariableInTemplate class.

        :param message: Detailed error message.
        :param error: Exception raised by the undefined variable.
        :param context: Dict for populating the template's variables.

        """
        self.message = message
        self.error = error
        self.context = context

    def __str__(self):
        """Create informal string representation of object."""
        return (
            "{self.message}. "
            "Error message: {self.error.message}. "
            "Context: {self.context}"
        ).format(**locals())


class UnknownExtension(CookiecutterException):
    """Raised when an environment is unable to import a required extension."""


class RepositoryNotFound(CookiecutterException):
    """Raised when the specified cookiecutter repository doesn't exist."""


class RepositoryCloneFailed(CookiecutterException):
    """Raised when a cookiecutter template can't be cloned."""
