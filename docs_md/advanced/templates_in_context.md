---
title: Templates in Context Values
---

The values (but not the keys!) of [cookiecutter.json]{.title-ref} are
also Jinja2 templates. Values from user prompts are added to the context
immediately, such that one context value can be derived from previous
values. This approach can potentially save your user a lot of keystrokes
by providing more sensible defaults.

Basic Example: Templates in Context
===================================

Python packages show some patterns for their naming conventions:

-   a human-readable project name
-   a lowercase, dashed repository name
-   an importable, dash-less package name

Here is a [cookiecutter.json]{.title-ref} with templated values for this
pattern:

    {
      "project_name": "My New Project",
      "project_slug": "{{ cookiecutter.project_name|lower|replace(' ', '-') }}",
      "pkg_name": "{{ cookiecutter.project_slug|replace('-', '') }}"
    }

If the user takes the defaults, or uses [no\_input]{.title-ref}, the
templated values will be:

-   [my-new-project]{.title-ref}
-   [mynewproject]{.title-ref}

Or, if the user gives [Yet Another New Project]{.title-ref}, the values
will be:

-   [yet-another-new-project]{.title-ref}
-   [yetanothernewproject]{.title-ref}

