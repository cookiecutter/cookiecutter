# Cookiecutter

[![pypi](https://img.shields.io/pypi/v/cookiecutter.svg)](https://pypi.python.org/pypi/cookiecutter)
[![python](https://img.shields.io/pypi/pyversions/cookiecutter.svg)](https://pypi.python.org/pypi/cookiecutter)
[![Build Status](https://travis-ci.org/cookiecutter/cookiecutter.svg?branch=master)](https://travis-ci.org/cookiecutter/cookiecutter)
[![Appveyor](https://ci.appveyor.com/api/projects/status/github/cookiecutter/cookiecutter?branch=master&svg=true)](https://ci.appveyor.com/project/cookiecutter/cookiecutter/branch/master)
[![codecov](https://codecov.io/gh/cookiecutter/cookiecutter/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/cookiecutter/cookiecutter?branch=master)
[![slack](https://img.shields.io/badge/cookiecutter-Join%20on%20Slack-green?style=flat&logo=slack)](https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U)
[![docs](https://readthedocs.org/projects/cookiecutter/badge/?version=latest)](https://readthedocs.org/projects/cookiecutter/?badge=latest)
[![Code Qaulity](https://img.shields.io/scrutinizer/g/cookiecutter/cookiecutter.svg)](https://scrutinizer-ci.com/g/cookiecutter/cookiecutter/?branch=master)

A command-line utility that creates projects from **cookiecutters** (project templates), e.g. creating a Python package project from a Python package project template.

* Documentation: [https://cookiecutter.readthedocs.io](https://cookiecutter.readthedocs.io)
* GitHub: [https://github.com/cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter)
* PyPI: [https://pypi.python.org/pypi/cookiecutter](https://pypi.python.org/pypi/cookiecutter)
* Free and open source software: [BSD license](https://github.com/cookiecutter/cookiecutter/blob/master/LICENSE)

![Cookiecutter](https://raw.githubusercontent.com/cookiecutter/cookiecutter/3ac078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/cookiecutter_medium.png)

We are proud to be an open source sponsor of [PyCon 2016](https://us.pycon.org/2016/sponsors/).

## Features

Did someone say features?

* Cross-platform: Windows, Mac, and Linux are officially supported.

* Works with Python 2.7, 3.5, 3.6, 3.7, 3.8 ,PyPy and PyPy3. *(But you don't have to know/write Python code to use Cookiecutter.)*

* Project templates can be in any programming language or markup format:  
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name it. You can use multiple languages in the same project template.

* Simple command line usage:

```bash
# Create project from the cookiecutter-pypackage.git repo template
# You'll be prompted to enter values.
# Then it'll create your Python package in the current working directory,
# based on those values.
$ cookiecutter https://github.com/audreyr/cookiecutter-pypackage
# For the sake of brevity, repos on GitHub can just use the 'gh' prefix
$ cookiecutter gh:audreyr/cookiecutter-pypackage
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
cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
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
    "full_name": "Audrey Roy",
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
full_name: "Audrey Roy"
email: "audreyr@gmail.com"
github_username: "audreyr"
cookiecutters_dir: "~/.cookiecutters/"
```

* Cookiecutters (cloned Cookiecutter project templates) are put into ``~/.cookiecutters/`` by default, or cookiecutters_dir if specified.

* If you have already cloned a cookiecutter into ``~/.cookiecutters/``, you can reference it by directory name:

```bash
# Clone cookiecutter-pypackage
$ cookiecutter gh:audreyr/cookiecutter-pypackage
# Now you can use the already cloned cookiecutter by name
$ cookiecutter cookiecutter-pypackage
```

* You can use local cookiecutters, or remote cookiecutters directly from Git repos or from Mercurial repos on Bitbucket.

* Default context: specify key/value pairs that you want used as defaults whenever you generate a project.

* Inject extra context with command-line arguments:

```bash
cookiecutter --no-input gh:msabramo/cookiecutter-supervisor program_name=foobar startsecs=10
```

* Direct access to the Cookiecutter API allows for injection of extra context.

* Pre- and post-generate hooks: Python or shell scripts to run before or after generating a project.

* Paths to local projects can be specified as absolute or relative.

* Projects are always generated to your current directory.

## Available Cookiecutters

Making great cookies takes a lot of cookiecutters and contributors. We're so pleased that there are many Cookiecutter project templates to choose from. We hope you find a cookiecutter that is just right for your needs.

### Cookiecutter Specials

These Cookiecutters are maintained by the cookiecutter team:

* [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage): [@audreyr's](https://github.com/audreyr) ultimate Python package project template.
* [cookiecutter-django](https://github.com/pydanny/cookiecutter-django): A bleeding edge Django project template with Bootstrap 4, customizable users app, starter templates, working user registration, celery setup, and much more.
* [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin): Minimal Cookiecutter template for authoring [pytest](http://pytest.org/latest/) plugins that help you to write better programs.

### Categories of Cookiecutters

[Python](#python) | [Python-Django](#python-django) | [Python-Pyramid](#python-pyramid) | [Cookiecutter (meta)](#cookiecutter-meta) | [Ansible](#ansible) | [Git](#git) | [C](#c) | [C++](#c-1) | [C#](#c-sharp) | [Common Lisp](#common-lisp) | [Elm](#elm) | [Golang](#golang) | [Java](#java) | [JS](#js) | [Kotlin](#kotlin) | [LaTeX/XeTeX](#latexxetex) | [PHP](#php) | [Berkshelf-Vagrant](#berkshelf-vagrant) | [HTML](#html) | [Scala](#scala) | [6502 Assembly](#6502-Assembly) | [Data Science](#data-science) | [Tornado](#tornado) | [Reproducible Science](#reproducible-science) | [Continuous Delivery](#continuous-delivery)

If you don't find a cookiecutter that suits your needs here, please consider writing or suggesting one. We wish for our users to find a solution for their use cases, and we provide a list of other projects that we do not maintain for your convenience (please see the [Similar Projects](#similar-projects) section).

## Community

The core committer team can be found in [authors section](AUTHORS.md). We are always welcome and invite you to participate.

Stuck? Try one of the following:

* See the [Troubleshooting](https://cookiecutter.readthedocs.io/en/latest/troubleshooting.html) page.
* Ask for help on [Stack Overflow](https://stackoverflow.com/).
* You are strongly encouraged to [file an issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen) about the problem, even if it's just "I can't get it to work on this cookiecutter" with a link to your cookiecutter. Don't worry about naming/pinpointing the issue properly.
* Ask for help on [Slack](https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U) if you must (but please try one of the other options first, so that others can benefit from the discussion).

Development on Cookiecutter is community-driven:

* Huge thanks to all the [contributors](AUTHORS.md) who have pitched in to help make Cookiecutter an even better tool.
* Everyone is invited to contribute. Read the [contributing instructions](CONTRIBUTING.md), then get started.

Connect with other Cookiecutter contributors and users on [Slack](https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U):

* [https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U](https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U) (note: due to work and commitments, a core committer might not always be available)

Encouragement is unbelievably motivating. If you want more work done on Cookiecutter, show support:

* Thank a core committer for their efforts.
* Star [Cookiecutter on GitHub](https://github.com/cookiecutter/cookiecutter).
* [Support this project](#support-this-project)

Got criticism or complaints?

* [File an issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen) so that Cookiecutter can be improved. Be friendly and constructive about what could be better. Make detailed suggestions.
* **Keep us in the loop so that we can help.** For example, if you are discussing problems with Cookiecutter on a mailing list, [file an issue](https://github.com/cookiecutter/cookiecutter/issues?q=is%3Aopen) where you link to the discussion thread and/or cc at least 1 core committer on the email.
* Be encouraging. A comment like "This function ought to be rewritten like this" is much more likely to result in action than a comment like "Eww, look how bad this function is."

Waiting for a response to an issue/question?

* Be patient and persistent. All issues are on the core committer team's radar and will be considered thoughtfully, but we have a lot of issues to work through. If urgent, it's fine to ping a core committer in the issue with a reminder.
* Ask others to comment, discuss, review, etc.
* Search the Cookiecutter repo for issues related to yours.
* Need a fix/feature/release/help urgently, and can't wait? [@audreyr](https://github.com/audreyr) is available for hire for consultation or custom development.

## Support This Project

This project is run by volunteers. Shortly we will be providing means for organizations and individuals to support the project.

## Code of Conduct

Everyone interacting in the Cookiecutter project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

## A Pantry Full of Cookiecutters

You can check all [cookiecutter templates](https://github.com/topics/cookiecutter-template) on GitHub. If you are template publisher keep in mind to add the ``cookiecutter-template`` topic to your repository and the correct language tags.

Please avoid creating PRs for listing additional templates. We outsourced their listing due to extra maintenance required to review them. We will likely replace the lists below with links to GitHub queries for each category.

### Python

* [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage): [@audreyr](https://github.com/audreyr)'s ultimate Python package project template.
* [cookiecutter-pipproject](https://github.com/wdm0006/cookiecutter-pipproject): Minimal package for pip-installable projects.
* [cookiecutter-pypackage-minimal](https://github.com/kragniz/cookiecutter-pypackage-minimal): A minimal Python package template.
* [cookiecutter-lux-python](https://github.com/alexkey/cookiecutter-lux-python): A boilerplate Python project that aims to create Python package with a convenient Makefile-facility and additional helpers.
* [cookiecutter-flask](https://github.com/cookiecutter-flask/cookiecutter-flask) : A Flask template with Bootstrap 3, starter templates, and working user registration.
* [cookiecutter-flask-2](https://github.com/wdm0006/cookiecutter-flask): A heavier weight fork of cookiecutter-flask, with more boilerplate including forgotten password and Heroku integration.
* [cookiecutter-flask-foundation](https://github.com/JackStouffer/cookiecutter-Flask-Foundation) : Flask Template with caching, forms, sqlalchemy and unit-testing.
* [cookiecutter-flask-minimal](https://github.com/candidtim/cookiecutter-flask-minimal) : Minimal but production-ready Flask project template with no other dependencies except for Flask itself.
* [cookiecutter-flask-skeleton](https://github.com/realpython/cookiecutter-flask-skeleton) : Flask starter project.
* [cookiecutter-bottle](https://github.com/avelino/cookiecutter-bottle) : A cookiecutter template for creating reusable Bottle projects quickly.
* [cookiecutter-openstack](https://github.com/openstack/cookiecutter): A template for an OpenStack project.
* [cookiecutter-docopt](https://github.com/sloria/cookiecutter-docopt): A template for a Python command-line script that uses [docopt](http://docopt.org/) for arguments parsing.
* [cookiecutter-quokka-module](https://github.com/quokkaproject/cookiecutter-quokka-module): A template to create a blueprint module for Quokka Flask CMS.
* [cookiecutter-kivy](https://github.com/hackebrot/cookiecutter-kivy): A template for NUI applications built upon the kivy python-framework.
* [cookiedozer](https://github.com/hackebrot/cookiedozer): A template for Python Kivy apps ready to be deployed to android devices with Buildozer.
* [cookiecutter-pylibrary](https://github.com/ionelmc/cookiecutter-pylibrary): An intricate template designed to quickly get started with good testing and packaging (working configuration for Tox, Pytest, Travis-CI, Coveralls, AppVeyor, Sphinx docs, isort, bumpversion, packaging checks etc).
* [cookiecutter-pyvanguard](https://github.com/robinandeer/cookiecutter-pyvanguard): A template for cutting edge Python development. [Invoke](http://docs.pyinvoke.org/en/latest/), pytest, bumpversion, and Python 2/3 compatibility.
* [Python-iOS-template](https://github.com/beeware/Python-iOS-template): A template to create a Python project that will run on iOS devices.
* [Python-Android-template](https://github.com/beeware/Python-Android-template): A template to create a Python project that will run on Android devices.
* [cookiecutter-tryton](https://bitbucket.org/tryton/cookiecutter-tryton/src/default/): A template to create base and external Tryton modules.
* [cookiecutter-tryton-fulfilio](https://github.com/trytonus/cookiecutter-tryton): A template for creating tryton modules.
* [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin): Minimal Cookiecutter template for authoring [pytest](http://pytest.org/latest/) plugins that help you to write better programs.
* [cookiecutter-tox-plugin](https://github.com/tox-dev/cookiecutter-tox-plugin): Minimal Cookiecutter template for authoring [tox](https://tox.readthedocs.io/en/latest/) plugins to change or extend the behavior of your test automation.
* [cookiecutter-tapioca](https://github.com/vintasoftware/cookiecutter-tapioca): A Template for building [tapioca-wrapper](https://github.com/vintasoftware/tapioca-wrapper) based web API wrappers (clients).

* [cookiecutter-muffin](https://github.com/drgarcia1986/cookiecutter-muffin): A Muffin template with Bootstrap 3, starter templates, and working user registration.
* [cookiecutter-octoprint-plugin](https://github.com/OctoPrint/cookiecutter-octoprint-plugin): A template for building plugins for [OctoPrint](https://github.com/foosel/OctoPrint).
* [cookiecutter-funkload-friendly](https://github.com/tokibito/cookiecutter-funkload-friendly): Cookiecutter template for a [funkload-friendly](https://github.com/tokibito/funkload-friendly) project.
* [cookiecutter-python-app](https://github.com/mdklatt/cookiecutter-python-app): A template to create a Python CLI application with subcommands, logging, YAML configuration, pytest tests, and Virtualenv deployment.
* [morepath-cookiecutter](https://github.com/morepath/morepath-cookiecutter): Cookiecutter template for Morepath, the web microframework with superpowers.
* [Springerle/hovercraft-slides](https://github.com/Springerle/hovercraft-slides): A template for new [Hovercraft!](https://hovercraft.readthedocs.io/en/latest/) presentation projects (``impress.js`` slides in *re*\ Structured\ *Text*).
* [cookiecutter-snakemake-analysis-pipeline](https://github.com/xguse/cookiecutter-snakemake-analysis-pipeline): One way to easily set up [Snakemake](https://bitbucket.org/snakemake/snakemake/wiki/Home)-based analysis pipelines.
* [cookiecutter-py3tkinter](https://github.com/ivanlyon/cookiecutter-py3tkinter): Template for Python 3 Tkinter application gui.
* [cookiecutter-pyqt5](https://github.com/mandeep/cookiecutter-pyqt5): A prebuilt PyQt5 GUI template with a fully featured Pytest test suite and Travis CI integration all in an optimal Python package.
* [cookiecutter-pyqt4](https://github.com/aeroaks/cookiecutter-pyqt4): A prebuilt PyQt4 GUI template with a logging support, structure for tests and separation of ui and worker components.
* [cookiecutter-xontrib](https://github.com/laerus/cookiecutter-xontrib): A template for building xontribs, a.k.a [xonsh](https://github.com/xonsh/xonsh) contributions.
* [cookiecutter-conda-python](https://github.com/conda/cookiecutter-conda-python): A template for building Conda Python packages.
* [cookiecutter-pypackage-rust-cross-platform-publish](https://github.com/mckaymatt/cookiecutter-pypackage-rust-cross-platform-publish): A template for a Python wheel containing a Rust binary module that supports releasing on Windows, OSX and Linux.
* [cookiecutter-telegram-bot](https://github.com/Ars2014/cookiecutter-telegram-bot): A template project for Telegram bots with webhooks on CherryPy.
* [python-project-template](https://github.com/Kwpolska/python-project-template): A template for Python projects with sophisticated release automation.
* [cookiecutter-anyblok-project](https://github.com/AnyBlok/cookiecutter-anyblok-project): A template for Anyblok based projects.
* [cookiecutter-python-cli](https://github.com/xuanluong/cookiecutter-python-cli): A cookiecutter template for creating a Python CLI application using click.

### Python-Django

* [cookiecutter-django](https://github.com/pydanny/cookiecutter-django): A bleeding edge Django project template with Bootstrap 4, customizable users app, starter templates, working user registration, celery setup, and much more.
* [cookiecutter-django-rest](https://github.com/agconti/cookiecutter-django-rest): For creating REST apis for mobile and web applications.
* [cookiecutter-simple-django](https://github.com/marcofucci/cookiecutter-simple-django): A cookiecutter template for creating reusable Django projects quickly.
* [django-docker-bootstrap](https://github.com/legios89/django-docker-bootstrap): Django development/production environment with docker, integrated with Postgres, NodeJS(React), Nginx, uWSGI.
* [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage): A template designed to create reusable third-party PyPI friendly Django apps. Documentation is written in tutorial format.
* [cookiecutter-django-cms](https://github.com/palazzem/cookiecutter-django-cms): A template for Django CMS with simple Bootstrap 3 template. It has a quick start and deploy documentation.
* [cookiecutter-django-crud](https://github.com/wildfish/cookiecutter-django-crud): A template to create a Django app with boilerplate CRUD around a model including a factory and tests.
* [cookiecutter-django-lborgav](https://github.com/lborgav/cookiecutter-django): Another cookiecutter template for Django project with Bootstrap 3 and FontAwesome 4.
* [cookiecutter-django-paas](https://github.com/pbacterio/cookiecutter-django-paas): Django template ready to use in PAAS platforms like Heroku, OpenShift, etc..
* [cookiecutter-django-rest-framework](https://github.com/jpadilla/cookiecutter-django-rest-framework): A template for creating reusable Django REST Framework packages.
* [cookiecutter-django-aws-eb](https://github.com/dolphinkiss/cookiecutter-django-aws-eb): Get up and running with Django on AWS Elastic Beanstalk.
* [cookiecutter-wagtail](https://github.com/torchbox/cookiecutter-wagtail): A cookiecutter template for [Wagtail](https://github.com/wagtail/wagtail) CMS based sites.
* [wagtail-cookiecutter-foundation](https://github.com/chrisdev/wagtail-cookiecutter-foundation): A complete template for Wagtail CMS projects featuring [Zurb Foundation](https://foundation.zurb.com/) 6, ansible provisioning and deployment , front-end dependency management with bower, modular apps to get your site up and running including photo_gallery, RSS feed etc.
* [django-starter](https://github.com/tkjone/starterkit-django): A Django template complete with vagrant and provisioning scripts - inspired by 12 factor apps and cookiecutter-django.
* [cookiecutter-django-gulp](https://github.com/valerymelou/cookiecutter-django-gulp): A Cookiecutter template for integrating frontend development tools in Django projects.
* [wagtail-starter-kit](https://github.com/tkjone/starterkit-wagtail): A cookiecutter complete with wagtail, django layout, vagrant, provisioning scripts, front end build system and more!
* [cookiecutter-django-herokuapp](https://github.com/dulacp/cookiecutter-django-herokuapp): A Django 1.7+ template optimized for Python 3 on Heroku.
* [cookiecutter-simple-django-cn](https://github.com/shenyushun/cookiecutter-simple-django-cn): A simple Django templates for chinese.
* [cc_django_ember_app](https://bitbucket.org/levit_scs/cc_django_ember_app/src/master/): For creating applications with Django and EmberJS.
* [cc_project_app_drf](https://bitbucket.org/levit_scs/cc_project_app_drf/src/master/): For creating REST apis based on the "project app" project architecture.
* [cc_project_app_full_with_hooks](https://bitbucket.org/levit_scs/cc_project_app_full_with_hooks/src/master/): For creating Django projects using the "project app" project architecture.
* [cc-automated-drf-template](https://github.com/TAMU-CPT/cc-automated-drf-template): A template + script that automatically creates your Django REST project with serializers, views, urls, and admin files based on your models file as input.
* [cookiecutter-django-foundation](https://github.com/Parbhat/cookiecutter-django-foundation): Fork of [cookiecutter-django](https://github.com/pydanny/cookiecutter-django) based on [Zurb Foundation](https://foundation.zurb.com/) 6 front-end framework.
* [cookiecutter-django-ansible](https://github.com/HackSoftware/cookiecutter-django-ansible): Cookiecutter Django Ansible is a framework for jumpstarting an ansible project for provisioning a server that is ready for your *cookiecutter-django* application.
* [wemake-django-template](https://github.com/wemake-services/wemake-django-template): Bleeding edge Django template focused on code quality and security.
* [cookiecutter-django-dokku](https://github.com/mashrikt/cookiecutter-django-dokku): A template for jumpstarting Django projects and deploying with Dokku.

### Python-Pyramid

* [pyramid-cookiecutter-alchemy](https://github.com/Pylons/pyramid-cookiecutter-alchemy): A Cookiecutter (project template) for creating a Pyramid project using SQLite for persistent storage SQLAlchemy for an ORM, URL dispatch for routing, and Jinja2 for templating.
* [pyramid-cookiecutter-starter](https://github.com/Pylons/pyramid-cookiecutter-starter): A Cookiecutter (project template) for creating a Pyramid starter project using URL dispatch for routing and either Jinja2, Chameleon, or Mako for templating.
* [pyramid-cookiecutter-zodb](https://github.com/Pylons/pyramid-cookiecutter-zodb): A Cookiecutter (project template) for creating a Pyramid project using ZODB for persistent storage traversal for routing, and Chameleon for templating.
* [substanced-cookiecutter](https://github.com/Pylons/substanced-cookiecutter): A cookiecutter (project template) for creating a Substance D starter project. Substance D is built on top of Pyramid.
* [cookiecutter-pyramid-talk-python-starter](https://github.com/mikeckennedy/cookiecutter-pyramid-talk-python-starter): An opinionated Cookiecutter template for creating Pyramid web applications starting way further down the development chain. This cookiecutter template will create a new Pyramid web application with email, sqlalchemy, rollbar, and way more integrated.

### Cookiecutter (meta)

Meta-templates for generating Cookiecutter project templates.

* [cookiecutter-template](https://github.com/eviweb/cookiecutter-template): Cookiecutter template for creating a... cookiecutter template...

### Ansible

* [cookiecutter-molecule](https://github.com/retr0h/cookiecutter-molecule): Create [Molecule](https://molecule.readthedocs.io/en/v2/) roles following community best practices, with an already implemented test infrastructure leveraging [Molecule](https://molecule.readthedocs.io/en/v2/), Docker and Testinfra.
* [cookiecutter-ansible-role](https://github.com/iknite/cookiecutter-ansible-role): A template to create ansible roles. Forget about file creation and focus on actions.
* [cookiecutter-ansible-role-ci](https://github.com/ferrarimarco/cookiecutter-ansible-role): Create Ansible roles following best practices, with an already implemented test infrastructure leveraging Test-kitchen, Docker and InSpec.

### Git

* [cookiecutter-git](https://github.com/NathanUrwin/cookiecutter-git): Git repo project template :clipboard.

### C

* [bootstrap.c](https://github.com/vincentbernat/bootstrap.c): A template for simple projects written in C with autotools.
* [cookiecutter-avr](https://github.com/solarnz/cookiecutter-avr): A template for avr development.

### C++

* [BoilerplatePP](https://github.com/Paspartout/BoilerplatePP): A simple cmake template with unit testing for projects written in C++.
* [cookiecutter-dpf-effect](https://github.com/SpotlightKid/cookiecutter-dpf-effect): An audio plugin project template for the DISTRHO Plugin Framework (DPF).
* [cookiecutter-dpf-audiotk](https://github.com/SpotlightKid/cookiecutter-dpf-audiotk): An audio plugin project template for the DISTRHO Plugin Framework (DPF) and the Audio Toolkit (ATK) DSP library
* [cookiecutter-kata-gtest](https://github.com/13coders/cookiecutter-kata-gtest): A template for C++ test-driven development katas using the Google Test framework.
* [cookiecutter-kata-cpputest](https://github.com/13coders/cookiecutter-kata-cpputest): A template for C++ test-driven-development katas using the CppUTest framework.

### C-Sharp

* [cookiecutter-csharp-objc-binding](https://github.com/SandyChapman/cookiecutter-csharp-objc-binding): A template for generating a C# binding project for binding an Objective-C static library.

### Common Lisp

* [cookiecutter-cl-project](https://github.com/svetlyak40wt/cookiecutter-cl-project): A template for Common Lisp project with bootstrap script and Slime integration.

### Elm

* [cookiecutter-elm](https://github.com/m-x-k/cookiecutter-elm): Elm based cookiecutter with basic html example.

### Golang

* [cookiecutter-golang](https://github.com/lacion/cookiecutter-golang): A template to create new go based projects following best practices.

### Java

* [cookiecutter-java](https://github.com/m-x-k/cookiecutter-java): Cookiecutter for basic java application setup with gradle.
* [cookiecutter-spring-boot](https://github.com/m-x-k/cookiecutter-spring-boot): Cookiecutter for standard java spring boot gradle application.
* [cookiecutter-android](https://github.com/alexfu/cookiecutter-android): Cookiecutter for Gradle-based Android projects.

### JS

* [cookiecutter-es6-boilerplate](https://github.com/agconti/cookiecutter-es6-boilerplate): A cookiecutter for front end projects in ES6.
* [cookiecutter-webpack](https://github.com/goldhand/cookiecutter-webpack): A template for webpack 2 projects with hot reloading, babel es6 modules, and react.
* [cookiecutter-jquery](https://github.com/audreyr/cookiecutter-jquery): A jQuery plugin project template based on jQuery Boilerplate.
* [cookiecutter-jswidget](https://github.com/audreyr/cookiecutter-jswidget): A project template for creating a generic front-end, non-jQuery JS widget packaged for multiple JS packaging systems.
* [cookiecutter-component](https://github.com/audreyr/cookiecutter-component): A template for a Component JS package.
* [cookiecutter-tampermonkey](https://github.com/christabor/cookiecutter-tampermonkey): A template for a TamperMonkey browser script.
* [cookiecutter-es6-package](https://github.com/ratson/cookiecutter-es6-package): A template for writing node packages using ES6 via babel.
* [cookiecutter-angular2](https://github.com/matheuspoleza/cookiecutter-angular2): A template for modular angular2 with typescript apps.
* [CICADA](https://github.com/TAMU-CPT/CICADA): A template + script that automatically creates list/detail controllers and partials for an AngularJS frontend to connect to a DRF backend. Works well with [cc-automated-drf-template](https://github.com/TAMU-CPT/cc-automated-drf-template).

### Kotlin

* [cookiecutter-kotlin-gradle](https://github.com/thomaslee/cookiecutter-kotlin-gradle): A bare-bones template for Gradle-based Kotlin projects.

### LaTeX/XeTeX

* [pandoc-talk](https://github.com/larsyencken/pandoc-talk): A cookiecutter template for giving talks with pandoc and XeTeX.
* [cookiecutter-latex-article](https://github.com/selimb/cookiecutter-latex-article): A LaTeX template geared towards academic use.
* [cookiecutter-beamer](https://github.com/luismartingil/cookiecutter-beamer): A template for a LaTeX Beamer presentation.

### PHP

* [cookiecutter-mediawiki-extension](https://github.com/JonasGroeger/cookiecutter-mediawiki-extension): A template for MediaWiki extensions.

### Sublime Text

* [cookiecutter-sublime-text-3-plugin](https://github.com/kkujawinski/cookiecutter-sublime-text-3-plugin): Sublime Text 3 plugin template with custom settings, commands, key bindings and main menu.
* [sublime-snippet-package-template](https://github.com/fhightower-templates/sublime-snippet-package-template): Template for Sublime Text packages containing snippets.

### Berkshelf-Vagrant

* [slim-berkshelf-vagrant](https://github.com/mahmoudimus/cookiecutter-slim-berkshelf-vagrant): A simple cookiecutter template with sane cookbook defaults for common vagrant/berkshelf cookbooks.

### HTML

* [cookiecutter-complexity](https://github.com/audreyr/cookiecutter-complexity): A cookiecutter for a Complexity static site with Bootstrap 3.
* [cookiecutter-reveal.js](https://github.com/keimlink/cookiecutter-reveal.js): A cookiecutter template for reveal.js presentations.
* [cookiecutter-tumblr-theme](https://github.com/relekang/cookiecutter-tumblr-theme): A cookiecutter for a Tumblr theme project with GruntJS as concatenation tool.

### Scala

* [cookiecutter-scala](https://github.com/Plippe/cookiecutter-scala): A cookiecutter template for a simple scala hello world application with a few libraries.
* [cookiecutter-scala-spark](https://github.com/jpzk/cookiecutter-scala-spark): A cookiecutter template for Apache Spark applications written in Scala.

### 6502 Assembly

* [cookiecutter-atari2600](https://github.com/joeyjoejoejr/cookiecutter-atari2600): A cookiecutter template for Atari2600 projects.

### Data Science

* [widget-cookiecutter](https://github.com/jupyter-widgets/widget-cookiecutter): A cookiecutter template for creating a custom Jupyter widget project.
* [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science): A logical, reasonably standardized, but flexible project structure for doing and sharing data science work in Python.  Full documentation available [here](http://drivendata.github.io/cookiecutter-data-science/).
* [cookiecutter-r-data-analysis](https://github.com/bdcaf/cookiecutter-r-data-analysis): Template for a R based workflow to docx (via Pandoc) and pdf (via LaTeX) reports.
* [cookiecutter-docker-science](https://github.com/docker-science/cookiecutter-docker-science): Cookiecutter template for data scientists working in Docker containers.

### Reproducible Science

* [cookiecutter-reproducible-science](https://github.com/mkrapp/cookiecutter-reproducible-science): A cookiecutter template to start a reproducible and transparent science project including data models, analysis, and reports (i.e., your scientific paper) with close resemblances to the philosophy of Cookiecutter [Data Science](#data-science).

### Data Driven Journalism

* [cookiecutter-data-driven-journalism](https://github.com/jastark/cookiecutter-data-driven-journalism): A cookiecutter template to facilitate transparency in data journalism with consistent organisation of data journalism projects and some pre-populated files (including .gitignore, README, AUTHORS).

### Continuous Delivery

* [painless-continuous-delivery](https://github.com/painless-software/painless-continuous-delivery): A cookiecutter template for software development setups with continuous delivery baked in. Python (Django, Flask), and experimental PHP support.
* [cookiecutter-devenv](https://bitbucket.org/greenguavalabs/cookiecutter-devenv/src/master/): A template to add a development and ci environment to an existing project.

### Cloud Tools

* [cookiecutter-tf-module](https://github.com/DualSpark/cookiecutter-tf-module): Cookiecutter template for building consistent Terraform modules.

### Tornado

* [cookiecutter-tornado](https://github.com/hkage/cookiecutter-tornado): Cookiecutter template for Tornado based projects.

### Other

* [cookiecutter-awesome](https://github.com/Pawamoy/cookiecutter-awesome): Cookiecutter to create an [awesome](https://github.com/sindresorhus/awesome) list.
* [cookiecutter_dotfile](https://github.com/bdcaf/cookiecutter_dotfile): Template for a folder of dotfiles managed by stow.
* [cookiecutter-raml](https://github.com/genzj/cookiecutter-raml): Template for RAML v1.0 API documents.

## Similar projects

* [Diecutter](https://github.com/diecutter/diecutter): an API service that will give you back a configuration file from a template and variables.

* [Django](https://docs.djangoproject.com/en/1.9/ref/django-admin/#cmdoption-startapp--template)'s `startproject` and `startapp` commands can take in a `--template` option.

* [python-packager](https://github.com/fcurella/python-packager): Creates Python packages from its own template, with configurable options.

* [Yeoman](https://github.com/yeoman/generator) has a Rails-inspired generator system that provides scaffolding for apps.

* [mr.bob](https://github.com/domenkozar/mr.bob) is a filesystem template renderer, meant to deprecate tools such as
  paster and templer.

* [grunt-init](https://github.com/gruntjs/grunt-init) is used to be built into Grunt and is now a standalone scaffolding tool
  to automate project creation.

* [scaffolt](https://github.com/paulmillr/scaffolt) consumes JSON generators with Handlebars support.

* [init-skeleton](https://github.com/brunch/init-skeleton) clones or copies a repository, executes npm install and bower install and removes the .git directory.

* [Cog](https://bitbucket.org/ned/cog/src/default/) python-based code generation toolkit developed by Ned Batchelder

* [Skaffold](https://github.com/christabor/Skaffold) python and json config based django/MVC generator, with some add-ons and integrations.
