Hooks
=====

Cookiecutter hooks are scripts executed at specific stages during the project generation process. They are either Python or shell scripts, facilitating automated tasks like data validation, pre-processing, and post-processing. These hooks are instrumental in customizing the generated project structure and executing initial setup tasks.

Types of Hooks
--------------

+------------------+------------------------------------------+------------------------------------------+--------------------+----------+
| Hook             | Execution Timing                         | Working Directory                        | Template Variables | Version  |
+==================+==========================================+==========================================+====================+==========+
| pre_prompt       | Before any question is rendered.         | A copy of the repository directory       | No                 | 2.4.0    |
+------------------+------------------------------------------+------------------------------------------+--------------------+----------+
| pre_gen_project  | After questions, before template process.| Root of the generated project            | Yes                | 0.7.0    |
+------------------+------------------------------------------+------------------------------------------+--------------------+----------+
| post_gen_project | After the project generation.            | Root of the generated project            | Yes                | 0.7.0    |
+------------------+------------------------------------------+------------------------------------------+--------------------+----------+

Creating Hooks
--------------

Hooks are added to the ``hooks/`` folder of your template. Both Python and Shell scripts are supported.

**Python Hooks Structure:**

.. code-block::

    cookiecutter-something/
    ├── {{cookiecutter.project_slug}}/
    ├── hooks
    │   ├── pre_prompt.py
    │   ├── pre_gen_project.py
    │   └── post_gen_project.py
    └── cookiecutter.json

**Shell Scripts Structure:**

.. code-block::

    cookiecutter-something/
    ├── {{cookiecutter.project_slug}}/
    ├── hooks
    │   ├── pre_prompt.sh
    │   ├── pre_gen_project.sh
    │   └── post_gen_project.sh
    └── cookiecutter.json

Python scripts are recommended for cross-platform compatibility. However, shell scripts or `.bat` files can be used for platform-specific templates.

Hook Execution
--------------

Hooks should be robust and handle errors gracefully. If a hook exits with a nonzero status, the project generation halts, and the generated directory is cleaned.

**Working Directory:**

* ``pre_prompt``: Scripts run in the root directory of a copy of the repository directory. That allows the rewrite of ``cookiecutter.json`` to your own needs.

* ``pre_gen_project`` and ``post_gen_project``: Scripts run in the root directory of the generated project, simplifying the process of locating generated files using relative paths.

**Template Variables:**

The ``pre_gen_project`` and ``post_gen_project`` hooks support Jinja template rendering, similar to project templates. For instance:

.. code-block:: python

    module_name = '{{ cookiecutter.module_name }}'

Examples
--------

**Pre-Prompt Sanity Check:**

A ``pre_prompt`` hook, like the one below in ``hooks/pre_prompt.py``, ensures prerequisites, such as Docker, are installed before prompting the user.

.. code-block:: python

    import sys
    import subprocess

    def is_docker_installed() -> bool:
        try:
            subprocess.run(["docker", "--version"], capture_output=True, check=True)
            return True
        except Exception:
            return False

    if __name__ == "__main__":
        if not is_docker_installed():
            print("ERROR: Docker is not installed.")
            sys.exit(1)

**Validating Template Variables:**

A ``pre_gen_project`` hook can validate template variables. The following script checks if the provided module name is valid.

.. code-block:: python

    import re
    import sys

    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
    module_name = '{{ cookiecutter.module_name }}'

    if not re.match(MODULE_REGEX, module_name):
        print(f'ERROR: {module_name} is not a valid Python module name!')
        sys.exit(1)

**Conditional File/Directory Removal:**

A ``post_gen_project`` hook can conditionally control files and directories. The example below removes unnecessary files based on the selected packaging option.

.. code-block:: python

    import os

    REMOVE_PATHS = [
        '{% if cookiecutter.packaging != "pip" %}requirements.txt{% endif %}',
        '{% if cookiecutter.packaging != "poetry" %}poetry.lock{% endif %}',
    ]

    for path in REMOVE_PATHS:
        path = path.strip()
        if path and os.path.exists(path):
            os.unlink(path) if os.path.isfile(path) else os.rmdir(path)
