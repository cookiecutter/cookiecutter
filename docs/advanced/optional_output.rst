.. _optional-output:

Optional files
--------------

Individual files can be removed from the output by
using a filename that expands to an empty string.

For example:

.. code-block:: JSON

    {
        "packaging": ["pip", "poetry"],
        "__requirements": "{% if cookiecutter.packaging == "pip" %}requirements.txt{% endif %}",
        "__poetry_lock": "{% if cookiecutter.packaging == "poetry" %}poetry.lock{% endif %}",
    }

With file layout
.. code-block::

    cookiecutter-something/
    ├── {{cookiecutter.project_slug}}/
    │   ├── {{cookiecutter.__requirements}}
    │   └── {{cookiecutter.__poetry_lock}}
    └── cookiecutter.json

Then only the appropriate output file is included in output.

Optional directories
--------------------

A similar approach works for entire directories.
If a directory name template expands to an empty
string it and all contained files and directories
are removed. For example:

.. code-block:: JSON

    {
        "docker": true,
        "packaging": ["pip", "poetry"],
        "__requirements": "{% if cookiecutter.packaging == "pip" %}requirements.txt{% endif %}",
        "__poetry_lock": "{% if cookiecutter.packaging == "poetry" %}poetry.lock{% endif %}",
    }

With file layout
.. code-block::

    cookiecutter-something/
    ├── {{cookiecutter.project_slug}}/
    │   ├── {% if cookiecutter.docker %}docker{% endif %}
    │   │   ├── Dockerfile
    │   │   └── install.sh
    │   ├── {{cookiecutter.__requirements}}
    │   └── {{cookiecutter.__poetry_lock}}
    └── cookiecutter.json

A user can remove all docker related files with a single option.
This also shows using conditionals directly in the file path.
