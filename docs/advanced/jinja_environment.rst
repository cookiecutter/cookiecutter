.. _`Jinja Environment`:

Jinja Environment
-------------------

A template may extend the Cookiecutter environment with custom arguments,
that can change the parser behaviour.

To do so, a template author must specify the custom arguments in ``cookiecutter.json`` as follows:

.. code-block:: json

    {
        "_environment": {
            "variable_start_string": "[[",
            "variable_end_string": "]]"
        }
    }

.. _`Jinja2 environment`: http://jinja.pocoo.org/docs/latest/api/#high-level-api