=============
Cookiecutter
=============

.. image:: https://img.shields.io/pypi/v/cookiecutter.svg
        :target: https://pypi.python.org/pypi/cookiecutter

.. image:: https://travis-ci.org/audreyr/cookiecutter.png?branch=master
        :target: https://travis-ci.org/audreyr/cookiecutter

.. image:: https://ci.appveyor.com/api/projects/status/github/audreyr/cookiecutter?branch=master
        :target: https://ci.appveyor.com/project/audreyr/cookiecutter/branch/master

.. image:: https://img.shields.io/pypi/dm/cookiecutter.svg
        :target: https://pypi.python.org/pypi/cookiecutter

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

A command-line utility that creates projects from **cookiecutters** (project
templates), e.g. creating a Python package project from a Python package project template.

* Documentation: http://cookiecutter.rtfd.org
* GitHub: https://github.com/audreyr/cookiecutter
* Free software: BSD license
* PyPI: https://pypi.python.org/pypi/cookiecutter

.. image:: https://raw.github.com/audreyr/cookiecutter/aa309b73bdc974788ba265d843a65bb94c2e608e/cookiecutter_medium.png

Features
--------

Did someone say features?

* Cross-platform: Windows, Mac, and Linux are officially supported.

* Works with Python 2.7, 3.3, 3.4, 3.5, and PyPy. *(But you don't have to know/write Python
  code to use Cookiecutter.)*

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

* Can also use it at the command line with a local template:

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

* Simply define your template variables in a `cookiecutter.json` file. For example:

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

* Unless you suppress it with `--no-input`, you are prompted for input:

  - Prompts are the keys in `cookiecutter.json`.
  - Default responses are the values in `cookiecutter.json`.
  - Prompts are shown in order.

* Cross-platform support for `~/.cookiecutterrc` files:

    .. code-block:: yaml

        default_context:
            full_name: "Audrey Roy"
            email: "audreyr@gmail.com"
            github_username: "audreyr"
        cookiecutters_dir: "~/.cookiecutters/"

* Cookiecutters (cloned Cookiecutter project templates) are put into
  `~/.cookiecutters/` by default, or cookiecutters_dir if specified.

* You can use local cookiecutters, or remote cookiecutters directly from Git
  repos or from Mercurial repos on Bitbucket.

* Default context: specify key/value pairs that you want used as defaults
  whenever you generate a project

* Direct access to the Cookiecutter API allows for injection of extra context.

* Pre- and post-generate hooks: Python or shell scripts to run before or after
  generating a project.

* Paths to local projects can be specified as absolute or relative.

* Projects are always generated to your current directory.

Available Cookiecutters
-----------------------

Here is a list of **cookiecutters** (aka Cookiecutter project templates) for you to use or fork.

Make your own, then submit a pull request adding yours to this list!

Python
~~~~~~
* `cookiecutter-pypackage`_: `@audreyr`_'s ultimate Python package project
  template.
* `cookiecutter-flask`_ : A Flask template with Bootstrap 3, starter templates, and working user registration.
* `cookiecutter-flask-foundation`_ : Flask Template with caching, forms, sqlalchemy and unit-testing.
* `cookiecutter-bottle`_ : A cookiecutter template for creating reusable Bottle projects quickly.
* `cookiecutter-openstack`_: A template for an OpenStack project.
* `cookiecutter-docopt`_: A template for a Python command-line script that uses `docopt`_ for arguments parsing.
* `cookiecutter-quokka-module`_: A template to create a blueprint module for Quokka Flask CMS.
* `cookiecutter-kivy`_: A template for NUI applications built upon the kivy python-framework.
* `cookiedozer`_: A template for Python Kivy apps ready to be deployed to android devices with Buildozer.
* `cookiecutter-pypackage-minimal`_: A mimimal Python package template.
* `cookiecutter-ansible-role`_: A template to create ansible roles. Forget about file creation and focus on actions.
* `cookiecutter-pylibrary`_: An intricate template designed to quickly get started with good testing and packaging (working configuration for Tox, Pytest, Travis-CI, Coveralls, AppVeyor, Sphinx docs, isort, bumpversion, packaging checks etc).
* `cookiecutter-pyvanguard`_: A template for cutting edge Python development. `Invoke`_, pytest, bumpversion, and Python 2/3 compatability.
* `Python-iOS-template`_: A template to create a Python project that will run on iOS devices.
* `Python-Android-template`_: A template to create a Python project that will run on Android devices.
* `cookiecutter-tryton`_: A template for creating tryton modules.
* `cookiecutter-pytest-plugin`_: Minimal Cookiecutter template for authoring `pytest`_ plugins that help you to write better programs.
* `cookiecutter-tapioca`_: A Template for building `tapioca-wrapper`_ based web API wrappers (clients).
* `cookiecutter-sublime-text-3-plugin`_: Sublime Text 3 plugin template with custom settings, commands, key bindings and main menu.
* `cookiecutter-muffin`_: A Muffin template with Bootstrap 3, starter templates, and working user registration.
* `cookiecutter-octoprint-plugin`_: A template for building plugins for `OctoPrint`_.

Python-Django
^^^^^^^^^^^^^

* `cookiecutter-django`_: A bleeding edge Django project template with Bootstrap 4, customizable users app, starter templates,  working user registration, celery setup, and much more.
* `cookiecutter-django-rest`_: For creating REST apis for mobile and web applications.
* `cookiecutter-simple-django`_: A cookiecutter template for creating reusable Django projects quickly.
* `cookiecutter-djangopackage`_: A template designed to create reusable third-party PyPI friendly Django apps. Documentation is written in tutorial format.
* `cookiecutter-django-cms`_: A template for Django CMS with simple Bootstrap 3 template. It has a quick start and deploy documentation.
* `cookiecutter-djangocms-plugin`_: A template to get started with custom plugins for django-cms
* `cookiecutter-django-crud`_: A template to create a Django app with boilerplate CRUD around a model including a factory and tests.
* `cookiecutter-django-lborgav`_: Another cookiecutter template for Django project with Booststrap 3 and FontAwesome 4
* `cookiecutter-django-paas`_: Django template ready to use in SAAS platforms like Heroku, OpenShift, etc..
* `cookiecutter-django-rest-framework`_: A template for creating reusable Django REST Framework packages.
* `cookiecutter-wagtail`_ : A cookiecutter template for `Wagtail`_ CMS based sites.

C
~~

* `bootstrap.c`_: A template for simple projects written in C with autotools.
* `cookiecutter-avr`_: A template for avr development.

C++
~~~

* `BoilerplatePP`_: A simple cmake template with unit testing for projects written in C++.

C#
~~

* `cookiecutter-csharp-objc-binding`_: A template for generating a C# binding project for binding an Objective-C static library.

.. _`cookiecutter-csharp-objc-binding`: https://github.com/SandyChapman/cookiecutter-csharp-objc-binding

Common Lisp
~~~~~~~~~~~

* `cookiecutter-cl-project`_: A template for Common Lisp project with bootstrap script and Slime integration.

JS
~~

* `cookiecutter-es6-boilerplate`_: A cookiecutter for front end projects in ES6.
* `cookiecutter-jquery`_: A jQuery plugin project template based on jQuery
  Boilerplate.
* `cookiecutter-jswidget`_: A project template for creating a generic front-end,
  non-jQuery JS widget packaged for multiple JS packaging systems.
* `cookiecutter-component`_: A template for a Component JS package.
* `cookiecutter-tampermonkey`_: A template for a TamperMonkey browser script.

LaTeX/XeTeX
~~~~~~~~~~~

* `pandoc-talk`_: A cookiecutter template for giving talks with pandoc and XeTeX.

* `cookiecutter-latex-article`_: A LaTeX template geared towards academic use.

* `cookiecutter-beamer`_: A template for a LaTeX Beamer presentation.


Berkshelf-Vagrant
~~~~~~~~~~~~~~~~~

* `slim-berkshelf-vagrant`_: A simple cookiecutter template with sane cookbook defaults for common vagrant/berkshelf cookbooks.


HTML
~~~~

* `cookiecutter-complexity`_: A cookiecutter for a Complexity static site with Bootstrap 3.
* `cookiecutter-tumblr-theme`_: A cookiecutter for a Tumblr theme project with GruntJS as concatination tool.

.. _`cookiecutter-django-rest`: https://github.com/agconti/cookiecutter-django-rest
.. _`cookiecutter-es6-boilerplate`: https://github.com/agconti/cookiecutter-es6-boilerplate
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`cookiecutter-jquery`: https://github.com/audreyr/cookiecutter-jquery
.. _`cookiecutter-flask`: https://github.com/sloria/cookiecutter-flask
.. _`cookiecutter-flask-foundation`: https://github.com/JackStouffer/cookiecutter-Flask-Foundation
.. _`cookiecutter-bottle`: https://github.com/avelino/cookiecutter-bottle
.. _`cookiecutter-simple-django`: https://github.com/marcofucci/cookiecutter-simple-django
.. _`cookiecutter-django`: https://github.com/pydanny/cookiecutter-django
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _`cookiecutter-django-cms`: https://github.com/palazzem/cookiecutter-django-cms
.. _`cookiecutter-djangocms-plugin`: https://github.com/mishbahr/cookiecutter-djangocms-plugin
.. _`cookiecutter-django-crud`: https://github.com/wildfish/cookiecutter-django-crud
.. _`cookiecutter-quokka-module`: https://github.com/pythonhub/cookiecutter-quokka-module
.. _`cookiecutter-django-lborgav`: https://github.com/lborgav/cookiecutter-django
.. _`cookiecutter-django-paas`: https://github.com/pbacterio/cookiecutter-django-paas
.. _`cookiecutter-kivy`: https://github.com/hackebrot/cookiecutter-kivy
.. _`cookiedozer`: https://github.com/hackebrot/cookiedozer
.. _`cookiecutter-pypackage-minimal`: https://github.com/borntyping/cookiecutter-pypackage-minimal
.. _`cookiecutter-ansible-role`: https://github.com/iknite/cookiecutter-ansible-role
.. _`bootstrap.c`: https://github.com/vincentbernat/bootstrap.c
.. _`BoilerplatePP`: https://github.com/Paspartout/BoilerplatePP
.. _`cookiecutter-openstack`: https://github.com/openstack-dev/cookiecutter
.. _`cookiecutter-component`: https://github.com/audreyr/cookiecutter-component
.. _`cookiecutter-tampermonkey`: https://github.com/christabor/cookiecutter-tampermonkey
.. _`cookiecutter-docopt`: https://github.com/sloria/cookiecutter-docopt
.. _`docopt`: http://docopt.org/
.. _`cookiecutter-jswidget`: https://github.com/audreyr/cookiecutter-jswidget
.. _`pandoc-talk`: https://github.com/larsyencken/pandoc-talk
.. _`cookiecutter-latex-article`: https://github.com/Kreger51/cookiecutter-latex-article
.. _`cookiecutter-complexity`: https://github.com/audreyr/cookiecutter-complexity
.. _`cookiecutter-cl-project`: https://github.com/svetlyak40wt/cookiecutter-cl-project
.. _`slim-berkshelf-vagrant`: https://github.com/mahmoudimus/cookiecutter-slim-berkshelf-vagrant
.. _`cookiecutter-avr`: https://github.com/solarnz/cookiecutter-avr
.. _`cookiecutter-tumblr-theme`: https://github.com/relekang/cookiecutter-tumblr-theme
.. _`cookiecutter-pylibrary`: https://github.com/ionelmc/cookiecutter-pylibrary
.. _`cookiecutter-pyvanguard`: https://github.com/robinandeer/cookiecutter-pyvanguard
.. _`Python-iOS-template`: https://github.com/pybee/Python-iOS-template
.. _`Python-Android-template`: https://github.com/pybee/Python-Android-template
.. _`Invoke`: http://invoke.readthedocs.org/en/latest/
.. _`cookiecutter-django-rest-framework`: https://github.com/jpadilla/cookiecutter-django-rest-framework
.. _`cookiecutter-tryton`: https://github.com/fulfilio/cookiecutter-tryton
.. _`cookiecutter-beamer`: https://github.com/luismartingil/cookiecutter-beamer
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`pytest`: http://pytest.org/latest/
.. _`cookiecutter-tapioca`: https://github.com/vintasoftware/cookiecutter-tapioca
.. _`tapioca-wrapper`: https://github.com/vintasoftware/tapioca-wrapper
.. _`cookiecutter-sublime-text-3-plugin`: https://github.com/kkujawinski/cookiecutter-sublime-text-3-plugin
.. _`cookiecutter-muffin`: https://github.com/drgarcia1986/cookiecutter-muffin
.. _`cookiecutter-wagtail`: https://github.com/torchbox/cookiecutter-wagtail
.. _`Wagtail`: https://github.com/torchbox/wagtail
.. _`cookiecutter-octoprint-plugin`: https://github.com/OctoPrint/cookiecutter-octoprint-plugin
.. _`OctoPrint`: https://github.com/foosel/OctoPrint

Scala
~~~~~

* `cookiecutter-scala-spark`_: A cookiecutter template for Apache Spark applications written in Scala.

.. _`cookiecutter-scala-spark`: https://github.com/jpzk/cookiecutter-scala-spark

6502 Assembly
~~~~~~~~~~~~~
* `cookiecutter-atari2600`_: A cookiecutter template for Atari2600 projects.

.. _`cookiecutter-atari2600`: https://github.com/joeyjoejoejr/cookiecutter-atari2600

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
.. _`Django`: https://docs.djangoproject.com/en/1.5/ref/django-admin/#django-admin-startproject
.. _`python-packager`: https://github.com/fcurella/python-packager
.. _`Yeoman`: https://github.com/yeoman/generator
.. _`Pyramid`: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/scaffolding.html
.. _`mr.bob`: https://github.com/iElectric/mr.bob
.. _`grunt-init`: https://github.com/gruntjs/grunt-init
.. _`scaffolt`: https://github.com/paulmillr/scaffolt
.. _`init-skeleton`: https://github.com/paulmillr/init-skeleton
.. _`Cog`: https://bitbucket.org/ned/cog
.. _`Skaffold`: https://github.com/christabor/Skaffold


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
* Join the `Cookiecutter Gittip community`_.

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

Code of Conduct
---------------

Everyone interacting in the Cookiecutter project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.

.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/

.. _`Cookiecutter on GitHub`: https://github.com/audreyr/cookiecutter
.. _`Troubleshooting`: http://cookiecutter.readthedocs.org/en/latest/troubleshooting.html
.. _`contributors`: https://github.com/audreyr/cookiecutter/blob/master/AUTHORS.rst
.. _`contributing instructions`: https://github.com/audreyr/cookiecutter/blob/master/CONTRIBUTING.rst
.. _`Stack Overflow`: http://stackoverflow.com/
.. _`File an issue`: https://github.com/audreyr/cookiecutter/issues?state=open
.. _`Cookiecutter Gittip community`: https://www.gittip.com/for/cookiecutter/
.. _`@audreyr`: https://github.com/audreyr
.. _`@pydanny`: https://github.com/pydanny
.. _`@michaeljoseph`: https://github.com/michaeljoseph
.. _`@pfmoore`: https://github.com/pfmoore
.. _`@hackebrot`: https://github.com/hackebrot
.. _`Gitter`: https://gitter.im/audreyr/cookiecutter
