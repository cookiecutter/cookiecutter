.. _loading-custom-filters:

Load custom filters for jinja2
------------------------------------------

You can add custom filters to the template

Step 1: define filters in `cookiecutter.json`, like this
------------------------------

    {
        "_filters": {
            "camelcase": "string_camelcase",
            "sanitize": "sanitize"
        }
    }

Step 2: Writing you filters
------------------------------

This is the directory structure for a simple cookiecutter::

    cookiecutter-something/
    ├── {{ cookiecutter.project_name }}/  <--------- Project template
    │   └── ...
    ├── filters/
    ├── └── filters.py                    <--------- Write the custom filters here
    │   └── __init__.py
    │
    │
    └── cookiecutter.json             <--------- Prompts & default values


Then, `filters.py` like this::
    import string
    import re
    import random


    def passphrase(length=32, punctuation=False, digits=True):
        characters = string.ascii_letters
        if digits:
            characters += string.digits

        if punctuation:
            punctuations = string.punctuation.replace('"', "").replace('\\', "")
            characters += punctuations

        password = ''.join(random.sample(characters, length))
        return password


    CAMELCASE_INVALID_CHARS = re.compile(r'[^a-zA-Z\d]')


    def string_camelcase(value):
        return CAMELCASE_INVALID_CHARS.sub('', value.title())


    def sanitize(module_name):
        """Sanitize the given module name, by replacing dashes and points
        with underscores and prefixing it with a letter if it doesn't start
        with one
        """
        return CAMELCASE_INVALID_CHARS.sub('', module_name)
