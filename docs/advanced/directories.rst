.. _directories:

Organizing cookiecutters in directories
---------------------------------------

*New in Cookiecutter 1.7*

Cookiecutter introduces the ability to organize several templates in one repository or zip file, separating them by directories.
This allows using symlinks to share files between templates.
Here's an example repository demonstrating this feature::

    https://github.com/user/repo-name.git
        ├── directory1-name/
        |   ├── {{cookiecutter.project_slug}}/
        |   └── cookiecutter.json
        └── directory2-name/
            ├── {{cookiecutter.project_slug}}/
            └── cookiecutter.json

To activate one of templates within a subdirectory, use the ``--directory`` option:

.. code-block:: bash

    cookiecutter https://github.com/user/repo-name.git --directory="directory1-name"

Sharing files with symbolic links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a system that supports symbolic links, a template file can link to a shared
file elsewhere in the repository. For example::

    repo-name/
        ├── shared/
        │   └── README.md
        ├── directory1-name/
        │   ├── {{cookiecutter.project_slug}}/
        │   │   └── README.md -> ../../shared/README.md
        │   └── cookiecutter.json
        └── directory2-name/
            ├── {{cookiecutter.project_slug}}/
            │   └── README.md -> ../../shared/README.md
            └── cookiecutter.json

Both links refer to the same source file. Its contents can include template
variables, such as ``{{ cookiecutter.project_slug }}``, which are rendered using
the context of the selected template.

Cookiecutter follows file links when reading their contents. The generated
``README.md`` is a regular file containing the rendered text, not a symbolic
link. Files matched by :ref:`copy-without-render` are also copied as regular
files, but their contents are not rendered.

.. note::

    During template rendering, Cookiecutter does not traverse symbolic links to
    directories. A linked directory is created as an empty directory in the
    generated project. Use links to individual files when sharing rendered
    content. A directory matched by :ref:`copy-without-render` is copied with its
    contents instead, following its links without rendering them.

    If the template has a ``pre_prompt`` hook, Cookiecutter first makes a
    temporary copy of the template, following both file and directory links.
    In that copy, the linked directories are regular directories and their
    contents can be rendered normally.

Creating symbolic links in the generated project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the generated project needs a symbolic link, create it in a
:doc:`post-generate hook <hooks>`, after the target file has been generated.
For example, save the following as ``hooks/post_gen_project.py``:

.. code-block:: python

    from pathlib import Path

    Path("README-link.md").symlink_to("README.md")

The hook runs in the root of the generated project, so this creates a relative
link to that project's ``README.md``. The link continues to work when the
project directory is moved. Creating links requires operating system support
and permission; on Windows, this may require Developer Mode or administrator
privileges.
