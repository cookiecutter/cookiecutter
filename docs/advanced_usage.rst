==============
Advanced Usage
==============

Using Pre/Post-Generate Hooks (0.7.0+)
--------------------------------------

You can have Python or Shell scripts that run before and/or after your project
is generated.

Put them in `hooks/` like this::

    cookiecutter-something/
    ├── {{cookiecutter.repo_name}}/
    ├── hooks
    │   ├── pre_gen_project.py
    │   └── post_gen_project.py
    └── cookiecutter.json

Shell scripts work similarly::

    cookiecutter-something/
    ├── {{cookiecutter.repo_name}}/
    ├── hooks
    │   ├── pre_gen_project.sh
    │   └── post_gen_project.sh
    └── cookiecutter.json

It shouldn't be too hard to extend Cookiecutter to work with other types of
scripts too. Pull requests are welcome.

For portability, you should use Python scripts (with extension `.py`) for your
hooks, as these can be run on any platform. However, if you intend for your
template to only be run on a single platform, a shell script (or `.bat` file
on Windows) can be a quicker alternative.

.. note::
    Make sure your hook scripts work in a robust manner. If a hook script fails
    (that is, `if it finishes with a nonzero exit status
    <https://docs.python.org/3/library/sys.html#sys.exit>`_), the project
    generation will stop and the generated directory will be cleaned up.

Example: Validating template variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is an example of script that validates a template variable
before generating the project, to be used as ``hooks/pre_gen_project.py``:

.. code-block:: python

    import re
    import sys


    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

    module_name = '{{ cookiecutter.module_name }}'

    if not re.match(MODULE_REGEX, module_name):
        print('ERROR: %s is not a valid Python module name!' % module_name)

        # exits with status 1 to indicate failure
        sys.exit(1)

.. _user-config:
	
User Config (0.7.0+)
----------------------

If you use Cookiecutter a lot, you'll find it useful to have a user config
file. By default Cookiecutter tries to retrieve settings from a `.cookiecutterrc`
file in your home directory.

From version 1.3.0 you can also specify a config file on the command line via ``--config-file``::

    $ cookiecutter --config-file /home/audreyr/my-custom-config.yaml cookiecutter-pypackage

Or you can set the ``COOKIECUTTER_CONFIG`` environment variable::

    $ export COOKIECUTTER_CONFIG=/home/audreyr/my-custom-config.yaml

If you wish to stick to the built-in config and not load any user config file at all,
use the cli option ``--default-config`` instead. Preventing Cookiecutter from loading
user settings is crucial for writing integration tests in an isolated environment.

Example user config:

.. code-block:: yaml

    default_context:
        full_name: "Audrey Roy"
        email: "audreyr@gmail.com"
        github_username: "audreyr"
    cookiecutters_dir: "/home/audreyr/my-custom-cookiecutters-dir/"
    replay_dir: "/home/audreyr/my-custom-replay-dir/"
    abbreviations:
        pp: https://github.com/audreyr/cookiecutter-pypackage.git
        gh: https://github.com/{0}.git
        bb: https://bitbucket.org/{0}

Possible settings are:

* default_context: A list of key/value pairs that you want injected as context
  whenever you generate a project with Cookiecutter. These values are treated
  like the defaults in `cookiecutter.json`, upon generation of any project.
* cookiecutters_dir: Directory where your cookiecutters are cloned to when you
  use Cookiecutter with a repo argument.
* replay_dir: Directory where Cookiecutter dumps context data to, which
  you can fetch later on when using the `replay feature`_.
* abbreviations: A list of abbreviations for cookiecutters. Abbreviations can
  be simple aliases for a repo name, or can be used as a prefix, in the form
  `abbr:suffix`. Any suffix will be inserted into the expansion in place of
  the text `{0}`, using standard Python string formatting.  With the above
  aliases, you could use the `cookiecutter-pypackage` template simply by saying
  `cookiecutter pp`, or `cookiecutter gh:audreyr/cookiecutter-pypackage`.
  The `gh` (github) and `bb` (bitbucket) abbreviations shown above are actually
  built in, and can be used without defining them yourself.

Calling Cookiecutter Functions From Python
------------------------------------------

You can use Cookiecutter from Python::

    from cookiecutter.main import cookiecutter

    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')

This is useful if, for example, you're writing a web framework and need to
provide developers with a tool similar to `django-admin.py startproject` or
`npm init`.

Injecting Extra Context
-----------------------

You can specify an `extra_context` dictionary that will override values from `cookiecutter.json` or `.cookiecutterrc`::

    cookiecutter('cookiecutter-pypackage/',
                 extra_context={'project_name': 'TheGreatest'})

Example: Injecting a Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a sample Python script that dynamically injects a timestamp value
as a project is generated::

    from cookiecutter.main import cookiecutter

    from datetime import datetime

    cookiecutter(
        'cookiecutter-django',
        extra_context={'timestamp': datetime.utcnow().isoformat()}
    )

How this works:

1. The script uses `datetime` to get the current UTC time in ISO format.
2. To generate the project, `cookiecutter()` is called, passing the timestamp
   in as context via the `extra_context` dict.

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

Templates in Context Values
--------------------------------

The values (but not the keys!) of `cookiecutter.json` are also Jinja2 templates.
Values from user prompts are added to the context immediately, such that one
context value can be derived from previous values. This approach can potentially
save your user a lot of keystrokes by providing more sensible defaults.

Basic Example: Templates in Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python packages show some patterns for their naming conventions:

* a human-readable project name
* a lowercase, dashed repository name
* an importable, dash-less package name

Here is a `cookiecuttter.json` with templated values for this pattern::

    {
      "project_name": "My New Project",
      "repo_name": "{{ cookiecutter.project_name|lower|replace(' ', '-') }}",
      "pkg_name": "{{ cookiecutter.repo_name|replace('-', '') }}"
    }

If the user takes the defaults, or uses `no_input`, the templated values will 
be:

* `my-new-project`
* `mynewproject`

Or, if the user gives `Yet Another New Project`, the values will be:

* `yet-another-new-project`
* `yetanothernewproject`

Copy without Render
-------------------

*New in Cookiecutter 1.1*

To avoid rendering directories and files of a cookiecutter mould, the `_copy_without_render` key can be used in the `cookiecutter.json`. The value of this key accepts a list of Unix shell-style wildcards::

    {
        "repo_name": "sample",
        "_copy_without_render": [
            "*.html",
            "*not_rendered_dir",
            "rendered_dir/not_rendered_file.ini"
        ]
    }

.. _`replay feature`:

Replay Project Generation
-------------------------

*New in Cookiecutter 1.1*

On invocation **Cookiecutter** dumps a json file to ``~/.cookiecutter_replay/`` which enables you to *replay* later on.

In other words, it persists your **input** for a template and fetches it when you run the same template again.

Example for a replay file (which was created via ``cookiecutter gh:hackebrot/cookiedozer``)::

    {
        "cookiecutter": {
            "app_class_name": "FooBarApp",
            "app_title": "Foo Bar",
            "email": "raphael@hackebrot.de",
            "full_name": "Raphael Pierzina",
            "github_username": "hackebrot",
            "kivy_version": "1.8.0",
            "repo_name": "foobar",
            "short_description": "A sleek slideshow app that supports swipe gestures.",
            "version": "0.1.0",
            "year": "2015"
        }
    }

To fetch this context data without being prompted on the command line you can use either of the following methods.

Pass the according option on the CLI::

    cookiecutter --replay gh:hackebrot/cookiedozer


Or use the Python API::

    from cookiecutter.main import cookiecutter
    cookiecutter('gh:hackebrot/cookiedozer', replay=True)


This feature is comes in handy if, for instance, you want to create a new project from an updated template.

.. _command_line_options:

Command Line Options
--------------------

.. cc-command-line-options::

.. _choice-variables:
   
Choice Variables (1.1+)
-----------------------

Choice variables provide different choices when creating a project. Depending on an user's choice
the template renders things differently.

Basic Usage
~~~~~~~~~~~

Choice variables are regular key / value pairs, but with the value being a list of strings.

For example, if you provide the follwing choice variable in your ``cookiecutter.json``::

   {
       "license": ["MIT", "BSD-3", "GNU GPL v3.0", "Apache Software License 2.0"]
   }

you'd get the following choices when running Cookiecutter::

   Select license:
   1 - MIT
   2 - BSD-3
   3 - GNU GPL v3.0
   4 - Apache Software License 2.0
   Choose from 1, 2, 3, 4 [1]:		

Depending on an user's choice, a different license is rendered by Cookiecutter. 

The above ``license`` choice variable creates ``cookiecutter.license``, which
can be used like this::

  {%- if cookiecutter.license == "MIT" -%}
  # Possible license content here
  
  {%- elif cookiecutter.license == "BSD-3" -%}
  # More possible license content here

Cookiecutter is using `Jinja2's if conditional expression <http://jinja.pocoo.org/docs/dev/templates/#if>`_ to determine the correct license.

The created choice variable is still a regular Cookiecutter variable and can be used like this::

  License
  -------

  Distributed under the terms of the `{{cookiecutter.license}}`_ license,
  
Overwriting Default Choice Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choice Variables are overwritable using a :ref:`user-config` file.

For example, a choice variable can be created in ``cookiecutter.json`` by using a list as value::

   {
       "license": ["MIT", "BSD-3", "GNU GPL v3.0", "Apache Software License 2.0"]
   }

By default, the first entry in the values list serves as default value in the prompt.

Setting the default ``license`` agreement to *Apache Software License 2.0* can be done using:

.. code-block:: yaml

   default_context:       
       license: "Apache Software License 2.0"  

in the :ref:`user-config` file. 
       
The resulting prompt changes and looks like::

  Select license:
  1 - Apache Software License 2.0
  2 - MIT
  3 - BSD-3
  4 - GNU GPL v3.0
  Choose from 1, 2, 3, 4 [1]:

.. note::
   As you can see the order of the options changed from ``1 - MIT`` to ``1 - Apache Software License 2.0``. **Cookiecutter** takes the first value in the list as the default.

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

.. _`Jinja2 extensions`: http://jinja2.readthedocs.org/en/latest/extensions.html#extensions
.. _`now`: https://github.com/hackebrot/jinja2-time#now-tag
.. _`jinja2_time.TimeExtension`: https://github.com/hackebrot/jinja2-time
