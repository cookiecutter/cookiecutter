Contributor Guidelines
-----------------------

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.3, 3.4, 3.5, and PyPy on Appveyor and Travis CI.
4. Check https://travis-ci.org/audreyr/cookiecutter/pull_requests and 
   https://ci.appveyor.com/project/audreyr/cookiecutter/history to ensure the tests pass for all supported Python versions and platforms.

Coding Standards
~~~~~~~~~~~~~~~~

* PEP8
* Functions over classes except in tests
* Quotes via http://stackoverflow.com/a/56190/5549

  * Use double quotes around strings that are used for interpolation or that are natural language messages
  * Use single quotes for small symbol-like strings (but break the rules if the strings contain quotes)
  * Use triple double quotes for docstrings and raw string literals for regular expressions even if they aren't needed.
  * Example:

    .. code-block:: python

        LIGHT_MESSAGES = {
            'English': "There are %(number_of_lights)s lights.",
            'Pirate':  "Arr! Thar be %(number_of_lights)s lights."
        }

        def lights_message(language, number_of_lights):
            """Return a language-appropriate string reporting the light count."""
            return LIGHT_MESSAGES[language] % locals()

        def is_pirate(message):
            """Return True if the given message sounds piratical."""
            return re.search(r"(?i)(arr|avast|yohoho)!", message) is not None

  * Write new code in Python 3.
