.. _user-dynamic-hooks:

Using dynamic Python Hooks (1.7.0+)
======================================

You can have runtime Python function intervene before and/or after your project
is generated.

Create a file `python_gen_project.py` in `hooks/` like this::

    cookiecutter-something/
    ├── {{cookiecutter.project_slug}}/
    ├── hooks
    │   └── python_gen_project.py
    └── cookiecutter.json

This file will be left untouched (i.e. no templating will be applied) and will
be imported directly from the template directory. The import takes place
in the Python interpreter running cookiecutter.

Writing hooks
-------------

`python_gen_project.py` is a python module exposing a `pre_gen_project` and/or
a `post_gen_project` callable objects. These callables take two input
arguments:

* a string `project_dir` containing the target project directoy
* an OrderedDict `cookiecutter`, the cookiecutter context

Usually these callables are simply functions.

Example: Generating a random UUID
---------------------------------

This is an example of how to insert a new entry in the cookiecutter context.
This new entry will be available when templating files.

.. code-block:: python

    from uuid import uuid4
    def pre_gen_project(project_dir, cookiecutter):
        cookiecutter['project_uuid'] = uuid4()
