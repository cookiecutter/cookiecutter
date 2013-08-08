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

Try it out!

Works directly with git repos too
---------------------------------

To create a project from the cookiecutter-pypackage.git repo template::

    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

You will be prompted to enter a bunch of project config values. (These are
defined in the project's `cookiecutter.json`.

Then, Cookiecutter will generate a project from the template, using the values
that you entered. It will be placed in your current directory.

Or hook directly into the Cookiecutter API
------------------------------------------

You can use Cookiecutter from Python::

    from cookiecutter.main import cookiecutter
    
    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
    
See the :ref:`API Reference` for more details.

If you use it in an interesting way, I'd love to hear about it: file an issue,
please!
