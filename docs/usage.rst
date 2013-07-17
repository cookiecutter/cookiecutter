=====
Usage
=====

Grab a Cookiecutter template
----------------------------

First, clone a Cookiecutter project template::

    $ git clone git@github.com:audreyr/cookiecutter-pypackage.git
    $ cd cookiecutter-pypackage

Make your changes
-----------------

Modify the variables defined in `json`.

Open up the skeleton project. If you need to change it around a bit, do so.

You probably also want to create a repo, name it differently, and push it as 
your own new Cookiecutter project template, for handy future use.

Generate your project
---------------------

Then generate your project from the project template::

    $ cookiecutter {{project.repo_name}}/ {{project.repo_name}}/

The first argument is the input dir, the second is the output dir.

Try it out!
