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
    """Raised when Cookiecutter cannot determine template directory.

    For example when more than one dir appears to be a template dir.
    """


class MissingProjectDir(CookiecutterException):
    """Raised when Cookiecutter can't find a generated project directory.

    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """


class ConfigDoesNotExistException(CookiecutterException):
    """Raised when config file is not found.

    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """


class InvalidConfiguration(CookiecutterException):
    """Raised if the global configuration file is invalid.

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
    """Raised when cookiecutter is called with invalid mode.

    Raised when cookiecutter is called with both `no_input==True` and
    `replay==True` at the same time.
    """


class FailedHookException(CookiecutterException):
    """Raised when a hook script fails."""


class UndefinedVariableInTemplate(CookiecutterException):
    """Raised for undefined variable in template.

    Raised when a template uses a variable which is not defined in the
    context.
    """

    def __init__(self, message, error, context):
        """Initiaize the exception."""
        self.message = message
        self.error = error
        self.context = context

    def __str__(self):
        """Return string representation of the exception.

        The representation consists of message, message from the error object
        and context.
        """
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


class InvalidZipRepository(CookiecutterException):
    """Raised or invalid zip repositories.

    Raised when the specified cookiecutter repository isn't a valid
    Zip archive.
    """
