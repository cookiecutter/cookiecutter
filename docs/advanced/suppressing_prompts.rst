.. _supressing-command-line-prompts:

Suppressing Command-Line Prompts
--------------------------------

To suppress the prompts asking for input, use `no_input`.

Basic Example: Using the Defaults
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: document `no_input`:

* As command-line argument
* As parameter of `cookiecutter()`

TODO: document where context values come from in this example (`cookiecutter.json` and `.cookiecutterrc`)

Advanced Example: Defaults + Extra Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you combine an `extra_context` dict with the `no_input` argument, you can programmatically create the project with a set list of context parameters and without any command line prompts::

    cookiecutter('cookiecutter-pypackage/',
                 no_input=True,
                 extra_context={'project_name': 'TheGreatest'})

See the :ref:`API Reference <apiref>` for more details.
