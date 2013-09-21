===============
Troubleshooting
===============

I created a cookiecutter, but it doesn't work, and I can't figure out why
-------------------------------------------------------------------------

* Try the latest development version of Cookiecutter, which prints better error
  messages and has fixes for several common bugs.
  
  .. note:: This is a temporary solution; the upcoming 0.7.0 release will be
     out shortly. Please be patient, as I'm rushing to get this ready during my
     limited free time. -- `@audreyr`_

.. _`@audreyr`: https://github.com/audreyr

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

Other common issues
-------------------

TODO: add a bunch of common new user issues here.

This document is incomplete. If you have knowledge that could help other users,
adding a section or filing an issue with details would be greatly appreciated.
