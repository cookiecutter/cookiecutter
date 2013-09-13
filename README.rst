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
        # Then it'll create your Python package based on those values.
        $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

* Can also use it at the command line with a local template:

    .. code-block:: bash

        # Create project from the local cookiecutter-pypackage/ template
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

* If generating a project from a git repo template, you are prompted for input:

  - Prompts are the keys in `cookiecutter.json`.
  - Default responses are the values in `cookiecutter.json`.
  - Prompts are shown in order.

Additional Features in 0.7.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

0.7.0 is not out yet, but these features are in the master branch:

* Cross-platform support for `~/.cookiecutterrc` files:

    default_context:
        full_name: "Audrey Roy"
        email: "audreyr@gmail.com"
        github_username: "audreyr"
    cookiecutters_dir: "~/.cookiecutters/"

* Cookiecutters (cloned Cookiecutter project templates) are put into
  `~/.cookiecutters/` by default, or cookiecutters_dir if specified.

* In addition to git repos, you can also use cookiecutters directly from
  Mercurial repos on Bitbucket.

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
* `cookiecutter-django`_: A Django project template with Bootstrap 3, customizable users app, starter templates, and working user registration.
* `cookiecutter-djangopackage`_: A template designed to create reusable third-party PyPI friendly Django apps. Documentation is written in tutorial format.
* `cookiecutter-openstack`_: A template for an OpenStack project.
* `cookiecutter-docopt`_: A template for a Python command-line script that uses `docopt`_ for arguments parsing.

C
~~

* `bootstrap.c`_: A template for simple projects written in C with autotools.

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

HTML
~~~~

* `cookiecutter-complexity`_: A cookiecutter for a Complexity static site with Bootstrap 3.

.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`@audreyr`: https://github.com/audreyr/
.. _`cookiecutter-jquery`: https://github.com/audreyr/cookiecutter-jquery
.. _`cookiecutter-flask`: https://github.com/sloria/cookiecutter-flask
.. _`cookiecutter-django`: https://github.com/pydanny/cookiecutter-django
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _`bootstrap.c`: https://github.com/vincentbernat/bootstrap.c
.. _`cookiecutter-openstack`: https://github.com/openstack-dev/cookiecutter
.. _`cookiecutter-component`: https://github.com/audreyr/cookiecutter-component
.. _`cookiecutter-docopt`: https://github.com/sloria/cookiecutter-docopt
.. _`docopt`: http://docopt.org/
.. _`cookiecutter-jswidget`: https://github.com/audreyr/cookiecutter-jswidget
.. _`pandoc-talk`: https://github.com/larsyencken/pandoc-talk
.. _`cookiecutter-complexity`: https://github.com/audreyr/cookiecutter-complexity


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

.. _`Paste`: http://pythonpaste.org/script/#paster-create
.. _`Diecutter`: https://github.com/novagile/diecutter
.. _`Django`: https://docs.djangoproject.com/en/1.5/ref/django-admin/#django-admin-startproject
.. _`python-packager`: https://github.com/fcurella/python-packager
.. _`Yeoman`: https://github.com/yeoman/generator
.. _`Pyramid`: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/scaffolding.html
.. _`mr.bob`: https://github.com/iElectric/mr.bob

Community
---------

If you have questions, don't hesitate to ask by `filing an issue`_ with your
question. (Questions are often a good indicator of places where the docs can be
improved :)

Development on Cookiecutter is community-driven. Huge thanks to all the
`contributors`_ who have pitched in to help make Cookiecutter an even better
tool.

Everyone is invited to contribute. Read the `contributing instructions`_, then
get started.

All members of the Cookiecutter community (end users, project template
maintainers, contributors, etc.) are invited to join the `Cookiecutter Gittip community`_.

.. _`contributors`: https://github.com/audreyr/cookiecutter/blob/master/AUTHORS.rst
.. _`contributing instructions`: https://github.com/audreyr/cookiecutter/blob/master/CONTRIBUTING.rst
.. _`filing an issue`: https://github.com/audreyr/cookiecutter/issues?state=open
.. _`Cookiecutter Gittip community`: https://www.gittip.com/for/cookiecutter/
