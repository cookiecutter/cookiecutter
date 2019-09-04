Organizing cookiecutter templates in subdirectories
===================================================

You can also organize one or more templates in a single repo, like this:

    https://github.com/user/repo-name.git
        ├── subdirectory-name/
            ├── {{cookiecutter.project_slug}}/
            └── cookiecutter.json

And then, using the cli

    cookiecutter https://github.com/user/repo-name.git --subdirectory="subdirectory-name"


Cookiecutter clones the repo into `~/.cookiecutter` as usual, then `cd`s
into `subdirectory-name`, where it must find `cookiecutter.json`
