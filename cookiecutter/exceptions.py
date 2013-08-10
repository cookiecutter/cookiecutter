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
