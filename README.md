<h1 align="center">
    <img alt="cookiecutter Logo" width="200px" src="https://raw.githubusercontent.com/cookiecutter/cookiecutter/3ac078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/cookiecutter_medium.png">
</h1>
#tilok paul
<div align="center">

[![pypi](https://img.shields.io/pypi/v/cookiecutter.svg)](https://pypi.org/project/cookiecutter/)
[![python](https://img.shields.io/pypi/pyversions/cookiecutter.svg)](https://pypi.org/project/cookiecutter/)
[![Build Status](https://github.com/cookiecutter/cookiecutter/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/cookiecutter/cookiecutter/actions)
[![codecov](https://codecov.io/gh/cookiecutter/cookiecutter/branch/main/graphs/badge.svg?branch=main)](https://codecov.io/github/cookiecutter/cookiecutter?branch=main)
[![discord](https://img.shields.io/badge/Discord-cookiecutter-5865F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/9BrxzPKuEW)
[![docs](https://readthedocs.org/projects/cookiecutter/badge/?version=latest)](https://readthedocs.org/projects/cookiecutter/?badge=latest)
[![Code Quality](https://img.shields.io/scrutinizer/g/cookiecutter/cookiecutter.svg)](https://scrutinizer-ci.com/g/cookiecutter/cookiecutter/?branch=main)

</div>

# Cookiecutter

Create projects swiftly from **cookiecutters** (project templates) with this command-line utility. Ideal for generating Python package projects and more.

- [Documentation](https://cookiecutter.readthedocs.io)
- [GitHub](https://github.com/cookiecutter/cookiecutter)
- [PyPI](https://pypi.org/project/cookiecutter/)
- [License (BSD)](https://github.com/cookiecutter/cookiecutter/blob/main/LICENSE)

## Installation

Install cookiecutter using pip package manager:
```
# pipx is strongly recommended.
pipx install cookiecutter

# If pipx is not an option,
# you can install cookiecutter in your Python user directory.
python -m pip install --user cookiecutter
```

## Features

- **Cross-Platform:** Supports Windows, Mac, and Linux.
- **User-Friendly:** No Python knowledge required.
- **Versatile:** Compatible with Python 3.7 to 3.12.
- **Multi-Language Support:** Use templates in any language or markup format.

### For Users

#### Quick Start

The recommended way to use Cookiecutter as a command line utility is to run it with [`pipx`](https://pypa.github.io/pipx/), which can be installed with `pip install pipx`, but if you plan to use Cookiecutter programmatically, please run `pip install cookiecutter`.

**Use a GitHub template**

```bash
# You'll be prompted to enter values.
# Then it'll create your Python package in the current working directory,
# based on those values.
# For the sake of brevity, repos on GitHub can just use the 'gh' prefix
$ pipx run cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
```

**Use a local template**

```bash
$ pipx run cookiecutter cookiecutter-pypackage/
```

**Use it from Python**

```py
from cookiecutter.main import cookiecutter

# Create project from the cookiecutter-pypackage/ template
cookiecutter('cookiecutter-pypackage/')

# Create project from the cookiecutter-pypackage.git repo template
cookiecutter('gh:audreyfeldroy//cookiecutter-pypackage.git')
```

#### Detailed Usage

- Generate projects from local or remote templates.
- Customize projects with `cookiecutter.json` prompts.
- Utilize pre-prompt, pre- and post-generate hooks.

[Learn More](https://cookiecutter.readthedocs.io/en/latest/usage.html)

### For Template Creators

- Utilize unlimited directory nesting.
- Employ Jinja2 for all templating needs.
- Define template variables easily with `cookiecutter.json`.

[Learn More](https://cookiecutter.readthedocs.io/en/latest/tutorials/)

## Available Templates

Discover a variety of ready-to-use templates on [GitHub](https://github.com/search?q=cookiecutter&type=Repositories).

### Special Templates

- [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)
- [cookiecutter-django](https://github.com/pydanny/cookiecutter-django)
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

### Support

- Star us on [GitHub](https://github.com/cookiecutter/cookiecutter).
- Stay tuned for upcoming support options.

### Feedback

We value your feedback. Share your criticisms or complaints constructively to help us improve.

- [File an Issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen)

### Waiting for a Response?

- Be patient and consider reaching out to the community for assistance.
- For urgent matters, contact [@audreyfeldroy](https://github.com/audreyfeldroy) for consultation or custom development.

## Code of Conduct

Adhere to the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/) during all interactions in the project's ecosystem.

## Acknowledgements

Created and led by [Audrey Roy Greenfeld](https://github.com/audreyfeldroy), supported by a dedicated team of maintainers and contributors.
