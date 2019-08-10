---
title: 'Suppressing Command-Line Prompts'
---

To suppress the prompts asking for input, use [no\_input]{.title-ref}.

Basic Example: Using the Defaults
=================================

Cookiecutter will pick a default value if used with \`no\_input\`:

    from cookiecutter.main import cookiecutter
    cookiecutter(
        'cookiecutter-django',
        no_input=True,
    )

In this case it will be using the default defined in
[cookiecutter.json]{.title-ref} or [.cookiecutterrc]{.title-ref}.

::: {.note}
::: {.admonition-title}
Note
:::

values from [cookiecutter.json]{.title-ref} will be overridden by values
from [.cookiecutterrc]{.title-ref}
:::

Advanced Example: Defaults + Extra Context
==========================================

If you combine an [extra\_context]{.title-ref} dict with the
[no\_input]{.title-ref} argument, you can programmatically create the
project with a set list of context parameters and without any command
line prompts:

    cookiecutter('cookiecutter-pypackage/',
                 no_input=True,
                 extra_context={'project_name': 'TheGreatest'})

See the `API Reference <apiref>`{.interpreted-text role="ref"} for more
details.

