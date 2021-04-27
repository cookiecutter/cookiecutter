# Cookiecutter

[![pypi](https://img.shields.io/pypi/v/cookiecutter.svg)](https://pypi.org/project/cookiecutter/)
[![python](https://img.shields.io/pypi/pyversions/cookiecutter.svg)](https://pypi.org/project/cookiecutter/)
[![Build Status](https://github.com/cookiecutter/cookiecutter/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/cookiecutter/cookiecutter/actions)
[![codecov](https://codecov.io/gh/cookiecutter/cookiecutter/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/cookiecutter/cookiecutter?branch=master)
[![slack](https://img.shields.io/badge/cookiecutter-Join%20on%20Slack-green?style=flat&logo=slack)](https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U)
[![docs](https://readthedocs.org/projects/cookiecutter/badge/?version=latest)](https://readthedocs.org/projects/cookiecutter/?badge=latest)
[![Code Quality](https://img.shields.io/scrutinizer/g/cookiecutter/cookiecutter.svg)](https://scrutinizer-ci.com/g/cookiecutter/cookiecutter/?branch=master)

A command-line utility that creates projects from **cookiecutters** (project
templates), e.g. creating a Python package project from a Python package project
template.

* Documentation: [https://cookiecutter.readthedocs.io](https://cookiecutter.readthedocs.io)
* GitHub: [https://github.com/cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter)
* PyPI: [https://pypi.org/project/cookiecutter/](https://pypi.org/project/cookiecutter/)
* Free and open source software: [BSD license](https://github.com/cookiecutter/cookiecutter/blob/master/LICENSE)

![Cookiecutter](https://raw.githubusercontent.com/cookiecutter/cookiecutter/3ac078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/cookiecutter_medium.png)

We are proud to be an open source sponsor of
[PyCon 2016](https://us.pycon.org/2016/sponsors/).

## Features

Did someone say features?

* Cross-platform: Windows, Mac, and Linux are officially supported.
* You don't have to know/write Python code to use Cookiecutter
* Works with Python 3.6, 3.7, 3.8, 3.9 and PyPy3.
* Project templates can be in any programming language or markup format:
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name it.
  You can use multiple languages in the same project template.
* Simple command line usage:

```bash
# Create project from the cookiecutter-pypackage.git repo template
# You'll be prompted to enter values.
# Then it'll create your Python package in the current working directory,
# based on those values.
$ cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage
# For the sake of brevity, repos on GitHub can just use the 'gh' prefix
$ cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
```

* Use it at the command line with a local template:

```bash
# Create project in the current working directory, from the local
# cookiecutter-pypackage/ template
$ cookiecutter cookiecutter-pypackage/
```

* Or use it from Python:

```py
from cookiecutter.main import cookiecutter

# Create project from the cookiecutter-pypackage/ template
cookiecutter('cookiecutter-pypackage/')

# Create project from the cookiecutter-pypackage.git repo template
cookiecutter('https://github.com/audreyfeldroy/cookiecutter-pypackage.git')
```

* Directory names and filenames can be templated. For example:

```py
{{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}.py
```

* Supports unlimited levels of directory nesting.
* 100% of templating is done with Jinja2. This includes file and directory names.
* Simply define your template variables in a ``cookiecutter.json`` file. For example:

```json
{
    "full_name": "Audrey Feldroy",
    "email": "audreyr@gmail.com",
    "project_name": "Complexity",
    "repo_name": "complexity",
    "project_short_description": "Refreshingly simple static site generator.",
    "release_date": "2013-07-10",
    "year": "2013",
    "version": "0.1.1"
}
```

* Unless you suppress it with ``--no-input``, you are prompted for input:
  * Prompts are the keys in ``cookiecutter.json``.
  * Default responses are the values in ``cookiecutter.json``.
  * Prompts are shown in order.
* Cross-platform support for ``~/.cookiecutterrc`` files:

```yaml
default_context:
    full_name: "Audrey Feldroy"
    email: "audreyr@gmail.com"
    github_username: "audreyfeldroy"
cookiecutters_dir: "~/.cookiecutters/"
```

* Cookiecutters (cloned Cookiecutter project templates) are put into
``~/.cookiecutters/`` by default, or cookiecutters_dir if specified.
* If you have already cloned a cookiecutter into ``~/.cookiecutters/``,
you can reference it by directory name:

```bash
# Clone cookiecutter-pypackage
$ cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
# Now you can use the already cloned cookiecutter by name
$ cookiecutter cookiecutter-pypackage
```

* You can use local cookiecutters, or remote cookiecutters directly from Git
repos or from Mercurial repos on Bitbucket.
* Default context: specify key/value pairs that you want used as defaults
whenever you generate a project.
* Inject extra context with command-line arguments:

```bash
cookiecutter --no-input gh:msabramo/cookiecutter-supervisor program_name=foobar startsecs=10
```

* Direct access to the Cookiecutter API allows for injection of extra context.
* Pre- and post-generate hooks: Python or shell scripts to run before or after
generating a project.
* Paths to local projects can be specified as absolute or relative.
* Projects generated to your current directory or to target directory if
specified with `-o` option.

## Available Cookiecutters

Making great cookies takes a lot of cookiecutters and contributors. We're so
pleased that there are many Cookiecutter project templates to choose from. We
hope you find a cookiecutter that is just right for your needs.

## A Pantry Full of Cookiecutters

The best place to start searching for specific and ready to use cookiecutter
template is [Github search](https://github.com/search?q=cookiecutter&type=Repositories).
Just type `cookiecutter` and you will discover over 4000 related repositories.

We also recommend you to check related GitHub topics. For general search use
[cookiecutter-template](https://github.com/topics/cookiecutter-template).
For specific topics try to use `cookiecutter-yourtopic`, like
`cookiecutter-python` or `cookiecutter-datascience`. This is a new GitHub feature,
so not all active repositories use it at the moment.

If you are template developer please add related
[topics](https://help.github.com/en/github/administering-a-repository/classifying-your-repository-with-topics)
with `cookiecutter` prefix to you repository. We believe it will make it more
discoverable. You are almost not limited in topics amount, use it!

## Cookiecutter Specials

These Cookiecutters are maintained by the cookiecutter team:

* [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage):
[@audreyfeldroy's](https://github.com/audreyfeldroy) ultimate Python package project template.
* [cookiecutter-django](https://github.com/pydanny/cookiecutter-django):
A bleeding edge Django project template with Bootstrap 4, customizable users app,
starter templates, working user registration, celery setup, and much more.
* [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin):
Minimal Cookiecutter template for authoring [pytest](https://docs.pytest.org/)
plugins that help you to write better programs.

## Community

The core committer team can be found in [authors section](AUTHORS.md).
We are always welcome and invite you to participate.

Stuck? Try one of the following:

* See the [Troubleshooting](https://cookiecutter.readthedocs.io/en/latest/troubleshooting.html) page.
* Ask for help on [Stack Overflow](https://stackoverflow.com/questions/tagged/cookiecutter).
* You are strongly encouraged to
[file an issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen)
about the problem, even if it's just "I can't get it to work on this cookiecutter"
with a link to your cookiecutter. Don't worry about naming/pinpointing the issue
properly.
* Ask for help on [Slack](https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U)
if you must (but please try one of the other options first, so that others
can benefit from the discussion).

Development on Cookiecutter is community-driven:

* Huge thanks to all the [contributors](AUTHORS.md) who have pitched in to help
make Cookiecutter an even better tool.
* Everyone is invited to contribute. Read the
[contributing instructions](CONTRIBUTING.md), then get started.
* Connect with other Cookiecutter contributors and users on
[Slack](https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U)
(note: due to work and commitments, a core committer might not always be available)

Encouragement is unbelievably motivating. If you want more work done on
Cookiecutter, show support:

* Thank a core committer for their efforts.
* Star [Cookiecutter on GitHub](https://github.com/cookiecutter/cookiecutter).
* [Support this project](#support-this-project)

Got criticism or complaints?

* [File an issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen)
so that Cookiecutter can be improved. Be friendly and constructive about what
could be better. Make detailed suggestions.
* **Keep us in the loop so that we can help.** For example, if you are
discussing problems with Cookiecutter on a mailing list,
[file an issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen)
where you link to the discussion thread and/or cc at least 1 core committer on the email.
* Be encouraging. A comment like "This function ought to be rewritten like this"
is much more likely to result in action than a comment like "Eww, look how bad
this function is."

Waiting for a response to an issue/question?

* Be patient and persistent. All issues are on the core committer team's radar
and will be considered thoughtfully, but we have a lot of issues to work through.
If urgent, it's fine to ping a core committer in the issue with a reminder.
* Ask others to comment, discuss, review, etc.
* Search the Cookiecutter repo for issues related to yours.
* Need a fix/feature/release/help urgently, and can't wait?
[@audreyfeldroy](https://github.com/audreyfeldroy) is available for hire for consultation
or custom development.

## Support This Project

This project is run by volunteers. Shortly we will be providing means for
organizations and individuals to support the project.

## Code of Conduct

Everyone interacting in the Cookiecutter project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the
[PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).
