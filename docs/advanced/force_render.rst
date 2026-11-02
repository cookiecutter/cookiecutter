.. _force-render:

Force Render
------------

Some text files can be misclassified as binary by Cookiecutter's binary
detection.  For example, a file whose first bytes are ``PACKAGE_NAME :=`` is
detected as a ``PACK`` binary signature, so its Jinja template would be copied
without rendering.

To force such files to be treated as text and rendered, use the
``_force_render`` key in ``cookiecutter.json``.  The value accepts a list of
Unix shell-style wildcards:

.. code-block:: JSON

    {
        "project_slug": "sample",
        "_force_render": [
            "Makefile",
            "*.mk"
        ]
    }

``_copy_without_render`` takes precedence over ``_force_render``.  If a file
matches both settings, it is copied without rendering.

The paths are subject to rendering, as with ``_copy_without_render``.
