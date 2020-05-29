.. _new-lines:

Working with line-ends special symbols LF/CRLF
----------------------------------------------

*New in Cookiecutter 2.0*

Before version 2.0 Cookiecutter silently used system line end character.
LF for POSIX and CRLF for Windows. Since version 2.0 this behaviour changed
and now can be forced at template level.

By default Cookiecutter now check every file at render stage and use same line
end as in source. This allow template developers to have both types of files in
the same template. Developers should correctly configure their `.gitattributes`
file to avoid line-end character overwrite by git.

Special template variable `_new_lines` was added in Cookiecutter 2.0.
Acceptable variables: `'\n\r'` for CRLF and `'\n'` for POSIX.

Here is example how to force line endings to CRLF on any deployment::

    {
        "project_slug": "sample",
        "_new_lines": "\n\r"
    }
