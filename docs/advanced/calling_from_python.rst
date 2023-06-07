.. _calling-from-python:

Calling Cookiecutter Functions From Python
------------------------------------------

You can use Cookiecutter from Python:

.. code-block:: python

    from cookiecutter.main import cookiecutter

    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyfeldroy/cookiecutter-pypackage.git')

This is useful if, for example, you're writing a web framework and need to provide developers with a tool similar to `django-admin.py startproject` or `npm init`.

See the :ref:`API Reference <apiref>` for more details.
