.. _templates:

Templates inheritance (2.2+)
---------------------------------------------------

*New in Cookiecutter 2.2+*

Sometimes you need to extend a base template with a different
configuration to avoid nested blocks.

Cookiecutter introduces the ability to use common templates
using the power of jinja: `extends`, `include` and `super`.

Here's an example repository::

    https://github.com/user/repo-name.git
    ├── {{cookiecutter.project_slug}}/
    |   └── file.txt
    ├── templates/
    |   └── base.txt
    └── cookiecutter.json

every file in the `templates` directory will become referable inside the project itself,
and the path should be relative from the `templates` folder like ::

    # file.txt
    {% extends "base.txt" %}

    ... or ...

    # file.txt
    {% include "base.txt" %}

The template target directory defaults to `../templates`, which is a path relative to the project
directory. It's possible to override the default directory by passing
a new path in the `_inheritance_template_dir` key in cookiecutter.json.

see more on https://jinja.palletsprojects.com/en/2.11.x/templates/
