===============
Troubleshooting
===============

I created a cookiecutter, but it doesn't work, and I can't figure out why
-------------------------------------------------------------------------

* Try upgrading to Cookiecutter 0.8.0, which prints better error
  messages and has fixes for several common bugs.

I'm having trouble generating Jinja templates from Jinja templates
------------------------------------------------------------------

Make sure you escape things properly, like this::

    {{ "{{" }}

Or this::

    {% raw %}
    <p>Go <a href="{{ url_for('home') }}">Home</a></p>
    {% endraw %}

Or this::

    {{ {{ url_for('home') }} }}

See https://jinja.palletsprojects.com/en/latest/templates/#escaping for more info.

You can also use the `_copy_without_render`_ key in your `cookiecutter.json`
file to escape entire files and directories.

.. _`_copy_without_render`: http://cookiecutter.readthedocs.io/en/latest/advanced/copy_without_render.html


Other common issues
-------------------

I see ``CalledProcessError`` or ``'git' returned non-zero exit status`` on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you run Cookiecutter from Windows Command Prompt (``cmd.exe``) and see an error like::

    subprocess.CalledProcessError: Command '['git', 'clone', '...']' returned non-zero exit status 128

This means ``cmd.exe`` cannot find the ``git`` command. Use **Git Bash**
(included with `Git for Windows <https://git-scm.com/downloads>`_) to run
Cookiecutter commands instead.

Alternatively, add Git to your system ``PATH`` environment variable and restart
your command prompt.

This document is incomplete. If you have knowledge that could help other users,
adding a section or filing an issue with details would be greatly appreciated.
