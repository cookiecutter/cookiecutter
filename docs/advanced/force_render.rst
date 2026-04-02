.. _force-render:

Force Render
------------

*New in Cookiecutter 2.8*

Cookiecutter uses the `binaryornot`_ library to detect whether a file is
binary before attempting to render it as a Jinja2 template.  The detection is
heuristic-based and can occasionally misclassify plain-text files as binary.
A well-known example is a ``Makefile`` whose first token is ``PACKAGE_NAME``
– the four-byte prefix ``PACK`` matches the magic bytes of a `git packfile`_,
so ``binaryornot`` marks the file as binary and cookiecutter copies it
verbatim without expanding any template variables.

To work around this, add the ``_force_render`` key to ``cookiecutter.json``.
Its value is a list of Unix shell-style wildcard patterns (identical to the
syntax used by :ref:`copy-without-render`).  Any file whose path matches one
of the patterns will **always** be rendered as a Jinja2 template, regardless
of what ``binaryornot`` reports.

.. code-block:: JSON

    {
        "project_slug": "sample",
        "_force_render": [
            "Makefile",
            "*.mk"
        ]
    }

With this configuration a ``Makefile`` that starts with::

    PACKAGE_NAME := {{cookiecutter.project_slug}}

will be correctly rendered to::

    PACKAGE_NAME := sample

instead of being copied as-is.

**Note**: ``_force_render`` only affects the *content* of the matched files.
Their *paths* (file names and directory names) are always rendered.

.. _binaryornot: https://pypi.org/project/binaryornot/
.. _git packfile: https://git-scm.com/book/en/v2/Git-Internals-Packfiles
