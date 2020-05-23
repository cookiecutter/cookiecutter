# -*- coding: utf-8 -*-

"""All exceptions used in the Cookiecutter code base are defined here."""


class CookiecutterException(Exception):
    """
    Base exception class.

    All Cookiecutter-specific exceptions should subclass this class.
    """


class NonTemplatedInputDirException(CookiecutterException):
    """
    Exception for when a project's input dir is not templated.

    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """


class UnknownTemplateDirException(CookiecutterException):
    """
    Exception for ambiguous project template directory.

    Raised when Cookiecutter cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """

    # unused locally


class MissingProjectDir(CookiecutterException):
    """
    Exception for missing generated project directory.

    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """

    # unused locally


class ConfigDoesNotExistException(CookiecutterException):
    """
    Exception for missing config file.

    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """


class InvalidConfiguration(CookiecutterException):
    """
    Exception for invalid configuration file.

    Raised if the global configuration file is not valid YAML or is
    badly constructed.
    """


class UnknownRepoType(CookiecutterException):
    """
    Exception for unknown repo types.

    Raised if a repo's type cannot be determined.
    """


class VCSNotInstalled(CookiecutterException):
    """
    Exception when version control is unavailable.

    Raised if the version control system (git or hg) is not installed.
    """


class ContextDecodingException(CookiecutterException):
    """
    Exception for failed JSON decoding.

    Raised when a project's JSON context file can not be decoded.
    """


class OutputDirExistsException(CookiecutterException):
    """
    Exception for existing output directory.

    Raised when the output directory of the project exists already.
    """


class InvalidModeException(CookiecutterException):
    """
    Exception for incompatible modes.

    Raised when cookiecutter is called with both `no_input==True` and
    `replay==True` at the same time.
    """


class FailedHookException(CookiecutterException):
    """
    Exception for hook failures.

    Raised when a hook script fails.
    """


class UndefinedVariableInTemplate(CookiecutterException):
    """
    Exception for out-of-scope variables.

    Raised when a template uses a variable which is not defined in the
    context.
    """

    def __init__(self, message, error, context):
        """Exception for out-of-scope variables."""
        self.message = message
        self.error = error
        self.context = context

    def __str__(self):
        """Text representation of UndefinedVariableInTemplate."""
        return (
            "{self.message}. "
            "Error message: {self.error.message}. "
            "Context: {self.context}"
        ).format(**locals())


class UnknownExtension(CookiecutterException):
    """
    Exception for un-importable extention.

    Raised when an environment is unable to import a required extension.
    """


class RepositoryNotFound(CookiecutterException):
    """
    Exception for missing repo.

    Raised when the specified cookiecutter repository doesn't exist.
    """


class RepositoryCloneFailed(CookiecutterException):
    """
    Exception for un-cloneable repo.

    Raised when a cookiecutter template can't be cloned.
    """


class InvalidZipRepository(CookiecutterException):
    """
    Exception for bad zip repo.

    Raised when the specified cookiecutter repository isn't a valid
    Zip archive.
    """
