.. _`subdirectories`:

Organizing cookiecutter templates in subdirectories
===================================================

You can also organize one or more templates in a single repo, like this::

    https://github.com/user/repo-name.git
        └── subdirectory-name/
            ├── {{cookiecutter.project_slug}}/
            └── cookiecutter.json

And then, using the cli::

    cookiecutter https://github.com/user/repo-name.git --subdirectory="subdirectory-name"

Cookiecutter follows this high-level algorithm:
1. Copy/clone/unzip a directory into (by default) `~/.cookiecutter/`
    a. Apply transformations, for example `git checkout branch`
    a. `cookiecutter.json` must exist in `~/.cookiecutter/repo-name` else Raise.
1. Generate the context from `cookiecutter.json`
1. Generate the files given the context into the (by default) current directory
1. Delete `~/.cookiecutter/`

`--subdirectory` is a simple "transformation", in that cookiecutter now looks for
`cookiecutter.json` in `~/.cookiecutter/repo-name/subdirectory-name/`
(instead of just `~/.cookiecutter/repo-name/`)
