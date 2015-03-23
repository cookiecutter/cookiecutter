===============
Troubleshooting
===============

I created a cookiecutter, but it doesn't work, and I can't figure out why
-------------------------------------------------------------------------

* Try upgrading to Cookiecutter 0.8.0, which prints better error
  messages and has fixes for several common bugs.

I'm having trouble generating Jinja templates from Jinja templates
------------------------------------------------------------------

Make sure you escape things properly, like this::

    {{ "{{" }}

Or this::

    {% raw %}
    <p>Go <a href="{{ url_for('home') }}">Home</a></p>
    {% endraw %}

Or this::

    {{ {{ url_for('home') }} }}

See http://jinja.pocoo.org/docs/templates/#escaping for more info.

You can also use the `_copy_without_render` key in your `cookiecutter.json`
file, which accepts Unix shell-style wildcards::

    {
        "repo_name": "sample",
        "_copy_without_render": [
            "*.html",
            "*not_rendered_dir",
            "rendered_dir/not_rendered_file.ini"
        ]
    }

Other common issues
-------------------

TODO: add a bunch of common new user issues here.

This document is incomplete. If you have knowledge that could help other users,
adding a section or filing an issue with details would be greatly appreciated.
