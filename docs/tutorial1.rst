========================================
Tutorial 1: Getting to Know Cookiecutter
========================================

.. note:: Before you begin, please install Cookiecutter 0.7.0 or higher.
   Instructions are in :doc:`installation`.

Cookiecutter is a tool for creating projects from *cookiecutters* (project
templates).

What exactly does this mean? Read on!

Case Study: cookiecutter-pypackage
-----------------------------------

*cookiecutter-pypackage* is a cookiecutter template that creates the starter
boilerplate for a Python package.

.. note:: There are several variations of it, but for this tutorial we'll use
   the original version at https://github.com/audreyr/cookiecutter-pypackage/.

Step 1: Generate a Python Package Project
------------------------------------------

Open your shell and cd into the directory where you'd like to create a starter
Python package project.

At the command line, run the cookiecutter command, passing in the link to
cookiecutter-pypackage's HTTPS clone URL like this:

.. code-block:: bash

    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

Local Cloning of Project Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, cookiecutter-pypackage gets cloned to `~/.cookiecutters/` (or equivalent
on Windows). Cookiecutter does this for you, so sit back and wait.

Local Generation of Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When cloning is complete, you will be prompted to enter a bunch of values, such
as `full_name`, `email`, and `project_name`. Either enter your info, or simply
press return/enter to accept the default values.

This info will be used to fill in the blanks for your project. For example,
your name and the year will be placed into the LICENSE file.

Step 2: Explore What Got Generated
----------------------------------

In your current directory, you should see that a project got generated:

.. code-block:: bash

    $ ls
    boilerplate

Looking inside the `boilerplate/` (or directory corresponding to your `repo_name`)
directory, you should see something like this:

.. code-block:: bash

    $ ls boilerplate/
    AUTHORS.rst      MANIFEST.in      docs             tox.ini
    CONTRIBUTING.rst Makefile         requirements.txt
    HISTORY.rst      README.rst       setup.py
    LICENSE          boilerplate      tests

That's your new project!

If you open the AUTHORS.rst file, you should see something like this:

.. code-block:: rst

    =======
    Credits
    =======

    Development Lead
    ----------------

    * Audrey Roy <audreyr@gmail.com>

    Contributors
    ------------

    None yet. Why not be the first?

Notice how it was auto-populated with your (or my) name and email.

Also take note of the fact that you are looking at a ReStructuredText file.
Cookiecutter can generate a project with text files of any type.

Great, you just generated a skeleton Python package. How did that work?

Step 3: Observe How It Was Generated
------------------------------------

Let's take a look at cookiecutter-pypackage together. Open https://github.com/audreyr/cookiecutter-pypackage in a new browser window.

{{ cookiecutter.repo_name }}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Find the directory called `{{ cookiecutter.repo_name }}`. Click on it. Observe
the files inside of it. You should see that this directory and its contents
corresponds to the project that you just generated.

AUTHORS.rst
~~~~~~~~~~~

Look at the raw version of `{{ cookiecutter.repo_name }}/AUTHORS.rst`, at
https://raw.github.com/audreyr/cookiecutter-pypackage/master/%7B%7Bcookiecutter.repo_name%7D%7D/AUTHORS.rst.

Observe how it corresponds to the `AUTHORS.rst` file that you generated.

cookiecutter.json
~~~~~~~~~~~~~~~~~

Now navigate back up to `cookiecutter-pypackage/` and look at the
`cookiecutter.json` file.

You should see JSON that corresponds to the prompts and default values shown
earlier during project generation:

.. code-block:: json

    {
        "full_name": "Audrey Roy",
        "email": "audreyr@gmail.com",
        "github_username": "audreyr",
        "project_name": "Python Boilerplate",
        "repo_name": "boilerplate",
        "project_short_description": "Python Boilerplate contains all the boilerplate you need to create a Python package.",
        "release_date": "2013-08-11",
        "year": "2013",
        "version": "0.1.0"
    }

Questions?
----------

If anything needs better explanation, please take a moment to file an issue at https://github.com/audreyr/cookiecutter/issues with what could be improved
about this tutorial.

Summary
-------

You have learned how to use Cookiecutter to generate your first project from a
cookiecutter project template.

In Tutorial 2, you'll see how to create cookiecutters of your own, from scratch.
