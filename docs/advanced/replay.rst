.. _replay-feature:

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
            "email": "raphael@example.com",
            "full_name": "Raphael Pierzina",
            "github_username": "hackebrot",
            "kivy_version": "1.8.0",
            "project_slug": "foobar",
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

Custom replay file
~~~~~~~~~~~~~~~~~~

*New in Cookiecutter 2.0*

To specify a custom filename, you can use the ``--replay-file`` option::

    cookiecutter --replay-file ./cookiedozer.json gh:hackebrot/cookiedozer

This may be useful to run the same replay file over several machines, in tests
or when a user of the template reports a problem
