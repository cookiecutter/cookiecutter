=====
Usage
=====

Grab a Cookiecutter template
----------------------------

First, clone a Cookiecutter project template::

    $ git clone git@github.com:audreyr/cookiecutter-pypackage.git

Make your changes
-----------------

Modify the variables defined in `cookiecutter.json`.

Open up the skeleton project. If you need to change it around a bit, do so.

You probably also want to create a repo, name it differently, and push it as 
your own new Cookiecutter project template, for handy future use.

Generate your project
---------------------

Then generate your project from the project template::

    $ cookiecutter cookiecutter-pypackage/

The only argument is the input directory. (The output directory is generated
by rendering that, and it can't be the same as the input directory.)

.. note:: see :ref:`command_line_options` for extra command line arguments

Try it out!



Works directly with git repos too
---------------------------------

To create a project from the cookiecutter-pypackage.git repo template::

    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

You will be prompted to enter a bunch of project config values. (These are
defined in the project's `cookiecutter.json`.

Then, Cookiecutter will generate a project from the template, using the values
that you entered. It will be placed in your current directory.

And if you want to specify a branch you can do that with::

    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git --checkout develop

Keeping your cookiecutters organized
------------------------------------

As of the upcoming Cookiecutter 0.7.0 release:

* Whenever you generate a project with a cookiecutter, the resulting project
  is output to your current directory.

* Your cloned cookiecutters are stored by default in your `~/.cookiecutters/`
  directory (or Windows equivalent). The location is configurable: see
  :doc:`advanced_usage` for details.

Pre-0.7.0, this is how it worked:

* Whenever you generate a project with a cookiecutter, the resulting project
  is output to your current directory.

* Cloned cookiecutters were not saved locally.

