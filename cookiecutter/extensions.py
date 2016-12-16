# -*- coding: utf-8 -*-

"""Jinja2 extensions."""

import json

from jinja2.ext import Extension


class JsonifyExtension(Extension):
    """Jinja2 extension to convert a python object to json"""

    def __init__(self, environment):
        super(JsonifyExtension, self).__init__(environment)

        def jsonify(obj):
            return json.dumps(obj, sort_keys=True, indent=4)

        environment.filters['jsonify'] = jsonify
