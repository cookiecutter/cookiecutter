.. _new-lines:

Working with line-ends special symbols LF/CRLF
----------------------------------------------

*New in Cookiecutter 2.0*

.. note::

    Before version 2.0 Cookiecutter silently used system line end character.
    LF for POSIX and CRLF for Windows.
    Since version 2.0 this behaviour changed and now can be forced at template level.

By default Cookiecutter checks every file at render stage and uses the same line end as in source.
This allow template developers to have both types of files in the same template.
Developers should correctly configure their ``.gitattributes`` file to avoid line-end character overwrite by git.

The special template variable ``_new_lines`` enforces a specific line ending.
Acceptable variables: ``'\r\n'`` for CRLF and ``'\n'`` for POSIX.

Here is example how to force line endings to CRLF on any deployment:

.. code-block:: JSON

    {
        "project_slug": "sample",
        "_new_lines": "\r\n"
    }
