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

Writing hooks
-------------

Here are some details on how to write pre/post-generate hook scripts.

Exit with an appropriate status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure your hook scripts work in a robust manner. If a hook script fails
(that is, `if it finishes with a nonzero exit status
<https://docs.python.org/3/library/sys.html#sys.exit>`_), the project
generation will stop and the generated directory will be cleaned up.

Current working directory
^^^^^^^^^^^^^^^^^^^^^^^^^

When the hook scripts script are run, their current working directory is the
root of the generated project. This makes it easy for a post-generate hook to
find generated files using relative paths.

Template variables are rendered in the script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just like your project template, Cookiecutter also renders Jinja template
syntax in your scripts. This lets you incorporate Jinja template variables in
your scripts. For example, this line of Python sets ``module_name`` to the
value of the ``cookiecutter.module_name`` template variable:

.. code-block:: python

    module_name = '{{ cookiecutter.module_name }}'

Example: Validating template variables
--------------------------------------

Here is an example of a pre-generate hook script, defined at
``hooks/pre_gen_project.py``, that validates a template variable before generating the
project:

.. code-block:: python

    import re
    import sys


    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

    module_name = '{{ cookiecutter.module_name }}'

    if not re.match(MODULE_REGEX, module_name):
        print('ERROR: %s is not a valid Python module name!' % module_name)

        # exits with status 1 to indicate failure
        sys.exit(1)

Example: Conditional files / directories
----------------------------------------

Here is an example of a post-generate hook script, defined at
``hooks/post_gen_project.py``, on how to achieve conditional control of files and
directories after generating the project.

The script ensures that the directory structure is as expected by
removing unwanted files and directories:

.. code-block:: python

   import os
   import sys

   REMOVE_PATHS = [
       '{% if cookiecutter.packaging != "pip" %} requirements.txt {% endif %}',
       '{% if cookiecutter.packaging != "poetry" %} poetry.lock {% endif %}',
   ]

   for path in REMOVE_PATHS:
       path = path.strip()
       if path and os.path.exists(path):
           if os.path.isdir(path):
               os.rmdir(path)
           else:
               os.unlink(path)
