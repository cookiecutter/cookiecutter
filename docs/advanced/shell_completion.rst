.. _shell-completion:

Configuring Shell Completion
----------------------------

Cookiecutter uses the `click <https://github.com/pallets/click>`_ library
to provide the CLI interface.
The click library natively supports `shell completions <https://click.palletsprojects.com/en/stable/shell-completion/>`_
for the Bash, Fish, and Zsh shells.

Bash
====

For Bash, add the following to your `~.bashrc` file:

.. code-block:: bash

    eval "$(_COOKIECUTTER_COMPLETE=bash_source cookiecutter)"


Fish
====

For Fish, add the following to your `~/.config/fish/completions/cookiecutter.fish` file

.. code-block:: fishshell

    _COOKIECUTTER_COMPLETE=fish_source cookiecutter | source


Zsh
===

For Zsh, add the following to your `~/.zshrc` file:

.. code-block:: zsh

    eval "$(_COOKIECUTTER_COMPLETE=zsh_source cookiecutter)"
