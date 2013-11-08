============
Installation
============

At the command line:

.. code-block:: bash

    $ easy_install cookiecutter

Or, if you have pip (the Python package installer tool):

.. code-block:: bash

    $ [sudo] pip install cookiecutter

Upgrading from 0.6.4 to 0.7.0
-----------------------------

First, read :doc:`history` in detail. There are a lot of major
changes. The big ones are:

* Cookiecutter no longer deletes the cloned repo after generating a project.
* Cloned repos are saved into `~/.cookiecutters/`. 
* You can optionally create a `~/.cookiecutterrc` config file.

Upgrade Cookiecutter with one of the following:

    $ easy_install --upgrade cookiecutter
    $ [sudo] pip install -U cookiecutter

Then you should be good to go.
