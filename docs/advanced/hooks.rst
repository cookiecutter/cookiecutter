.. _user-hooks:

Using Pre/Post-Generate Hooks (0.7.0+)
======================================

You can have Python or Shell scripts that run before and/or after your project
is generated.

Put them in `hooks/` like this::

    cookiecutter-something/
    ├── {{cookiecutter.project_slug}}/
    ├── hooks
    │   ├── pre_gen_project.py
    │   └── post_gen_project.py
    └── cookiecutter.json

Shell scripts work similarly::

    cookiecutter-something/
    ├── {{cookiecutter.project_slug}}/
    ├── hooks
    │   ├── pre_gen_project.sh
    │   └── post_gen_project.sh
    └── cookiecutter.json

It shouldn't be too hard to extend Cookiecutter to work with other types of
scripts too. Pull requests are welcome.

For portability, you should use Python scripts (with extension `.py`) for your
hooks, as these can be run on any platform. However, if you intend for your
template to only be run on a single platform, a shell script (or `.bat` file
on Windows) can be a quicker alternative.

.. note::
    Make sure your hook scripts work in a robust manner. If a hook script fails
    (that is, `if it finishes with a nonzero exit status
    <https://docs.python.org/3/library/sys.html#sys.exit>`_), the project
    generation will stop and the generated directory will be cleaned up.

Example: Validating template variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is an example of script that validates a template variable
before generating the project, to be used as ``hooks/pre_gen_project.py``:

.. code-block:: python

    import re
    import sys


    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

    module_name = '{{ cookiecutter.module_name }}'

    if not re.match(MODULE_REGEX, module_name):
        print('ERROR: %s is not a valid Python module name!' % module_name)

        # exits with status 1 to indicate failure
        sys.exit(1)
