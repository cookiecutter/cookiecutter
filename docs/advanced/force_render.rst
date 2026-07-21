.. _force-render:

Force Render
------------

*New in Cookiecutter (unreleased)*

Binary detection is heuristic and can produce false positives (for example, a
plain-text file that starts with ``PACKAGE_NAME`` is treated as binary because
``binaryornot`` matches the ``PACK`` signature).

To force Jinja rendering for matching paths even when binary detection would
skip them, use the ``_force_render`` key in ``cookiecutter.json``. The value is a
list of Unix shell-style wildcards, the same style as ``_copy_without_render``:

.. code-block:: JSON

    {
        "project_slug": "sample",
        "_force_render": [
            "Makefile",
            "*.mk",
            "configs/*.ini"
        ]
    }

**Precedence**

1. Paths matching ``_copy_without_render`` are copied without rendering.
2. Paths matching ``_force_render`` are always rendered as text.
3. Otherwise binary detection decides whether to copy or render.

**Note**:
``_force_render`` only affects file *contents*. Path rendering still uses the
normal Jinja path expansion for the output name.
