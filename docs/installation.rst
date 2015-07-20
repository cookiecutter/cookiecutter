============
Installation
============

At the command line:

.. code-block:: bash

    $ [sudo] pip install cookiecutter

Or, if you do not have pip:

.. code-block:: bash

    $ [sudo] easy_install cookiecutter

Though, pip is recommended.

Or, if you are using conda:

.. code-block:: bash

    $ conda install -c https://conda.binstar.org/pydanny cookiecutter

Alternate installations
-----------------------

Homebrew (Mac OS X only):

.. code-block:: bash

    $ brew install cookiecutter

Pipsi (Linux/OSX only):

.. code-block:: bash

    $ pipsi install cookiecutter

Upgrading from 0.6.4 to 0.7.0 or greater
-----------------------------------------

First, read :doc:`history` in detail. There are a lot of major
changes. The big ones are:

* Cookiecutter no longer deletes the cloned repo after generating a project.
* Cloned repos are saved into `~/.cookiecutters/`.
* You can optionally create a `~/.cookiecutterrc` config file.

Upgrade Cookiecutter either with easy_install:

.. code-block:: bash

    $ [sudo] easy_install --upgrade cookiecutter

Or with pip:

.. code-block:: bash

    $ [sudo] pip install -U cookiecutter

Then you should be good to go.
