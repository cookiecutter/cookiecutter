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


A command-line utility that creates projects from project templates, e.g.
creating a Python package project from a Python package project template.

* Documentation: http://cookiecutter.rtfd.org
* GitHub: https://github.com/audreyr/cookiecutter
* Free software: BSD license
* PyPI: https://pypi.python.org/pypi/cookiecutter

Features
--------

Did someone say features? Cookiecutter's got more features than you can shake
a stick at!

* Works with Python 2.6, 2.7, 3.3, and PyPy.

* Simple command line usage::
    
    # Create project from the cookiecutter-pypackage.git repo template
    # You'll be prompted to enter values.
    # Then it'll create your Python package based on those values.
    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

* Can also use it at the command line with a local template::

    # Create project from the local cookiecutter-pypackage/ template
    $ cookiecutter cookiecutter-pypackage/

* Or use it from Python::

    from cookiecutter.main import cookiecutter
    
    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')

* Directory names and filenames can be templated. For example::

    {{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}.py

* Supports unlimited levels of directory nesting.

* All templating is done with Jinja2.

* Project templates can be in any programming language or markup format:
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name 
  it. You can use multiple languages in the same project template.

* Simply define your template variables in a `cookiecutter.json` file. For example::

    {
    	"full_name": "Audrey Roy",
    	"email": "audreyr@gmail.com",
    	"project_name": "A Lot of Effort",
    	"repo_name": "alotofeffort",
    	"project_short_description": "Deploy static HTML sites to S3 with the simple 'alotofeffort' command.",
    	"release_date": "2013-07-10",
    	"year": "2013",
    	"version": "0.1.1"
    }

* If generating a project from a git repo template, you are prompted for input:

  - Prompts are the keys in `cookiecutter.json`.
  - Default responses are the values in `cookiecutter.json`.
  - Prompts are shown in order (thanks to those handy OrderedDicts!)

Available Templates
-------------------

Here is a list of the working Cookiecutter project templates that exist:

* `cookiecutter-pypackage`_: `@audreyr`_'s ultimate Python package project 
  template.
* `cookiecutter-jquery`_: A jQuery plugin project template based on jQuery
  Boilerplate.

Make your own, then submit a pull request adding yours to this list!

.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`@audreyr`: https://github.com/audreyr/
.. _`cookiecutter-jquery`: https://github.com/audreyr/cookiecutter-jquery

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

.. _`Paste`: http://pythonpaste.org/script/#paster-create
.. _`Diecutter`: https://github.com/novagile/diecutter
.. _`Django`: https://docs.djangoproject.com/en/1.5/ref/django-admin/#django-admin-startproject
.. _`python-packager`: https://github.com/fcurella/python-packager
.. _`Yeoman`: https://github.com/yeoman/generator
