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

Or, if you are using conda, first add conda-forge to your channels:

.. code-block:: bash

    $ conda config --add channels conda-forge

Once the conda-forge channel has been enabled, cookiecutter can be installed with:

.. code-block:: bash

    $ conda install cookiecutter

Alternate installations
-----------------------

**Homebrew (Mac OS X only):**

.. code-block:: bash

    $ brew install cookiecutter

**Pipsi (Linux/OSX only):**

.. code-block:: bash

    $ pipsi install cookiecutter

**Debian (Most recentpackaged cookiecutter version):**

To access the most recent version, choose the 'unstable' branch at https://packages.debian.org/search?searchon=names&keywords=cookiecutter.  Before cookiecutter may be  installed, all dependencies must be installed.  These dependencies may be safely discovered by performing 'dpkg -i' on cookiecutter and then installing the printed dependency notifications.  What follows is a log of the commands entered during a typical cookiecutter installation of the latest debian package version (Note:  your packages may vary).

.. code-block:: bash

    $ sudo dpkg -i cookiecutter_1.4.0-1_all.deb
    $ sudo dpkg -i python-cookiecutter_1.4.0-1_all.deb
    $ sudo dpkg -i python-binaryornot_0.4.0-1_all.deb
    $ sudo dpkg -i python-click_6.6-1_all.deb
    $ sudo dpkg -i python-future_0.15.2-2_all.deb
    $ sudo dpkg -i python-configparser_3.3.0r2-2_all.deb
    $ sudo dpkg -i python-jinja2-time_0.1.0-1_all.deb
    $ sudo dpkg -i python-arrow_0.7.0-1_all.deb
    $ sudo dpkg -i python-whichcraft_0.1.1-1_all.deb
    $ sudo dpkg -i python-ruamel.yaml_0.11.11-1_amd64.deb # architecture specific
    $ sudo dpkg -i python-ruamel.ordereddict_0.4.9-1_amd64.deb # architecture specific
    $ sudo dpkg --configure -a # configures all packages installed above
    $ cookiecutter --version # Test installation of cookiecutter

.. note:: The debian cookiecutter package is patched version of cookiecutter using a different YAML parser from other installations.

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
