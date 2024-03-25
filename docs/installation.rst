============
Installation
============

Prerequisites
-------------

* Python interpreter
* Adjust your path
* Packaging tools

Python interpreter
^^^^^^^^^^^^^^^^^^

Install Python for your operating system.
On Windows and macOS this is usually necessary.
Most Linux distributions come with Python pre-installed.
Consult the official `Python documentation <https://docs.python.org/3/using/index.html>`_ for details.

You can install the Python binaries from `python.org <https://www.python.org/downloads/>`_.
Alternatively on macOS, you can use the `homebrew <http://brew.sh/>`_ package manager.

.. code-block:: bash

    brew install python3


Adjust your path
^^^^^^^^^^^^^^^^

Ensure that your ``bin`` folder is on your path for your platform. Typically ``~/.local/`` for UNIX and macOS, or ``%APPDATA%\Python`` on Windows. (See the Python documentation for `site.USER_BASE <https://docs.python.org/3/library/site.html#site.USER_BASE>`_ for full details.)


UNIX and macOS
""""""""""""""

For bash shells, add the following to your ``.bash_profile`` (adjust for other shells):

.. code-block:: bash

    # Add ~/.local/ to PATH
    export PATH=$HOME/.local/bin:$PATH

Remember to load changes with ``source ~/.bash_profile`` or open a new shell session.


Windows
"""""""

Ensure the directory where cookiecutter will be installed is in your environment's ``Path`` in order to make it possible to invoke it from a command prompt. To do so, search for "Environment Variables" on your computer (on Windows 10, it is under ``System Properties`` --> ``Advanced``) and add that directory to the ``Path`` environment variable, using the GUI to edit path segments.

Example segments should look like ``%APPDATA%\Python\Python3x\Scripts``, where you have your version of Python instead of ``Python3x``.

You may need to restart your command prompt session to load the environment variables.

.. seealso:: See `Configuring Python (on Windows) <https://docs.python.org/3/using/windows.html#configuring-python>`_ for full details.

**Unix on Windows**


You may also install  `Windows Subsystem for Linux <https://msdn.microsoft.com/en-us/commandline/wsl/install-win10>`_ or `GNU utilities for Win32 <http://unxutils.sourceforge.net>`_ to use Unix commands on Windows.

Packaging tools
^^^^^^^^^^^^^^^

See the Python Packaging Authority's (PyPA) documentation `Requirements for Installing Packages <https://packaging.python.org/en/latest/installing/#requirements-for-installing-packages>`_ for full details.


Install cookiecutter
--------------------

At the command line:

.. code-block:: bash

    python3 -m pip install --user cookiecutter

Or, if you do not have pip:

.. code-block:: bash

    easy_install --user cookiecutter

Though, pip is recommended, easy_install is deprecated.

Or, if you are using conda, first add conda-forge to your channels:

.. code-block:: bash

    conda config --add channels conda-forge

Once the conda-forge channel has been enabled, cookiecutter can be installed with:

.. code-block:: bash

    conda install cookiecutter

Alternate installations
-----------------------

**Homebrew (Mac OS X only):**

.. code-block:: bash

    brew install cookiecutter

**Void Linux:**

.. code-block:: bash

    xbps-install cookiecutter

**Pipx (Linux, OSX and Windows):**

.. code-block:: bash

    pipx install cookiecutter


Upgrading
---------

from 0.6.4 to 0.7.0 or greater
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, read :doc:`HISTORY` in detail.
There are a lot of major changes.
The big ones are:

* Cookiecutter no longer deletes the cloned repo after generating a project.
* Cloned repos are saved into `~/.cookiecutters/`.
* You can optionally create a `~/.cookiecutterrc` config file.


Or with pip:

.. code-block:: bash

    python3 -m pip install --upgrade cookiecutter

Upgrade Cookiecutter either with easy_install (deprecated):

.. code-block:: bash

    easy_install --upgrade cookiecutter

Then you should be good to go.
