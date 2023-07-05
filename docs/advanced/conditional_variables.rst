.. _conditional_variables:

Using conditional variables
---------------------------

You can specify conditional variables that will only be rendered if a certain other variable is set to 'yes' and the name starts with ``_if_use_``::

    {
        "_if_use_<variable-name>": {
            "extra_variables" : "extra
        }
    }

Example: Add a conditional variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have ``cookiecutter.json`` that has the following keys::

    {
        "project_name": "project_name",
        "docker": "yes",
        "_if_use_docker": {
            "activate_docker": "now",
            "platform": "Linux
        }
    }


If the value of docker is 'yes' the two other variables will be added to the output. 
If the value of docker is 'no', the complete dictionary of ``_if_use_docker`` will be removed.
