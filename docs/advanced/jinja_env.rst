.. _jinja-env:

Customizing the Jinja2 environment
----------------------------------------------

The special template variable ``_jinja2_env_vars`` can be used
to customize the [Jinja2 environment](https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment).

This example shows how to control whitespace with ``lstrip_blocks`` and ``trim_blocks``:

.. code-block:: JSON

    {
        "project_slug": "sample",
        "_jinja2_env_vars": {"lstrip_blocks": true, "trim_blocks": true}
    }
