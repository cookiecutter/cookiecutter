# -*- coding: utf-8 -*-

"""
cookiecutter.exceptions
-----------------------

All exceptions used in the Cookiecutter code base are defined here.
"""


class CookiecutterException(Exception):
    """
    Base exception class.

    All Cookiecutter-specific exceptions should subclass
    this class.
    """


class NonTemplatedInputDirException(CookiecutterException):
    """
    Raised when a project's input dir is not templated.

    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """


class UnknownTemplateDirException(CookiecutterException):
    """
    Cannot determine which directory is the project template.

    Raised when Cookiecutter cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """


class MissingProjectDir(CookiecutterException):
    """
    Cannot find generated project directory.

    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """


class ConfigDoesNotExistException(CookiecutterException):
    """
    Config file not found.

    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """


class InvalidConfiguration(CookiecutterException):
    """
    Configuration is not valid.

    Raised if the global configuration file is not valid YAML or is
    badly constructed.
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
    """
    Called with both `no_input==True` and `replay==True`.

    Raised when cookiecutter is called with both `no_input==True` and
    `replay==True` at the same time.
    """


class FailedHookException(CookiecutterException):
    """Raised when a hook script fails."""


class UndefinedVariableInTemplate(CookiecutterException):
    """Variable is not defined in the context.

    Raised when a template uses a variable which is not defined in the
    context.
    """

    def __init__(self, message, error, context):
        """Initialize exception."""
        self.message = message
        self.error = error
        self.context = context

    def __str__(self):
        """Stringify error."""
        return (
            "{self.message}. "
            "Error message: {self.error.message}. "
            "Context: {self.context}"
        ).format(**locals())


class UnknownExtension(CookiecutterException):
    """Raised when an environment is unable to import a required extension."""


class RepositoryNotFound(CookiecutterException):
    """
    Repository doesn't exist.

    Raised when the specified cookiecutter repository doesn't exist.
    """


class RepositoryCloneFailed(CookiecutterException):
    """Raised when a cookiecutter template can't be cloned."""


class InvalidZipRepository(CookiecutterException):
    """
    Not a valid Zip archive.

    Raised when the specified cookiecutter repository isn't a valid
    Zip archive.
    """
