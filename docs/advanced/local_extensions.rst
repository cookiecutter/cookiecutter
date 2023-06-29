.. _`local extensions`:

Local Extensions
----------------

*New in Cookiecutter 2.1*

A template may extend the Cookiecutter environment with local extensions.
These can be part of the template itself, providing it with more sophisticated custom tags and filters.

To do so, a template author must specify the required extensions in ``cookiecutter.json`` as follows:

.. code-block:: json

    {
        "project_slug": "Foobar",
        "year": "{% now 'utc', '%Y' %}",
        "_extensions": ["local_extensions.FoobarExtension"]
    }

This example uses a simple module ``local_extensions.py`` which exists in the template root, containing the following (for instance):

.. code-block:: python

    from jinja2.ext import Extension


    class FoobarExtension(Extension):
        def __init__(self, environment):
            super(FoobarExtension, self).__init__(environment)
            environment.filters['foobar'] = lambda v: v * 2

This will register the ``foobar`` filter for the template.

For many cases, this will be unnecessarily complicated.
It's likely that we'd only want to register a single function as a filter. For this, we can use the ``simple_filter`` decorator:

.. code-block:: json

    {
        "project_slug": "Foobar",
        "year": "{% now 'utc', '%Y' %}",
        "_extensions": ["local_extensions.simplefilterextension"]
    }

.. code-block:: python

    from cookiecutter.utils import simple_filter


    @simple_filter
    def simplefilterextension(v):
        return v * 2

This snippet will achieve the exact same result as the previous one.

For complex use cases, a python module ``local_extensions`` (a folder with an ``__init__.py``) can also be created in the template root.
Here, for example, a module ``main.py`` would have to export all extensions with ``from .main import FoobarExtension, simplefilterextension`` or ``from .main import *`` in the ``__init__.py``.
