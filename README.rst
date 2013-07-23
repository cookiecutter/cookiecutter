=============
Cookiecutter
=============

.. image:: https://badge.fury.io/py/cookiecutter.png
    :target: http://badge.fury.io/py/cookiecutter
    
.. image:: https://travis-ci.org/audreyr/cookiecutter.png?branch=master
        :target: https://travis-ci.org/audreyr/cookiecutter

.. image:: https://pypip.in/d/cookiecutter/badge.png
        :target: https://crate.io/packages/cookiecutter?version=latest

A command-line utility that creates projects from project templates, e.g.
creating a Python package project from a Python package project template.

* Documentation: http://cookiecutter.rtfd.org
* GitHub: https://github.com/audreyr/cookiecutter
* Free software: BSD license
* PyPI: https://pypi.python.org/pypi/cookiecutter

Features
--------

* Simple command line usage.
* Works with any type of text file.
* Directory names and filenames can be templated. For example::

    {{project.repo_name}}/{{project.repo_name}}/{{project.repo_name}}.py

* Supports unlimited levels of directory nesting.
* Simply define your template variables in a JSON file. For example::

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

* All templating is done with Jinja2. Cookiecutter simply renders a directory
  of Jinja2 templates to files, including rendering the dir names and filenames.

Cookiecutter Project Templates
------------------------------

Here is a list of the Cookiecutter project templates that exist as of now:

* `cookiecutter-pypackage`_: `@audreyr`_'s ultimate Python package project 
  template.

Make your own, then submit a pull request adding yours to this list!

.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`@audreyr`: https://github.com/audreyr/

Similar projects
----------------
    
* `Paste`_ has a create option that creates a skeleton project.

* `Diecutter`_: an API service that will give you back a configuration file from
  a template and variables. 
  
* `Django`_'s `startproject` and `startapp` commands can take in a `--template`
  option.

* `python-packager`_: Creates Python packages from its own template, with
  configurable options.

.. _`Paste`: http://pythonpaste.org/script/#paster-create
.. _`Diecutter`: https://github.com/novagile/diecutter
.. _`Django`: https://docs.djangoproject.com/en/1.5/ref/django-admin/#django-admin-startproject
.. _`python-packager`: https://github.com/fcurella/python-packager