.. _jinja2-custom-delimiter:

Jinja2 custom delimiter
-----------------------

You can specify a dictionary under the ``_jinja2_env_vars`` key in the ``cookiecutter.json`` file to modify the default jinja2 delimiter (``{{``).
This is very useful for templates which contain files that have expressions with that use the default delimiters ``{{ ... }}``  such as:

1. Helm Charts
2. Jinja2 files

Example usages in ``cookiecutter.json``::

    "_jinja2_env_vars": {
        "block_start_string": "[%",
        "block_end_string": "%]",
        "variable_start_string": "[[",
        "variable_end_string": "]]"
    }
