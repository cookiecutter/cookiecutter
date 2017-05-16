.. _symlinks:

Symlinks
----------------------

Symlinks are virtual files or folders that simply point to another location on the
file system. For example, you may add a symlink to your project template ``system_logs``
that points to ``/var/log`` on the system where the template is rendered. Symlinks can
be thought of as a shortcut to a specific file or folder.

Symlinks will work on most platforms with cookiecutter. However, if you expect your
template to be used on Windows systems with Python < 3.2, it is recommended that you
do not use symlinks or that you handle symlinking in a post-generation hook.


Using symlinks
~~~~~~~~~~~~~~~~~~~~~~~

`Symbolic links`_ are commonly used in posix systems. Cookiecutter supports symlinks
in templates both as rendered and unrendered content. That is, the symlink itself
both be named with a variable or point to a destination with a variable in it.

On posix systems (see below for Windows systems) you can simply create a symbolic link
as normal in the template directory::

    ln -s existing_file_path new_symlink_path

As stated above, either ``existing_file_path`` or ``new_symlink_path`` can contain
variables that will be templated in braces ``{{ cookiecutter.variable }}``. These
will be replaced when the template is rendered.


Symlinks on Windows
~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: Symlinks are not currently supported on Windows systems with a
             Python version < 3.2. Symlinks should work as expected on other
             configurations.

Symlinks in the posix sense are a relatively new addition to Windows operating
systems, and support for these was introduced into Python in Python 3.2. If you
want to use symlinks in a template on a Windows system, you may need to take some
additional steps. On windows the ``mklink`` command will create links::

    > mklink new_symlink_path existing_file_path

First, if your template is cloned using ``git``, you will need to tell ``git`` to respect
symlinks when cloning the project. This can be done at the commandline::

    $ git config --global core.symlinks true

Second, it may be the case that a user, if not an administrator,  needs to be granted
special permissions in order to create symlinks. More details on permissions for
symlinks and how those can be managed are available `from Microsoft`_.


.. _`Symbolic links`: https://en.wikipedia.org/wiki/Symbolic_link
.. _`from Microsoft`: https://blogs.windows.com/buildingapps/2016/12/02/symlinks-windows-10/#TXpueSdQMpMz2YWf.97