=====
Hooks
=====

Using Pre/Post-Generate Hooks (0.7.0+)
--------------------------------------

You can have Python or Shell scripts that run before and/or after your project
is generated.

Put them in `hooks/` like this::

    cookiecutter-something/
    ├── {{cookiecutter.repo_name}}/
    ├── hooks
    │   ├── pre_gen_project.py
    │   └── post_gen_project.py
    └── cookiecutter.json

Shell scripts work similarly::

    cookiecutter-something/
    ├── {{cookiecutter.repo_name}}/
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

By default, hooks are duplicated in a temporary file and the template is directly applied in this ephemeral file. This allows you to use template variables directly within your hook, as shown in `Example: Validating template variables`_ below.

The cookiecutter context object is serialized and passed to your hook through the standard input stream. You can then modify some configuration settings and send them back to the main context by writing to the standard output stream.

.. note::
  JSON is currently used as the serialization format by default.
  Only the last JSON object sent through the standard output will be taken into account.

Sometimes, when using template variables in hook is not needed, it may be preferable to run your real hook file in place.
To do this, you simply have to add the key ``_run_hook_in_place`` with the value ``true`` in your configuration cookiecutter.json, as shown in `Running hooks in place and consuming serialized context`_.

.. note::
  Only the value: ``true`` will run hooks in place and then disable hooks duplication. Every other values or the absence of the ``_run_hook_in_place`` key will result in the default behaviour.

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

.. _`running hooks in place`:

Running hooks in place and consuming serialized context
-------------------------------------------------------

Disabling hook duplication
~~~~~~~~~~~~~~~~~~~~~~~~~~
As explained in `Using Pre/Post-Generate Hooks (0.7.0+)`_, you can disable the default behaviour of hook duplication. This is interesting when you don't need to use template variables directly in your hook.

To do so, a template author must specify this wish in ``cookiecutter.json`` as follows:

.. code-block:: json

    {
        "_run_hook_in_place": "true"
    }

Using serialized context
~~~~~~~~~~~~~~~~~~~~~~~~
Given the ``cookiecutter.json``

.. code-block:: json

    {
        "project_name": "Cookiecutter example project",
        "project_slug": "{{ cookiecutter.project_name }}"
    }

Here follows an example on how to take advantage of the context serialization in ``hooks/pre_gen_project.py``

.. code-block:: python

  #!/usr/bin/env python
  # -*- coding: utf-8 -*-
  import sys
  import json
  import re
  
  # get the serialized context from the standard input
  context = json.loads(sys.stdin.readlines()[0])
  
  # remove 'project' word used in project_name from project_slug
  context['project_slug'] = re.sub(
    r'project', '', context['project_slug'], 1, flags=re.I
  )

  # serialize the updated context and send this modification through the standard output 
  print(json.dumps(context))