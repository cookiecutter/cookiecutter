# -*- coding: utf-8 -*-

"""Jinja2 extensions."""

from jinja2.ext import Extension

from cookiecutter.utils import jsonify


def jsonify_extension(environment):
    """Jinja2 extension to convert a Python object to JSON."""
    environment.filters['jsonify'] = jsonify
    extension = Extension(environment)
    return extension
