.. _force-render:

Force Render
------------

To force Cookiecutter to render text files that its binary-file detection would
otherwise copy unchanged, use the ``_force_render`` key in
``cookiecutter.json``.

The value accepts a list of Unix shell-style wildcards:

.. code-block:: JSON

    {
        "project_slug": "sample",
        "_force_render": [
            "Makefile",
            "*.mk",
            "scripts/*.sh"
        ]
    }

This is useful for text files whose first bytes match a binary signature. For
example, a ``Makefile`` that starts with ``PACKAGE_NAME := ...`` begins with
the bytes ``PACK``, which some binary-detection heuristics treat as binary
data.

Only file contents are affected by ``_force_render``. Paths are still rendered
normally before the generated file is written.
