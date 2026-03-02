<h1 align="center">
    <img alt="cookiecutter Logo" width="200px" src="https://raw.githubusercontent.com/cookiecutter/cookiecutter/main/logo/cookiecutter_medium.png">
</h1>

<div align="center">

[![pypi](https://img.shields.io/pypi/v/cookiecutter.svg)](https://pypi.org/project/cookiecutter/)
[![python](https://img.shields.io/pypi/pyversions/cookiecutter.svg)](https://pypi.org/project/cookiecutter/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/cookiecutter?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/cookiecutter)
[![GitHub Stars](https://img.shields.io/github/stars/cookiecutter/cookiecutter?style=flat&logo=github&label=stars)](https://github.com/cookiecutter/cookiecutter)
[![discord](https://img.shields.io/badge/Discord-cookiecutter-5865F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/9BrxzPKuEW)
[![docs](https://readthedocs.org/projects/cookiecutter/badge/?version=latest)](https://readthedocs.org/projects/cookiecutter/?badge=latest)

</div>

# Cookiecutter

Create projects swiftly from **cookiecutters** (project templates) with this command-line utility. Ideal for generating Python package projects and more.

- [Documentation](https://cookiecutter.readthedocs.io)
- [GitHub](https://github.com/cookiecutter/cookiecutter)
- [PyPI](https://pypi.org/project/cookiecutter/)
- [License (BSD)](https://github.com/cookiecutter/cookiecutter/blob/main/LICENSE)

## Installation

Install Cookiecutter as a CLI tool with [uv](https://docs.astral.sh/uv/):
```
uv tool install cookiecutter
```

## Features

- **Cross-Platform:** Supports Windows, Mac, and Linux.
- **User-Friendly:** No Python knowledge required.
- **Versatile:** Compatible with Python 3.10 to 3.14.
- **Multi-Language Support:** Use templates in any language or markup format.

### For Users

#### Quickstart

The most common way to use Cookiecutter is as a command line utility with a GitHub-hosted Cookiecutter template such as https://github.com/audreyfeldroy/cookiecutter-pypackage

**Use a GitHub-hosted Cookiecutter template**

```bash
# You'll be prompted to enter values.
# Then it'll create your Python package in the current working directory,
# based on those values.
# For the sake of brevity, repos on GitHub can just use the 'gh' prefix
$ uvx cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
```

**Use a local template**

```bash
$ uvx cookiecutter cookiecutter-pypackage/
```

**Use it from Python**

If you plan to use Cookiecutter programmatically, please run `uv add cookiecutter` to add it to your project. Then you can import and use it like this:

```py
from cookiecutter.main import cookiecutter

# Create project from the cookiecutter-pypackage/ template
cookiecutter('cookiecutter-pypackage/')

# Create project from the cookiecutter-pypackage.git repo template
cookiecutter('gh:audreyfeldroy/cookiecutter-pypackage')
```

> If Cookiecutter saves you time, [star it on GitHub](https://github.com/cookiecutter/cookiecutter) so other developers can find it too.

#### Detailed Usage

- Generate projects from local or remote templates.
- Customize projects with `cookiecutter.json` prompts.
- Utilize pre-prompt, pre- and post-generate hooks.

[Learn More](https://cookiecutter.readthedocs.io/en/latest/usage.html)

### For Template Creators

- **Any language, any framework.** A Cookiecutter template is just a directory with variables. It works for Python, Rust, Terraform, docs sites, whatever you build repeatedly.
- **Hooks for the rest of the setup.** Pre- and post-generate scripts (shell or Python) handle git init, dependency installs, or anything else your boilerplate needs.
- **One file defines the interface.** `cookiecutter.json` declares every variable and its default. Users answer prompts; the template does the rest.

[Learn More](https://cookiecutter.readthedocs.io/en/latest/tutorials/)

## Available Templates

Discover a variety of ready-to-use templates on [GitHub](https://github.com/search?q=cookiecutter&type=Repositories).

### Special Templates

- [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)
- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django)
- [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)
- [cookiecutter-plone-starter](https://github.com/collective/cookiecutter-plone-starter)

## Community

Join the community, contribute, or seek assistance.

- [Troubleshooting Guide](https://cookiecutter.readthedocs.io/en/latest/troubleshooting.html)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/cookiecutter)
- [Discord](https://discord.gg/9BrxzPKuEW)
- [File an Issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen)
- [Contributors](AUTHORS.md)
- [Contribution Guide](CONTRIBUTING.md)

### Feedback

We value your feedback. Share your criticisms or complaints constructively to help us improve.

- [File an Issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen)

### Waiting for a Response?

- Be patient and consider reaching out to the community for assistance.
- For enterprise support, contact support@feldroy.com.

## Code of Conduct

Adhere to the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/) during all interactions in the project's ecosystem.

## Acknowledgements

Created and led by [Audrey M. Roy Greenfeld](https://github.com/audreyfeldroy), supported by a dedicated team of maintainers and contributors.
