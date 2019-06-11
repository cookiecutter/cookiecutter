=============
Cookiecutter
=============

.. image:: https://img.shields.io/pypi/v/cookiecutter.svg
        :target: https://pypi.python.org/pypi/cookiecutter

.. image:: https://img.shields.io/pypi/pyversions/cookiecutter.svg
        :target: https://pypi.python.org/pypi/cookiecutter

.. image:: https://travis-ci.org/audreyr/cookiecutter.svg?branch=master
        :target: https://travis-ci.org/audreyr/cookiecutter

.. image:: https://ci.appveyor.com/api/projects/status/github/audreyr/cookiecutter?branch=master
        :target: https://ci.appveyor.com/project/audreyr/cookiecutter/branch/master

.. image:: https://codecov.io/github/audreyr/cookiecutter/coverage.svg?branch=master
        :target: https://codecov.io/github/audreyr/cookiecutter?branch=master

.. image:: https://badges.gitter.im/Join Chat.svg
        :target: https://gitter.im/audreyr/cookiecutter?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://readthedocs.org/projects/cookiecutter/badge/?version=latest
        :target: https://readthedocs.org/projects/cookiecutter/?badge=latest
        :alt: Documentation Status

.. image:: https://landscape.io/github/audreyr/cookiecutter/master/landscape.svg?style=flat
        :target: https://landscape.io/github/audreyr/cookiecutter/master
        :alt: Code Health

.. image:: https://img.shields.io/scrutinizer/g/audreyr/cookiecutter.svg
        :target: https://scrutinizer-ci.com/g/audreyr/cookiecutter/?branch=master
        :alt: Scrutinizer Code Quality

A command-line utility that creates projects from **cookiecutters** (project
templates), e.g. creating a Python package project from a Python package project template.

* Documentation: https://cookiecutter.readthedocs.io
* GitHub: https://github.com/audreyr/cookiecutter
* PyPI: https://pypi.python.org/pypi/cookiecutter
* Free and open source software: `BSD license`_

.. image:: https://raw.github.com/audreyr/cookiecutter/3ac078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/cookiecutter_medium.png

We are proud to be an open source sponsor of `PyCon 2016`_.

Features
--------

Did someone say features?

* Cross-platform: Windows, Mac, and Linux are officially supported.

* Works with Python 2.7, 3.5, 3.6, 3.7, and PyPy. *(But you don't have to
  know/write Python code to use Cookiecutter.)*

* Project templates can be in any programming language or markup format:
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name
  it. You can use multiple languages in the same project template.

* Simple command line usage:

    .. code-block:: bash

        # Create project from the cookiecutter-pypackage.git repo template
        # You'll be prompted to enter values.
        # Then it'll create your Python package in the current working directory,
        # based on those values.
        $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage
        # For the sake of brevity, repos on GitHub can just use the 'gh' prefix
        $ cookiecutter gh:audreyr/cookiecutter-pypackage

* Use it at the command line with a local template:

    .. code-block:: bash

        # Create project in the current working directory, from the local
        # cookiecutter-pypackage/ template
        $ cookiecutter cookiecutter-pypackage/

* Or use it from Python:

    .. code-block:: python

        from cookiecutter.main import cookiecutter

        # Create project from the cookiecutter-pypackage/ template
        cookiecutter('cookiecutter-pypackage/')

        # Create project from the cookiecutter-pypackage.git repo template
        cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')

* Directory names and filenames can be templated. For example::

    {{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}.py

* Supports unlimited levels of directory nesting.

* 100% of templating is done with Jinja2. This includes file and directory names.

* Simply define your template variables in a ``cookiecutter.json`` file. For example:

    .. code-block:: json

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

* Unless you suppress it with ``--no-input``, you are prompted for input:

  - Prompts are the keys in ``cookiecutter.json``.
  - Default responses are the values in ``cookiecutter.json``.
  - Prompts are shown in order.

* Cross-platform support for ``~/.cookiecutterrc`` files:

    .. code-block:: yaml

        default_context:
            full_name: "Audrey Roy"
            email: "audreyr@gmail.com"
            github_username: "audreyr"
        cookiecutters_dir: "~/.cookiecutters/"

* Cookiecutters (cloned Cookiecutter project templates) are put into
  ``~/.cookiecutters/`` by default, or cookiecutters_dir if specified.

* If you have already cloned a cookiecutter into ``~/.cookiecutters/``, you
  can reference it by directory name:

    .. code-block:: bash

        # Clone cookiecutter-pypackage
        $ cookiecutter gh:audreyr/cookiecutter-pypackage
        # Now you can use the already cloned cookiecutter by name
        $ cookiecutter cookiecutter-pypackage

* You can use local cookiecutters, or remote cookiecutters directly from Git
  repos or from Mercurial repos on Bitbucket.

* Default context: specify key/value pairs that you want used as defaults
  whenever you generate a project

* Inject extra context with command-line arguments:

    .. code-block:: bash

        $ cookiecutter --no-input gh:msabramo/cookiecutter-supervisor program_name=foobar startsecs=10

* Direct access to the Cookiecutter API allows for injection of extra context.

* Pre- and post-generate hooks: Python or shell scripts to run before or after
  generating a project.

* Paths to local projects can be specified as absolute or relative.

* Projects are always generated to your current directory.

Available Cookiecutters
-----------------------

Making great cookies takes a lot of cookiecutters and contributors. We're so
pleased that there are many Cookiecutter project templates to choose from. We
hope you find a cookiecutter that is just right for your needs.

Cookiecutter Specials
~~~~~~~~~~~~~~~~~~~~~

These Cookiecutters are maintained by the cookiecutter team:

* `cookiecutter-pypackage`_: `@audreyr`_'s ultimate Python package project
  template.
* `cookiecutter-django`_: A bleeding edge Django project template with
  Bootstrap 4, customizable users app, starter templates, working user
  registration, celery setup, and much more.
* `cookiecutter-pytest-plugin`_: Minimal Cookiecutter template for authoring
  `pytest`_ plugins that help you to write better programs.

Categories of Cookiecutters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Python`_ |
`Python-Django`_ |
`Python-Pyramid`_ |
`Cookiecutter (meta)`_ |
`Ansible`_ |
`Git`_ |
`C`_ |
`C++`_ |
`C#`_ |
`Common Lisp`_ |
`Elm`_ |
`Golang`_ |
`Java`_ |
`JS`_ |
`Kotlin`_ |
`LaTeX/XeTeX`_ |
`PHP`_ |
`Berkshelf-Vagrant`_ |
`HTML`_ |
`Scala`_ |
`6502 Assembly`_ |
`Data Science`_ |
`Tornado`_ |
`Reproducible Science`_ |
`Continuous Delivery`_

If you don't find a cookiecutter that suits your needs here, please consider
writing or suggesting one. We wish for our users to find a solution for their
use cases, and we provide a list of other projects that we do not maintain for
your convenience (please see the `Similar Projects`_ section).

Community
---------

The core committer team is `@audreyr`_, `@pydanny`_, `@michaeljoseph`_,
`@pfmoore`_, and `@hackebrot`_. We
welcome you and invite you to participate.

Stuck? Try one of the following:

* See the `Troubleshooting`_ page.
* Ask for help on `Stack Overflow`_.
* You are strongly encouraged to `file an issue`_ about the problem, even if
  it's just "I can't get it to work on this cookiecutter" with a link to your
  cookiecutter. Don't worry about naming/pinpointing the issue properly.
* Ask for help on `Gitter`_ if you must (but please try one of the other
  options first, so that others can benefit from the discussion)

Development on Cookiecutter is community-driven:

* Huge thanks to all the `contributors`_ who have pitched in to help make
  Cookiecutter an even better tool.
* Everyone is invited to contribute. Read the `contributing instructions`_,
  then get started.

Connect with other Cookiecutter contributors and users on `Gitter`_:

* https://gitter.im/audreyr/cookiecutter (note: due to work and commitments,
  a core committer might not always be available)

Encouragement is unbelievably motivating. If you want more work done on
Cookiecutter, show support:

* Thank a core committer for their efforts.
* Star `Cookiecutter on GitHub`_.
* `Support this project`_

Got criticism or complaints?

* `File an issue`_ so that Cookiecutter can be improved. Be friendly
  and constructive about what could be better. Make detailed suggestions.
* **Keep us in the loop so that we can help.** For example, if you are
  discussing problems with Cookiecutter on a mailing list, `file an issue`_
  where you link to the discussion thread and/or cc at least 1 core committer on
  the email.
* Be encouraging. A comment like "This function ought to be rewritten like
  this" is much more likely to result in action than a comment like "Eww, look
  how bad this function is."

Waiting for a response to an issue/question?

* Be patient and persistent. All issues are on the core committer team's radar and
  will be considered thoughtfully, but we have a lot of issues to work through. If
  urgent, it's fine to ping a core committer in the issue with a reminder.
* Ask others to comment, discuss, review, etc.
* Search the Cookiecutter repo for issues related to yours.
* Need a fix/feature/release/help urgently, and can't wait? `@audreyr`_ is
  available for hire for consultation or custom development.

Support This Project
--------------------

This project is run by volunteers. Please support them in their efforts to
maintain and improve Cookiecutter:

* Daniel Roy Greenfeld (`@pydanny`_): `patreon.com/danielroygreenfeld`_
* Raphael Pierzina (`@hackebrot`_): `patreon.com/hackebrot`_

.. _`patreon.com/danielroygreenfeld`: https://www.patreon.com/danielroygreenfeld
.. _`patreon.com/hackebrot`: https://www.patreon.com/hackebrot

You can also support this project by taking our Python packaging course:

.. image:: https://www.pydanny.com/static/packaging-course.jpg
   :name: Creating and Distributing Python Packages image
   :align: center
   :alt: Creating and Distributing Python Packages
   :target: https://courses.twoscoopspress.com/courses/creating-and-distributing-python-packages

Also available in Spanish:

.. image:: https://www.pydanny.com/static/packaging-course-es.jpg
   :name: Creating and Distributing Python Packages ES image
   :align: center
   :alt: Creating and Distributing Python Packages ES
   :target: https://courses.twoscoopspress.com/courses/creating-and-distributing-python-packages-es


Backers
-------

We would like to thank the following people for supporting us:

* Alex DeBrie
* Alexandre Y. Harano
* Bruno Alla
* Carol Willing
* Russell Keith-Magee

Code of Conduct
---------------

Everyone interacting in the Cookiecutter project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.

----

A Pantry Full of Cookiecutters
------------------------------

Here is a list of **cookiecutters** (aka Cookiecutter project templates) for
you to use or fork.

Make your own, then submit a pull request adding yours to this list!

Python
~~~~~~

* `cookiecutter-pypackage`_: `@audreyr`_'s ultimate Python package project
  template.
* `cookiecutter-pipproject`_: Minimal package for pip-installable projects
* `cookiecutter-pypackage-minimal`_: A minimal Python package template.
* `cookiecutter-lux-python`_: A boilerplate Python project that aims to create Python package with a convenient Makefile-facility and additional helpers.
* `cookiecutter-flask`_ : A Flask template with Bootstrap 3, starter templates, and working user registration.
* `cookiecutter-flask-2`_: A heavier weight fork of cookiecutter-flask, with more boilerplate including forgotten password and Heroku integration
* `cookiecutter-flask-foundation`_ : Flask Template with caching, forms, sqlalchemy and unit-testing.
* `cookiecutter-flask-minimal`_ : Minimal but production-ready Flask project template with no other dependencies except for Flask itself.
* `cookiecutter-flask-skeleton`_ : Flask starter project.
* `cookiecutter-bottle`_ : A cookiecutter template for creating reusable Bottle projects quickly.
* `cookiecutter-openstack`_: A template for an OpenStack project.
* `cookiecutter-docopt`_: A template for a Python command-line script that uses `docopt`_ for arguments parsing.
* `cookiecutter-quokka-module`_: A template to create a blueprint module for Quokka Flask CMS.
* `cookiecutter-kivy`_: A template for NUI applications built upon the kivy python-framework.
* `cookiedozer`_: A template for Python Kivy apps ready to be deployed to android devices with Buildozer.
* `cookiecutter-pylibrary`_: An intricate template designed to quickly get started with good testing and packaging (working configuration for Tox, Pytest, Travis-CI, Coveralls, AppVeyor, Sphinx docs, isort, bumpversion, packaging checks etc).
* `cookiecutter-pyvanguard`_: A template for cutting edge Python development. `Invoke`_, pytest, bumpversion, and Python 2/3 compatibility.
* `Python-iOS-template`_: A template to create a Python project that will run on iOS devices.
* `Python-Android-template`_: A template to create a Python project that will run on Android devices.
* `cookiecutter-tryton`_: A template to create base and external Tryton modules.
* `cookiecutter-tryton-fulfilio`_: A template for creating tryton modules.
* `cookiecutter-pytest-plugin`_: Minimal Cookiecutter template for authoring `pytest`_ plugins that help you to write better programs.
* `cookiecutter-tox-plugin`_: Minimal Cookiecutter template for authoring `tox`_ plugins to change or extend the behavior of your test automation.
* `cookiecutter-tapioca`_: A Template for building `tapioca-wrapper`_ based web API wrappers (clients).
* `cookiecutter-muffin`_: A Muffin template with Bootstrap 3, starter templates, and working user registration.
* `cookiecutter-octoprint-plugin`_: A template for building plugins for `OctoPrint`_.
* `cookiecutter-funkload-friendly`_: Cookiecutter template for a `funkload-friendly`_ project.
* `cookiecutter-python-app`_: A template to create a Python CLI application with subcommands, logging, YAML configuration, pytest tests, and Virtualenv deployment.
* `morepath-cookiecutter`_: Cookiecutter template for Morepath, the web microframework with superpowers.
* `Springerle/hovercraft-slides`_: A template for new `Hovercraft!`_ presentation projects (``impress.js`` slides in *re*\ Structured\ *Text*).
* `cookiecutter-snakemake-analysis-pipeline`_: One way to easily set up `Snakemake`_-based analysis pipelines.
* `cookiecutter-py3tkinter`_: Template for Python 3 Tkinter application gui.
* `cookiecutter-pyqt5`_: A prebuilt PyQt5 GUI template with a fully featured Pytest test suite and Travis CI integration all in an optimal Python package.
* `cookiecutter-pyqt4`_: A prebuilt PyQt4 GUI template with a logging support, structure for tests and separation of ui and worker components.
* `cookiecutter-xontrib`_: A template for building xontribs, a.k.a `xonsh`_ contributions
* `cookiecutter-conda-python`_: A template for building Conda Python packages
* `cookiecutter-pypackage-rust-cross-platform-publish`_: A template for a Python wheel containing a Rust binary module that supports releasing on Windows, OSX and Linux.
* `cookiecutter-telegram-bot`_: A template project for Telegram bots with webhooks on CherryPy.
* `python-project-template`_: A template for Python projects with sophisticated release automation.
* `cookiecutter-anyblok-project`_: A template for Anyblok based projects.
* `cookiecutter-python-cli`_: A cookiecutter template for creating a Python CLI application using click

.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`cookiecutter-pipproject`: https://github.com/wdm0006/cookiecutter-pipproject
.. _`cookiecutter-pypackage-minimal`: https://github.com/kragniz/cookiecutter-pypackage-minimal
.. _`cookiecutter-lux-python`: https://github.com/alexkey/cookiecutter-lux-python
.. _`cookiecutter-flask`: https://github.com/sloria/cookiecutter-flask
.. _`cookiecutter-flask-2`: https://github.com/wdm0006/cookiecutter-flask
.. _`cookiecutter-flask-foundation`: https://github.com/JackStouffer/cookiecutter-Flask-Foundation
.. _`cookiecutter-flask-minimal`: https://github.com/candidtim/cookiecutter-flask-minimal
.. _`cookiecutter-flask-skeleton`: https://github.com/realpython/cookiecutter-flask-skeleton
.. _`cookiecutter-flask-ask`: https://github.com/chrisvoncsefalvay/cookiecutter-flask-ask
.. _`cookiecutter-bottle`: https://github.com/avelino/cookiecutter-bottle
.. _`cookiecutter-openstack`: https://github.com/openstack-dev/cookiecutter
.. _`cookiecutter-docopt`: https://github.com/sloria/cookiecutter-docopt
.. _`docopt`: http://docopt.org/
.. _`cookiecutter-quokka-module`: https://github.com/pythonhub/cookiecutter-quokka-module
.. _`cookiecutter-kivy`: https://github.com/hackebrot/cookiecutter-kivy
.. _`cookiedozer`: https://github.com/hackebrot/cookiedozer
.. _`cookiecutter-pylibrary`: https://github.com/ionelmc/cookiecutter-pylibrary
.. _`cookiecutter-pyvanguard`: https://github.com/robinandeer/cookiecutter-pyvanguard
.. _`Invoke`: http://docs.pyinvoke.org/en/latest/
.. _`Python-iOS-template`: https://github.com/pybee/Python-iOS-template
.. _`Python-Android-template`: https://github.com/pybee/Python-Android-template
.. _`cookiecutter-tryton`: https://bitbucket.org/tryton/cookiecutter-tryton
.. _`cookiecutter-tryton-fulfilio`: https://github.com/fulfilio/cookiecutter-tryton
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`pytest`: http://pytest.org/latest/
.. _`cookiecutter-tox-plugin`: https://github.com/tox-dev/cookiecutter-tox-plugin
.. _`tox`: https://tox.readthedocs.io/
.. _`cookiecutter-tapioca`: https://github.com/vintasoftware/cookiecutter-tapioca
.. _`tapioca-wrapper`: https://github.com/vintasoftware/tapioca-wrapper
.. _`cookiecutter-muffin`: https://github.com/drgarcia1986/cookiecutter-muffin
.. _`cookiecutter-octoprint-plugin`: https://github.com/OctoPrint/cookiecutter-octoprint-plugin
.. _`OctoPrint`: https://github.com/foosel/OctoPrint
.. _`cookiecutter-funkload-friendly`: https://github.com/tokibito/cookiecutter-funkload-friendly
.. _`funkload-friendly`: https://github.com/tokibito/funkload-friendly
.. _`cookiecutter-python-app`: https://github.com/mdklatt/cookiecutter-python-app
.. _`morepath-cookiecutter`: https://github.com/morepath/morepath-cookiecutter
.. _`Springerle/hovercraft-slides`: https://github.com/Springerle/hovercraft-slides
.. _`Hovercraft!`: https://hovercraft.readthedocs.io/
.. _`cookiecutter-snakemake-analysis-pipeline`: https://github.com/xguse/cookiecutter-snakemake-analysis-pipeline
.. _`Snakemake`: https://bitbucket.org/snakemake/snakemake/wiki/Home
.. _`cookiecutter-py3tkinter`: https://github.com/ivanlyon/cookiecutter-py3tkinter
.. _`cookiecutter-pyqt5`: https://github.com/mandeepbhutani/cookiecutter-pyqt5
.. _`cookiecutter-pyqt4`: https://github.com/aeroaks/cookiecutter-pyqt4
.. _`cookiecutter-xontrib`: https://github.com/laerus/cookiecutter-xontrib
.. _`xonsh`: https://github.com/xonsh/xonsh
.. _`cookiecutter-conda-python`: https://github.com/conda/cookiecutter-conda-python
.. _`cookiecutter-pypackage-rust-cross-platform-publish`: https://github.com/mckaymatt/cookiecutter-pypackage-rust-cross-platform-publish
.. _`cookiecutter-telegram-bot`: https://github.com/Ars2014/cookiecutter-telegram-bot
.. _`python-project-template`: https://github.com/Kwpolska/python-project-template
.. _`cookiecutter-anyblok-project`: https://github.com/AnyBlok/cookiecutter-anyblok-project
.. _`cookiecutter-python-cli`: https://github.com/xuanluong/cookiecutter-python-cli

Python-Django
^^^^^^^^^^^^^

* `cookiecutter-django`_: A bleeding edge Django project template with Bootstrap 4, customizable users app, starter templates,  working user registration, celery setup, and much more.
* `cookiecutter-django-rest`_: For creating REST apis for mobile and web applications.
* `cookiecutter-simple-django`_: A cookiecutter template for creating reusable Django projects quickly.
* `django-docker-bootstrap`_: Django development/production environment with docker, integrated with Postgres, NodeJS(React), Nginx, uWSGI.
* `cookiecutter-djangopackage`_: A template designed to create reusable third-party PyPI friendly Django apps. Documentation is written in tutorial format.
* `cookiecutter-django-cms`_: A template for Django CMS with simple Bootstrap 3 template. It has a quick start and deploy documentation.
* `cookiecutter-django-crud`_: A template to create a Django app with boilerplate CRUD around a model including a factory and tests.
* `cookiecutter-django-lborgav`_: Another cookiecutter template for Django project with Bootstrap 3 and FontAwesome 4
* `cookiecutter-django-paas`_: Django template ready to use in PAAS platforms like Heroku, OpenShift, etc..
* `cookiecutter-django-rest-framework`_: A template for creating reusable Django REST Framework packages.
* `cookiecutter-django-aws-eb`_: Get up and running with Django on AWS Elastic Beanstalk.
* `cookiecutter-wagtail`_ : A cookiecutter template for `Wagtail`_ CMS based sites.
* `wagtail-cookiecutter-foundation`_: A complete template for Wagtail CMS projects featuring `Zurb Foundation`_ 6, ansible provisioning and deployment , front-end dependency management with bower, modular apps to get your site up and running including photo_gallery, RSS feed etc.
* `django-starter`_: A Django template complete with vagrant and provisioning scripts - inspired by 12 factor apps and cookiecutter-django.
* `cookiecutter-django-gulp`_: A Cookiecutter template for integrating frontend development tools in Django projects.
* `wagtail-starter-kit`_: A cookiecutter complete with wagtail, django layout, vagrant, provisioning scripts, front end build system and more!
* `cookiecutter-django-herokuapp`_: A Django 1.7+ template optimized for Python 3 on Heroku.
* `cookiecutter-simple-django-cn`_: A simple Django templates for chinese.
* `cc_django_ember_app`_: For creating applications with Django and EmberJS
* `cc_project_app_drf`_: For creating REST apis based on the "project app" project architecture
* `cc_project_app_full_with_hooks`_: For creating Django projects using the "project app" project architecture
* `cc-automated-drf-template`_: A template + script that automatically creates your Django REST project with serializers, views, urls, and admin files based on your models file as input.
* `cookiecutter-django-foundation`_: Fork of `cookiecutter-django`_ based on `Zurb Foundation`_ 6 front-end framework
* `cookiecutter-django-ansible`_: Cookiecutter Django Ansible is a framework for jumpstarting an ansible project for provisioning a server that is ready for your *cookiecutter-django* application.
* `wemake-django-template`_: Bleeding edge Django template focused on code quality and security.

.. _`cookiecutter-django`: https://github.com/pydanny/cookiecutter-django
.. _`cookiecutter-django-rest`: https://github.com/agconti/cookiecutter-django-rest
.. _`cookiecutter-simple-django`: https://github.com/marcofucci/cookiecutter-simple-django
.. _`django-docker-bootstrap`: https://github.com/legios89/django-docker-bootstrap
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _`cookiecutter-django-cms`: https://github.com/palazzem/cookiecutter-django-cms
.. _`cookiecutter-django-crud`: https://github.com/wildfish/cookiecutter-django-crud
.. _`cookiecutter-django-lborgav`: https://github.com/lborgav/cookiecutter-django
.. _`cookiecutter-django-paas`: https://github.com/pbacterio/cookiecutter-django-paas
.. _`cookiecutter-django-rest-framework`: https://github.com/jpadilla/cookiecutter-django-rest-framework
.. _`cookiecutter-django-aws-eb`: https://github.com/dolphinkiss/cookiecutter-django-aws-eb
.. _`cookiecutter-wagtail`: https://github.com/torchbox/cookiecutter-wagtail
.. _`Wagtail`: https://github.com/torchbox/wagtail
.. _`wagtail-cookiecutter-foundation`: https://github.com/chrisdev/wagtail-cookiecutter-foundation
.. _`django-starter`: https://github.com/tkjone/django-starter
.. _`cookiecutter-django-gulp`: https://github.com/valerymelou/cookiecutter-django-gulp
.. _`wagtail-starter-kit`: https://github.com/tkjone/wagtail-starter-kit
.. _`cookiecutter-django-herokuapp`: https://github.com/dulaccc/cookiecutter-django-herokuapp
.. _`cookiecutter-simple-django-cn`: https://github.com/shenyushun/cookiecutter-simple-django-cn
.. _`cc_django_ember_app`: https://bitbucket.org/levit_scs/cc_django_ember_app
.. _`cc_project_app_drf`: https://bitbucket.org/levit_scs/cc_project_app_drf
.. _`cc_project_app_full_with_hooks`: https://bitbucket.org/levit_scs/cc_project_app_full_with_hooks
.. _`cc-automated-drf-template`: https://github.com/TAMU-CPT/cc-automated-drf-template
.. _`cookiecutter-django-foundation`: https://github.com/Parbhat/cookiecutter-django-foundation
.. _`Zurb Foundation`: http://foundation.zurb.com
.. _`cookiecutter-django-ansible`: https://github.com/HackSoftware/cookiecutter-django-ansible
.. _`wemake-django-template`: https://github.com/wemake-services/wemake-django-template

Python-Pyramid
^^^^^^^^^^^^^^

* `pyramid-cookiecutter-alchemy`_: A Cookiecutter (project template) for creating a Pyramid project using SQLite for persistent storage, SQLAlchemy for an ORM, URL dispatch for routing, and Jinja2 for templating.
* `pyramid-cookiecutter-starter`_: A Cookiecutter (project template) for creating a Pyramid starter project using URL dispatch for routing and either Jinja2, Chameleon, or Mako for templating.
* `pyramid-cookiecutter-zodb`_: A Cookiecutter (project template) for creating a Pyramid project using ZODB for persistent storage, traversal for routing, and Chameleon for templating.
* `substanced-cookiecutter`_: A cookiecutter (project template) for creating a Substance D starter project. Substance D is built on top of Pyramid.
* `cookiecutter-pyramid-talk-python-starter`_: An opinionated Cookiecutter template for creating Pyramid web applications starting way further down the development chain. This cookiecutter template will create a new Pyramid web application with email, sqlalchemy, rollbar, and way more integrated.

.. _`pyramid-cookiecutter-alchemy`: https://github.com/Pylons/pyramid-cookiecutter-alchemy
.. _`pyramid-cookiecutter-starter`: https://github.com/Pylons/pyramid-cookiecutter-starter
.. _`pyramid-cookiecutter-zodb`: https://github.com/Pylons/pyramid-cookiecutter-zodb
.. _`substanced-cookiecutter`: https://github.com/Pylons/substanced-cookiecutter
.. _`cookiecutter-pyramid-talk-python-starter`: https://github.com/mikeckennedy/cookiecutter-pyramid-talk-python-starter

Cookiecutter (meta)
~~~~~~~~~~~~~~~~~~~

Meta-templates for generating Cookiecutter project templates.

* `cookiecutter-template`_: Cookiecutter template for creating a... cookiecutter template...

.. _`cookiecutter-template`: https://github.com/eviweb/cookiecutter-template

Ansible
~~~~~~~

* `cookiecutter-molecule`_: Create `Molecule`_ roles following community best practices, with an already implemented test infrastructure leveraging `Molecule`_, Docker and Testinfra.
* `cookiecutter-ansible-role`_: A template to create ansible roles. Forget about file creation and focus on actions.
* `cookiecutter-ansible-role-ci`_: Create Ansible roles following best practices, with an already implemented test infrastructure leveraging Test-kitchen, Docker and InSpec.

.. _`cookiecutter-ansible-role`: https://github.com/iknite/cookiecutter-ansible-role
.. _`cookiecutter-ansible-role-ci`: https://github.com/ferrarimarco/cookiecutter-ansible-role
.. _`cookiecutter-molecule`: https://github.com/retr0h/cookiecutter-molecule

.. _`Molecule`: http://molecule.readthedocs.io/en/v2/

Git
~~~

* `cookiecutter-git`_: Git repo project template :clipboard:

.. _`cookiecutter-git`: https://github.com/NathanUrwin/cookiecutter-git


C
~~

* `bootstrap.c`_: A template for simple projects written in C with autotools.
* `cookiecutter-avr`_: A template for avr development.

.. _`bootstrap.c`: https://github.com/vincentbernat/bootstrap.c
.. _`cookiecutter-avr`: https://github.com/solarnz/cookiecutter-avr


C++
~~~

* `BoilerplatePP`_: A simple cmake template with unit testing for projects written in C++.
* `cookiecutter-dpf-effect`_: An audio plugin project template for the DISTRHO Plugin Framework (DPF)
* `cookiecutter-dpf-audiotk`_: An audio plugin project template for the DISTRHO Plugin Framework (DPF) and the Audio Toolkit (ATK) DSP library
* `cookiecutter-kata-gtest`_: A template for C++ test-driven development katas using the Google Test framework.
* `cookiecutter-kata-cpputest`_: A template for C++ test-driven-development katas using the CppUTest framework.

.. _`BoilerplatePP`: https://github.com/Paspartout/BoilerplatePP
.. _cookiecutter-dpf-effect: https://github.com/SpotlightKid/cookiecutter-dpf-effect
.. _cookiecutter-dpf-audiotk: https://github.com/SpotlightKid/cookiecutter-dpf-audiotk
.. _cookiecutter-kata-gtest: https://github.com/13coders/cookiecutter-kata-gtest
.. _cookiecutter-kata-cpputest: https://github.com/13coders/cookiecutter-kata-cpputest


C#
~~

* `cookiecutter-csharp-objc-binding`_: A template for generating a C# binding project for binding an Objective-C static library.

.. _`cookiecutter-csharp-objc-binding`: https://github.com/SandyChapman/cookiecutter-csharp-objc-binding


Common Lisp
~~~~~~~~~~~

* `cookiecutter-cl-project`_: A template for Common Lisp project with bootstrap script and Slime integration.

.. _`cookiecutter-cl-project`: https://github.com/svetlyak40wt/cookiecutter-cl-project

Elm
~~~

* `cookiecutter-elm`_: Elm based cookiecutter with basic html example.

.. _`cookiecutter-elm`: https://github.com/m-x-k/cookiecutter-elm.git


Golang
~~~~~~

* `cookiecutter-golang`_: A template to create new go based projects following best practices.

.. _`cookiecutter-golang`: https://github.com/lacion/cookiecutter-golang

Java
~~~~

* `cookiecutter-java`_: Cookiecutter for basic java application setup with gradle
* `cookiecutter-spring-boot`_: Cookiecutter for standard java spring boot gradle application
* `cookiecutter-android`_: Cookiecutter for Gradle-based Android projects

.. _`cookiecutter-java`: https://github.com/m-x-k/cookiecutter-java.git
.. _`cookiecutter-spring-boot`: https://github.com/m-x-k/cookiecutter-spring-boot.git
.. _`cookiecutter-android`: https://github.com/alexfu/cookiecutter-android


JS
~~

* `cookiecutter-es6-boilerplate`_: A cookiecutter for front end projects in ES6.
* `cookiecutter-webpack`_: A template for webpack 2 projects with hot reloading, babel es6 modules, and react.
* `cookiecutter-jquery`_: A jQuery plugin project template based on jQuery
  Boilerplate.
* `cookiecutter-jswidget`_: A project template for creating a generic front-end,
  non-jQuery JS widget packaged for multiple JS packaging systems.
* `cookiecutter-component`_: A template for a Component JS package.
* `cookiecutter-tampermonkey`_: A template for a TamperMonkey browser script.
* `cookiecutter-es6-package`_: A template for writing node packages using ES6 via babel.
* `cookiecutter-angular2`_: A template for modular angular2 with typescript apps.
* `CICADA`_: A template + script that automatically creates list/detail controllers and partials for an AngularJS frontend to connect to a DRF backend. Works well with `cc-automated-drf-template <https://github.com/TAMU-CPT/cc-automated-drf-template>`__.

.. _`cookiecutter-es6-boilerplate`: https://github.com/agconti/cookiecutter-es6-boilerplate
.. _`cookiecutter-webpack`: https://github.com/hzdg/cookiecutter-webpack
.. _`cookiecutter-jquery`: https://github.com/audreyr/cookiecutter-jquery
.. _`cookiecutter-jswidget`: https://github.com/audreyr/cookiecutter-jswidget
.. _`cookiecutter-component`: https://github.com/audreyr/cookiecutter-component
.. _`cookiecutter-tampermonkey`: https://github.com/christabor/cookiecutter-tampermonkey
.. _`cookiecutter-es6-package`: https://github.com/ratson/cookiecutter-es6-package
.. _`cookiecutter-angular2`: https://github.com/matheuspoleza/cookiecutter-angular2
.. _`CICADA`: https://github.com/TAMU-CPT/CICADA

Kotlin
~~~~~~

* `cookiecutter-kotlin-gradle`_: A bare-bones template for Gradle-based Kotlin projects.

.. _`cookiecutter-kotlin-gradle`: https://github.com/thomaslee/cookiecutter-kotlin-gradle


LaTeX/XeTeX
~~~~~~~~~~~

* `pandoc-talk`_: A cookiecutter template for giving talks with pandoc and XeTeX.
* `cookiecutter-latex-article`_: A LaTeX template geared towards academic use.
* `cookiecutter-beamer`_: A template for a LaTeX Beamer presentation.

.. _`pandoc-talk`: https://github.com/larsyencken/pandoc-talk
.. _`cookiecutter-latex-article`: https://github.com/Kreger51/cookiecutter-latex-article
.. _`cookiecutter-beamer`: https://github.com/luismartingil/cookiecutter-beamer


PHP
~~~

* `cookiecutter-mediawiki-extension`_: A template for MediaWiki extensions.

.. _`cookiecutter-mediawiki-extension`: https://github.com/JonasGroeger/cookiecutter-mediawiki-extension


Sublime Text
~~~~~~~~~~~~

* `cookiecutter-sublime-text-3-plugin`_: Sublime Text 3 plugin template with custom settings, commands, key bindings and main menu.
* `sublime-snippet-package-template`_: Template for Sublime Text packages containing snippets.

.. _`cookiecutter-sublime-text-3-plugin`: https://github.com/kkujawinski/cookiecutter-sublime-text-3-plugin
.. _`sublime-snippet-package-template`: https://github.com/agenoria/sublime-snippet-package-template

Berkshelf-Vagrant
~~~~~~~~~~~~~~~~~

* `slim-berkshelf-vagrant`_: A simple cookiecutter template with sane cookbook defaults for common vagrant/berkshelf cookbooks.

.. _`slim-berkshelf-vagrant`: https://github.com/mahmoudimus/cookiecutter-slim-berkshelf-vagrant


HTML
~~~~

* `cookiecutter-complexity`_: A cookiecutter for a Complexity static site with Bootstrap 3.
* `cookiecutter-reveal.js`_: A cookiecutter template for reveal.js presentations.
* `cookiecutter-tumblr-theme`_: A cookiecutter for a Tumblr theme project with GruntJS as concatenation tool.

.. _`cookiecutter-complexity`: https://github.com/audreyr/cookiecutter-complexity
.. _`cookiecutter-reveal.js`: https://github.com/keimlink/cookiecutter-reveal.js
.. _`cookiecutter-tumblr-theme`: https://github.com/relekang/cookiecutter-tumblr-theme


Scala
~~~~~

* `cookiecutter-scala`_: A cookiecutter template for a simple scala hello world application with a few libraries.
* `cookiecutter-scala-spark`_: A cookiecutter template for Apache Spark applications written in Scala.

.. _`cookiecutter-scala`: https://github.com/Plippe/cookiecutter-scala
.. _`cookiecutter-scala-spark`: https://github.com/jpzk/cookiecutter-scala-spark


6502 Assembly
~~~~~~~~~~~~~
* `cookiecutter-atari2600`_: A cookiecutter template for Atari2600 projects.

.. _`cookiecutter-atari2600`: https://github.com/joeyjoejoejr/cookiecutter-atari2600

Data Science
~~~~~~~~~~~~

* `widget-cookiecutter`_: A cookiecutter template for creating a custom Jupyter widget project.
* `cookiecutter-data-science`_: A logical, reasonably standardized, but flexible project structure for doing and sharing data science work in Python.  Full documentation available `here <http://drivendata.github.io/cookiecutter-data-science/>`__.
* `cookiecutter-r-data-analysis`_: Template for a R based workflow to docx (via Pandoc) and pdf (via LaTeX) reports.
* `cookiecutter-docker-science`_: Cookiecutter template for data scientists working in Docker containers.

.. _`widget-cookiecutter`: https://github.com/jupyter/widget-cookiecutter
.. _`cookiecutter-data-science`: https://github.com/drivendata/cookiecutter-data-science
.. _`cookiecutter-r-data-analysis`: https://github.com/bdcaf/cookiecutter-r-data-analysis
.. _`cookiecutter-docker-science`: https://github.com/docker-science/cookiecutter-docker-science

Reproducible Science
~~~~~~~~~~~~~~~~~~~~

* `cookiecutter-reproducible-science`_: A cookiecutter template to start a reproducible and transparent science project including data, models, analysis, and reports (i.e., your scientific paper) with close resemblances to the philosophy of Cookiecutter `Data Science`_.

.. _`cookiecutter-reproducible-science`: https://github.com/mkrapp/cookiecutter-reproducible-science

Data Driven Journalism
~~~~~~~~~~~~~~~~~~~~~~

* `cookiecutter-data-driven-journalism`_: A cookiecutter template to facilitate
  transparency in data journalism with consistant organisation of data
  journalism projects and some pre-populated files (including .gitignore,
  README, AUTHORS)

.. _`cookiecutter-data-driven-journalism`: https://github.com/jastark/cookiecutter-data-driven-journalism

Continuous Delivery
~~~~~~~~~~~~~~~~~~~

* `painless-continuous-delivery`_: A cookiecutter template for software development setups with continuous delivery baked in. Python (Django, Flask), and experimental PHP support.
* `cookiecutter-devenv`_: A template to add a development and ci environment to an existing project.

.. _`painless-continuous-delivery`: https://github.com/painless-software/painless-continuous-delivery
.. _`cookiecutter-devenv`: https://bitbucket.org/greenguavalabs/cookiecutter-devenv.git

Cloud Tools
~~~~~~~~~~~~

* `cookiecutter-tf-module`_: Cookiecutter template for building consistent Terraform modules.

.. _`cookiecutter-tf-module`: https://github.com/DualSpark/cookiecutter-tf-module

Tornado
~~~~~~~

* `cookiecutter-tornado`_: Cookiecutter template for Tornado based projects

.. _`cookiecutter-tornado`: https://github.com/hkage/cookiecutter-tornado

Other
~~~~~

* `cookiecutter-awesome`_: Cookiecutter to create an `awesome`_ list.
* `cookiecutter_dotfile`_: Template for a folder of dotfiles managed by stow.
* `cookiecutter-raml`_: Template for RAML v1.0 API documents.

.. _`cookiecutter-awesome`: https://github.com/Pawamoy/cookiecutter-awesome
.. _`cookiecutter_dotfile`: https://github.com/bdcaf/cookiecutter_dotfile
.. _`cookiecutter-raml`: https://github.com/genzj/cookiecutter-raml

.. _`awesome`: https://github.com/sindresorhus/awesome


Similar projects
----------------

* `Paste`_ has a create option that creates a skeleton project.

* `Diecutter`_: an API service that will give you back a configuration file from
  a template and variables.

* `Django`_'s `startproject` and `startapp` commands can take in a `--template`
  option.

* `python-packager`_: Creates Python packages from its own template, with
  configurable options.

* `Yeoman`_ has a Rails-inspired generator system that provides scaffolding
  for apps.

* `Pyramid`_'s `pcreate` command for creating Pyramid projects from scaffold templates.

* `mr.bob`_ is a filesystem template renderer, meant to deprecate tools such as
  paster and templer.

* `grunt-init`_ used to be built into Grunt and is now a standalone scaffolding tool
  to automate project creation.

* `scaffolt`_ consumes JSON generators with Handlebars support.

* `init-skeleton`_ clones or copies a repository, executes npm install and bower install and removes the .git directory.

* `Cog`_ python-based code generation toolkit developed by Ned Batchelder

* `Skaffold`_ python and json config based django/MVC generator, with some add-ons and integrations.

.. _`Paste`: http://pythonpaste.org/script/#paster-create
.. _`Diecutter`: https://github.com/novagile/diecutter
.. _`Django`: https://docs.djangoproject.com/en/1.9/ref/django-admin/#cmdoption-startapp--template
.. _`python-packager`: https://github.com/fcurella/python-packager
.. _`Yeoman`: https://github.com/yeoman/generator
.. _`Pyramid`: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/scaffolding.html
.. _`mr.bob`: https://github.com/iElectric/mr.bob
.. _`grunt-init`: https://github.com/gruntjs/grunt-init
.. _`scaffolt`: https://github.com/paulmillr/scaffolt
.. _`init-skeleton`: https://github.com/paulmillr/init-skeleton
.. _`Cog`: https://bitbucket.org/ned/cog
.. _`Skaffold`: https://github.com/christabor/Skaffold

.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/
.. _`PyCon 2016`: https://us.pycon.org/2016/sponsors/
.. _`BSD license`: https://github.com/audreyr/cookiecutter/blob/master/LICENSE

.. _`Cookiecutter on GitHub`: https://github.com/audreyr/cookiecutter
.. _`Troubleshooting`: http://cookiecutter.readthedocs.io/en/latest/troubleshooting.html
.. _`contributors`: https://github.com/audreyr/cookiecutter/blob/master/AUTHORS.rst
.. _`contributing instructions`: https://github.com/audreyr/cookiecutter/blob/master/CONTRIBUTING.rst
.. _`Stack Overflow`: http://stackoverflow.com/
.. _`File an issue`: https://github.com/audreyr/cookiecutter/issues?state=open
.. _`@audreyr`: https://github.com/audreyr
.. _`@pydanny`: https://github.com/pydanny
.. _`@michaeljoseph`: https://github.com/michaeljoseph
.. _`@pfmoore`: https://github.com/pfmoore
.. _`@hackebrot`: https://github.com/hackebrot
.. _`Gitter`: https://gitter.im/audreyr/cookiecutter
