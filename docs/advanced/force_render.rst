.. _force-render:

Force Render
------------

*New in Cookiecutter 2.8*

Sometimes the ``binaryornot`` library incorrectly classifies text files as binary.
For example, a ``Makefile`` starting with ``PACKAGE_NAME := ...`` will be detected as a
binary file because the first four bytes (``PACK``) match a known binary signature
(Git pack-files).

To override this detection, the ``_force_render`` key can be used in ``cookiecutter.json``.
The value of this key accepts a list of Unix shell-style wildcards:

.. code-block:: JSON

    {
        "project_slug": "sample",
        "_force_render": [
            "Makefile",
            "*.mk",
            "config/settings.cfg"
        ]
    }

Files matching these patterns will always be rendered as text, even if they are detected
as binary by the heuristic.

**Note**:
The ``_force_render`` key works together with ``_copy_without_render``:

1. If a path matches ``_copy_without_render`` -- the file is copied without rendering.
2. If a path matches ``_force_render`` -- the file is always rendered as text, overriding binary detection.
3. Otherwise -- binary detection determines whether to render or copy.

``_copy_without_render`` takes precedence over ``_force_render``, since it is evaluated first.
