.. _single-file-templates:

Single File Templates
---------------------

*New in dev master*

Sometimes you want to create individual files within a repository, rather than
creating a complete project. This can be achieved with the `_target` key,
which specifies which directory template files should be placed in.

For example, the following places all files in the template into the
current directory::

    {
        "project_slug": "sample",
        "_target": ".",
    }

A top-level directory of the form `{{cookiecutter.<X>}}` must be created to keep the
templates and files as for standard-templates, but its name is ignored.
