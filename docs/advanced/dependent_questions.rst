Dependent Questions
-------------------

.. versionadded:: 2.2.0

Dependent questions are questions that should be presented only if another question is answered with a trueful answer.

For example, consider the following ``cookiecutter.json``::

   {
       "is_storage": true,
       "access_mode?{{is_storage}}": ["ReadWriteOnce", "ReadOnlyMany", "ReadWriteMany"],
       "app": "app"
   }

The second question ``access_mode`` will be asked just if the value of ``is_storage`` is ``True``, otherwise the default value (``"ReadWriteOnce"``) will be stored in ``access_mode``.

Question prompt
~~~~~~~~~~~~~~~
- Setting ``is_storage`` to ``True``::

    is_storage [True]: true
    Select access_mode:
    1 - ReadWriteOnce
    2 - ReadOnlyMany
    3 - ReadWriteMany
    Choose from 1, 2, 3 [1]: 2
    app [app]: application

- Setting ``is_storage`` to ``False``::

    is_storage [True]: false
    app [app]: application


Support any boolean expression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Any boolean expression is supported after a ``?`` character.

For example::

    {
      "queue": ["kafka", "rabbit"],
      "topic?{{queue=='kafka'}}": "topic",
      "app": "app"
    }

The expression will be evaluated as a `Jinja2's boolean expression <https://jinja.palletsprojects.com/en/latest/templates/#comparisons>`_.


Template use
~~~~~~~~~~~~
These example values can be used in a template, such as the following::

    {%- if cookiecutter.is_storage -%}
    access_mode = {{cookiecutter.access_mode}}
    {% endif %}

