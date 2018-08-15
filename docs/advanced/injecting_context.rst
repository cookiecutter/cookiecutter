.. _injecting-extra-content:

Injecting Extra Context
-----------------------

You can specify an `extra_context` dictionary that will override values from `cookiecutter.json` or `.cookiecutterrc`::

    cookiecutter('cookiecutter-pypackage/',
                 extra_context={'project_name': 'TheGreatest'})

You will also need to add these keys to the `cookiecutter.json` or `.cookiecutterrc`.

Example: Injecting a Timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have ``cookiecutter.json`` that has the following keys::

    {
        "timestamp": "{{ cookiecutter.timestamp }}"
    }


This Python script will dynamically inject a timestamp value as the project is
generated::

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
