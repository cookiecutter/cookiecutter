=============
Cookiecutter
=============

.. image:: https://badge.fury.io/py/cookiecutter.png
    :target: http://badge.fury.io/py/cookiecutter

.. image:: https://travis-ci.org/audreyr/cookiecutter.png?branch=master
        :target: https://travis-ci.org/audreyr/cookiecutter

.. image:: https://pypip.in/d/cookiecutter/badge.png
        :target: https://crate.io/packages/cookiecutter?version=latest

.. image:: https://coveralls.io/repos/audreyr/cookiecutter/badge.png?branch=master
        :target: https://coveralls.io/r/audreyr/cookiecutter?branch=master


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

* Works with Python 2.6, 2.7, 3.3, and PyPy. *(But you don't have to know/write Python
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
        $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

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

    .. code-block:: guess

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
* `cookiecutter-flask-env`_: A lucuma-flavored flask app template.
* `cookiecutter-simple-django`_: A cookiecutter template for creating reusable Django projects quickly.
* `cookiecutter-django`_: A bleeding edge Django project template with Bootstrap 3, customizable users app, starter templates, and working user registration.
* `cookiecutter-djangopackage`_: A template designed to create reusable third-party PyPI friendly Django apps. Documentation is written in tutorial format.
* `cookiecutter-django-cms`_: A template for Django CMS with simple Bootstrap 3 template. It has a quick start and deploy documentation.
* `cookiecutter-openstack`_: A template for an OpenStack project.
* `cookiecutter-docopt`_: A template for a Python command-line script that uses `docopt`_ for arguments parsing.
* `cookiecutter-django-crud`_: A template to create a Django app with boilerplate CRUD around a model including a factory and tests.
* `cookiecutter-quokka-module`_: A template to create a blueprint module for Quokka Flask CMS.
* `cookiecutter-django-lborgav`_: Another cookiecutter template for Django project with Booststrap 3 and FontAwesome 4.
* `cookiecutter-django-paas`_: Django template ready to use in SAAS platforms like Heroku, OpenShift, etc..
* `cookiecutter-kivy`_: A template for NUI applications built upon the kivy python-framework.

C
~~

* `bootstrap.c`_: A template for simple projects written in C with autotools.
* `cookiecutter-avr`_: A template for avr development.

Common Lisp
~~~~~~~~~~~

* `cookiecutter-cl-project`_: A template for Common Lisp project with bootstrap script and Slime integration.

JS
~~

* `cookiecutter-jquery`_: A jQuery plugin project template based on jQuery
  Boilerplate.
* `cookiecutter-jswidget`_: A project template for creating a generic front-end,
  non-jQuery JS widget packaged for multiple JS packaging systems.
* `cookiecutter-component`_: A template for a Component JS package.

LaTeX/XeTeX
~~~~~~~~~~~

* `pandoc-talk`_: A cookiecutter template for giving talks with pandoc and XeTeX.


Berkshelf-Vagrant
~~~~~~~~~~~~~~~~~

* `slim-berkshelf-vagrant`_: A simple cookiecutter template with sane cookbook defaults for common vagrant/berkshelf cookbooks.


HTML
~~~~

* `cookiecutter-complexity`_: A cookiecutter for a Complexity static site with Bootstrap 3.
* `cookiecutter-tumblr-theme`_: A cookiecutter for a Tumblr theme project with GruntJS as concatination tool.

.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`@audreyr`: https://github.com/audreyr/
.. _`cookiecutter-jquery`: https://github.com/audreyr/cookiecutter-jquery
.. _`cookiecutter-flask`: https://github.com/sloria/cookiecutter-flask
.. _`cookiecutter-flask-env`: https://github.com/lucuma/cookiecutter-flask-env
.. _`cookiecutter-simple-django`: https://github.com/marcofucci/cookiecutter-simple-django
.. _`cookiecutter-django`: https://github.com/pydanny/cookiecutter-django
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _`cookiecutter-django-cms`: https://github.com/palazzem/cookiecutter-django-cms
.. _`cookiecutter-django-crud`: https://github.com/wildfish/cookiecutter-django-crud
.. _`cookiecutter-quokka-module`: https://github.com/pythonhub/cookiecutter-quokka-module
.. _`cookiecutter-django-lborgav`: https://github.com/lborgav/cookiecutter-django
.. _`cookiecutter-django-paas`: https://github.com/pbacterio/cookiecutter-django-paas
.. _`cookiecutter-kivy`: https://github.com/hackebrot/cookiecutter-kivy
.. _`bootstrap.c`: https://github.com/vincentbernat/bootstrap.c
.. _`cookiecutter-openstack`: https://github.com/openstack-dev/cookiecutter
.. _`cookiecutter-component`: https://github.com/audreyr/cookiecutter-component
.. _`cookiecutter-docopt`: https://github.com/sloria/cookiecutter-docopt
.. _`docopt`: http://docopt.org/
.. _`cookiecutter-jswidget`: https://github.com/audreyr/cookiecutter-jswidget
.. _`pandoc-talk`: https://github.com/larsyencken/pandoc-talk
.. _`cookiecutter-complexity`: https://github.com/audreyr/cookiecutter-complexity
.. _`cookiecutter-cl-project`: https://github.com/svetlyak40wt/cookiecutter-cl-project
.. _`slim-berkshelf-vagrant`: https://github.com/mahmoudimus/cookiecutter-slim-berkshelf-vagrant
.. _`cookiecutter-avr`: https://github.com/solarnz/cookiecutter-avr
.. _`cookiecutter-tumblr-theme`: https://github.com/relekang/cookiecutter-tumblr-theme


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

Community
---------

Stuck? Try one of the following:

* See the `Troubleshooting`_ page.
* Ask for help on `Stack Overflow`_.
* You are strongly encouraged to `file an issue`_ about the problem, even if
  it's just "I can't get it to work on this cookiecutter" with a link to your
  cookiecutter. Don't worry about naming/pinpointing the issue properly.
* Ask for help in #cookiecutter if you must (but please try one of the other
  options first, so that others can benefit from the discussion)

Development on Cookiecutter is community-driven:

* Huge thanks to all the `contributors`_ who have pitched in to help make
  Cookiecutter an even better tool.
* Everyone is invited to contribute. Read the `contributing instructions`_,
  then get started.

Connect with other Cookiecutter contributors and users in IRC:

* #cookiecutter on irc.freenode.net (note: due to work and commitments,
  `@audreyr`_ might not always be available)

Encouragement is unbelievably motivating. If you want more work done on
Cookiecutter, show support:

* Star `Cookiecutter on GitHub`_.
* Please, please join the `Cookiecutter Gittip community`_.

Got criticism or complaints?

* `File an issue`_ so that Cookiecutter can be improved. Be friendly
  and constructive about what could be better. Make detailed suggestions.
* **Keep us in the loop so that we can help.** For example, if you are
  discussing problems with Cookiecutter on a mailing list, `file an issue`_
  where you link to the discussion thread and/or cc `audreyr@gmail.com` on
  the email.
* Be encouraging. A comment like "This function ought to be rewritten like
  this" is much more likely to result in action than a comment like "Eww, look
  how bad this function is."

Waiting for a response to an issue/question?

* Be patient and persistent. All issues are on `audreyr`_'s radar and will be
  considered thoughtfully, but due to the growing to-do list/free time ratio,
  it may take time for a response. If urgent, it's fine to ping `audreyr`_
  in the issue with a reminder.
* Ask others to comment, discuss, review, etc.
* Search the Cookiecutter repo for issues related to yours.
* Need a fix/feature/release/help urgently, and can't wait? `audreyr`_ is
  available hourly for consultation or custom development.

.. _`Cookiecutter on GitHub`: https://github.com/audreyr/cookiecutter
.. _`Troubleshooting`: http://cookiecutter.readthedocs.org/en/latest/troubleshooting.html
.. _`contributors`: https://github.com/audreyr/cookiecutter/blob/master/AUTHORS.rst
.. _`contributing instructions`: https://github.com/audreyr/cookiecutter/blob/master/CONTRIBUTING.rst
.. _`Stack Overflow`: http://stackoverflow.com/
.. _`File an issue`: https://github.com/audreyr/cookiecutter/issues?state=open
.. _`Cookiecutter Gittip community`: https://www.gittip.com/for/cookiecutter/
.. _`audreyr`: https://github.com/audreyr
