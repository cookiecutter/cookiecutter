.. _human-readable-prompts:

Human readable prompts
--------------------------------

You can add human-readable prompts that will be shown to the user for each variable using the ``__prompts__`` key.
For multiple choices questions you can also provide labels for each option.

See the following cookiecutter config as example:


.. code-block:: json

    {
        "package_name": "my-package",
        "module_name": "{{ cookiecutter.package_name.replace('-', '_') }}",
        "package_name_stylized": "{{ cookiecutter.module_name.replace('_', ' ').capitalize() }}",
        "short_description": "A nice python package",
        "github_username": "your-org-or-username",
        "full_name": "Firstname Lastname",
        "email": "email@example.com",
        "init_git": true,
        "linting": ["ruff", "flake8", "none"],
        "__prompts__": {
            "package_name": "Select your package name",
            "module_name": "Select your module name",
            "package_name_stylized": "Stylized package name",
            "short_description": "Short description",
            "github_username": "GitHub username or organization",
            "full_name": "Author full name",
            "email": "Author email",
            "command_line_interface": "Add CLI",
            "init_git": "Initialize a git repository",
            "linting": {
                "__prompt__": "Which linting tool do you want to use?",
                "ruff": "Ruff",
                "flake8": "Flake8",
                "none": "No linting tool"
            }
        }
    }
