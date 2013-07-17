=============
Cookiecutter
=============

A command-line utility that creates projects from project templates. Renders a
directory of Jinja2 templates to files.

* Documentation: http://cookiecutter.rtfd.org
* GitHub: https://github.com/audreyr/cookiecutter
* Free software: BSD license
* PyPI: https://pypi.python.org/pypi/cookiecutter

Features
--------

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
    	"travis_ci_username": "audreyr",
    	"release_date": "2013-07-10",
    	"year": "2013",
    	"version": "0.1.1"
    }

Cookiecutter Project Templates
------------------------------

Here is a list of the Cookiecutter project templates that exist as of now:

* **cookiecutter-pypackage**: @audreyr's ultimate Python package project 
  template. https://github.com/audreyr/cookiecutter-pypackage

Make your own, then submit a pull request adding yours to this list!

Similar projects
----------------
    
* Paste has a create option that creates a skeleton project: 
  http://pythonpaste.org/script/#paster-create

* Diecutter: an API service that will give you back a configuration file from
  a template and variables. https://github.com/novagile/diecutter
  
* Django's `startproject` and `startapp` commands can take in a `--template`
  option: https://docs.djangoproject.com/en/1.5/ref/django-admin/#django-admin-startproject
