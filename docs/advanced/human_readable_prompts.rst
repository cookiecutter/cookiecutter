.. _human-readable-prompts:

Human readable prompts
--------------------------------

You can add human-readable prompts that will be shown to the user for each variable using the ``__prompts__`` key:


.. code-block:: json

    {
        "package_name": "my-package",
        "module_name": "{{ cookiecutter.package_name.replace('-', '_') }}",
        "package_name_stylized": "{{ cookiecutter.module_name.replace('_', ' ').capitalize() }}",
        "short_description": "A nice python package",
        "github_username": "your-org-or-username",
        "full_name": "Firstname Lastname",
        "email": "email@example.com",
        "command_line_interface": ["yes", "no"],
        "init_git": ["yes", "no"],
        "enable_pre_commit": ["yes", "no"],
        "documentation_website": ["yes", "no"],
        "black_formatting": ["yes", "no"],
        "__prompts__": {
            "package_name": "Select your package name:",
            "module_name": "Select your module name:",
            "package_name_stylized": "Stylized package name:",
            "short_description": "Short description:",
            "github_username": "GitHub username or organization:",
            "full_name": "Author full name:",
            "email": "Author email:",
            "command_line_interface": "Add CLI:",
            "init_git": "Initialize a git repository:",
            "enable_pre_commit": "Enable pre-commit:",
            "documentation_website": "Add a documentation website:",
            "black_formatting": "Enable black formatting:"
        }
    }
