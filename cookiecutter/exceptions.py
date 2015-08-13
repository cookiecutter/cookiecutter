#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.exceptions
-----------------------

All exceptions used in the Cookiecutter code base are defined here.
"""


class CookiecutterException(Exception):
    """
    Base exception class. All Cookiecutter-specific exceptions should subclass
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
    Raised when Cookiecutter cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """


class MissingProjectDir(CookiecutterException):
    """
    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """


class ConfigDoesNotExistException(CookiecutterException):
    """
    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """


class InvalidConfiguration(CookiecutterException):
    """
    Raised if the global configuration file is not valid YAML or is
    badly contructed.
    """


class UnknownRepoType(CookiecutterException):
    """
    Raised if a repo's type cannot be determined.
    """


class VCSNotInstalled(CookiecutterException):
    """
    Raised if the version control system (git or hg) is not installed.
    """


class ContextDecodingException(CookiecutterException):
    """
    Raised when a project's JSON context file can not be decoded.
    """


class OutputDirExistsException(CookiecutterException):
    """
    Raised when the output directory of the project exists already.
    """


class InvalidModeException(CookiecutterException):
    """
    Raised when cookiecutter is called with both `no_input==True` and
    `replay==True` at the same time.
    """
