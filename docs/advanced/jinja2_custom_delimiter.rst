.. _jinja2-custom-delimiter:

Jinja2 custom delimiter
-----------------------

You can specify an ``_jinja2_env_vars`` in ``cookiecutter.json`` file for change the default jinja2 delimiter ``{{``.
This is very useful when you templates contains files like:

1. Helm Chart
2. Jinja2 files

Example usages in ``cookiecutter.json``::

    "_jinja2_env_vars": {
        "block_start_string": "[%",
        "block_end_string": "%]",
        "variable_start_string": "[[",
        "variable_end_string": "]]"
    }
