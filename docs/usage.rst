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



Works directly with git and hg (mercurial) repos too
------------------------------------------------------

To create a project from the cookiecutter-pypackage.git repo template::

    $ cookiecutter gh:audreyr/cookiecutter-pypackage

Cookiecutter knows abbreviations for Github (``gh``) and Bitbucket (``bb``)
projects, but you can also give it the full URL to any repository::

    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git
    $ cookiecutter git+ssh://git@github.com/audreyr/cookiecutter-pypackage.git
    $ cookiecutter hg+ssh://hg@bitbucket.org/audreyr/cookiecutter-pypackage


You will be prompted to enter a bunch of project config values. (These are
defined in the project's `cookiecutter.json`.)

Then, Cookiecutter will generate a project from the template, using the values
that you entered. It will be placed in your current directory.

And if you want to specify a branch you can do that with::

    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git --checkout develop

Works with private repos
------------------------

If you want to work with repos that are not hosted in github or bitbucket you can indicate explicitly the
type of repo that you want to use prepending `hg+` or `git+` to repo url::

    $ cookiecutter hg+https://example.com/repo


Keeping your cookiecutters organized
------------------------------------

As of the Cookiecutter 0.7.0 release:

* Whenever you generate a project with a cookiecutter, the resulting project
  is output to your current directory.

* Your cloned cookiecutters are stored by default in your `~/.cookiecutters/`
  directory (or Windows equivalent). The location is configurable: see
  :doc:`advanced_usage` for details.

Pre-0.7.0, this is how it worked:

* Whenever you generate a project with a cookiecutter, the resulting project
  is output to your current directory.

* Cloned cookiecutters were not saved locally.

