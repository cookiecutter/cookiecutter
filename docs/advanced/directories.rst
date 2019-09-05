.. _directories:

Organizing cookiecutters in directories (1.7+)
---------------------------------------------------

*New in Cookiecutter 1.7*

Cookiecutter introduces the ability to organize several templates in one
repository or zip file, separating them by directories. This allows using
symlinks for general files, to edit them in one place. Here is how the
structure looks for repositories or archives with this feature enabled::

    https://github.com/user/repo-name.git
        ├── directory1-name/
        |   ├── {{cookiecutter.project_slug}}/
        |   └── cookiecutter.json
        └── directory2-name/
            ├── {{cookiecutter.project_slug}}/
            └── cookiecutter.json

To activate one of templates from subdirectory use cli with ``--directory`` option::

    cookiecutter https://github.com/user/repo-name.git --directory="directory-name"


``--directory`` is a simple "transformation", where cookiecutter looks for
``cookiecutter.json`` in ``~/.cookiecutter/repo-name/directory-name/`` instead
of just ``~/.cookiecutter/repo-name/``
