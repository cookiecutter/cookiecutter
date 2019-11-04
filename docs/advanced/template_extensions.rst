.. _`template extensions`:

Template Extensions
-------------------

*New in Cookiecutter 1.4*

A template may extend the Cookiecutter environment with custom `Jinja2 extensions`_,
that can add extra filters, tests, globals or even extend the parser.

To do so, a template author must specify the required extensions in ``cookiecutter.json`` as follows:

.. code-block:: json

    {
        "project_slug": "Foobar",
        "year": "{% now 'utc', '%Y' %}",
        "_extensions": ["jinja2_time.TimeExtension"]
    }

On invocation Cookiecutter tries to import the extensions and add them to its environment respectively.

In the above example, Cookiecutter provides the additional tag `now`_, after
installing the `jinja2_time.TimeExtension`_ and enabling it in ``cookiecutter.json``.

Please note that Cookiecutter will **not** install any dependencies on its own!
As a user you need to make sure you have all the extensions installed, before
running Cookiecutter on a template that requires custom Jinja2 extensions.

.. _`Jinja2 extensions`: http://jinja.pocoo.org/docs/latest/extensions/
.. _`now`: https://github.com/hackebrot/jinja2-time#now-tag
.. _`jinja2_time.TimeExtension`: https://github.com/hackebrot/jinja2-time
