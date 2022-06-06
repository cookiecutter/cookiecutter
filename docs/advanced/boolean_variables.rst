.. _boolean-variables:

Boolean Variables (2.2+)
------------------------

Boolean variables are used for answering True/False questions.

Basic Usage
~~~~~~~~~~~

Boolean variables are regular key / value pairs, but with the value being True/False.

For example, if you provide the following boolean variable in your ``cookiecutter.json``::

   {
       "run_as_docker": true
   }

you'd get the following user input when running Cookiecutter::

  run_as_docker [True]:

The following values are considered valid input:

   true, 1, yes, y **or**
   false, 0, no, n

The above ``run_as_docker`` boolean variable creates ``cookiecutter.run_as_docker``, which
can be used like this::

  {%- if cookiecutter.run_as_docker -%}
  # In case of True add your content here

  {%- else -%}
  # In case of False add your content here

  {% endif %}

Cookiecutter is using `Jinja2's if conditional expression <http://jinja.pocoo.org/docs/dev/templates/#if>`_ to determine the correct ``run_as_docker``.

Input Validation
~~~~~~~~~~~~~~~~
If a non valid value is inserted to a boolean field, the following error will be printed:

.. code-block:: bash

   run_as_docker [True]: docker
   Error: docker is not a valid boolean

