.. _`template extensions`:

Local Extensions
----------------

*New in Cookiecutter X.x*

A template may extend the Cookiecutter environment with local extensions.
These can be part of the template itself, providing it with more sophisticated custom tags and filters.

To do so, a template author must specify the required extensions in ``cookiecutter.json`` as follows:

.. code-block:: json

    {
        "project_slug": "Foobar",
        "year": "{% now 'utc', '%Y' %}",
        "_local_extensions": ["local_extensions.FoobarExtension"]
    }

This example assumes that a ``local_extensions`` folder (python module) exists in the template root.
It will contain a ``main.py`` file, containing the following (for instance):

.. code-block:: python

    # -*- coding: utf-8 -*-

    from jinja2.ext import Extension


    class FoobarExtension(Extension):
        def __init__(self, environment):
            super(FoobarExtension, self).__init__(environment)
            environment.filters['foobar'] = lambda v: v * 2

This will register the ``foobar`` filter for the template.
