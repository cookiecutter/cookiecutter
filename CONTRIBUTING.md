# CONTRIBUTING TO COOKIECUTTER

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. 


- [Types of Contributions](#Types-of-Contributions)
- [Contributor Setup](#Setting-Up-the-Code-for-Local-Development)
- [Contributor Guidelines](#Contributor-Guidelines)
- [Contributor Testing](#Testing-with-tox)
- [Core Committer Guide](#)


## Types of Contributions

You can contribute in many ways:

### Create Cookiecutter Templates

Some other Cookiecutter templates to list in the [README](README.md) would
be great.

If you create a Cookiecutter template, submit a pull request adding it to
README.rst.

### Report Bugs

Report bugs at https://github.com/audreyr/cookiecutter/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- If you can, provide detailed steps to reproduce the bug.
- If you don't have steps to reproduce the bug, just note your observations in
  as much detail as you can. Questions to start a discussion about the issue
  are welcome.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "please-help" is open to whoever wants to implement it.

Please do not combine multiple feature enhancements into a single pull request.

Note: this project is very conservative, so new features that aren't tagged
with "please-help" might not get into core. We're trying to keep the code base
small, extensible, and streamlined. Whenever possible, it's best to try and
implement feature ideas as separate projects outside of the core codebase.

### Write Documentation

Cookiecutter could always use more documentation, whether as part of the
official Cookiecutter docs, in docstrings, or even on the web in blog posts,
articles, and such.

If you want to review your changes on the documentation locally, you can do::

    pip install -r docs/requirements.txt
    make servedocs

This will compile the documentation, open it in your browser and start
watching the files for changes, recompiling as you save.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/audreyr/cookiecutter/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Setting Up the Code for Local Development

Here's how to set up `cookiecutter` for local development.

1. Fork the `cookiecutter` repo on GitHub.
2. Clone your fork locally:

```
    $ git clone git@github.com:your_name_here/cookiecutter.git
```

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:
 ```
    $ mkvirtualenv cookiecutter
    $ cd cookiecutter/
    $ python setup.py develop
 ```

4. Create a branch for local development:

```
    $ git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and flake8:

```
    $ pip install tox
    $ tox
```

Please note that tox runs flake8 automatically, since we have a test environment for it.

If you feel like running only the flake8 environment, please use the following command:
```
    $ tox -e flake8
```

6. Commit your changes and push your branch to GitHub:
```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
```

7. Check that the test coverage hasn't dropped::
```
    $ tox -e cov-report
```

8. Submit a pull request through the GitHub website.


## Contributor Guidelines

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
3. The pull request should work for Python 2.7, 3.4, 3.5, 3.6, and PyPy on AppVeyor and Travis CI.
4. Check https://travis-ci.org/audreyr/cookiecutter/pull_requests and https://ci.appveyor.com/project/audreyr/cookiecutter/history to ensure the tests pass for all supported Python versions and platforms.

### Coding Standards

* PEP8
* Functions over classes except in tests
* Quotes via http://stackoverflow.com/a/56190/5549

  * Use double quotes around strings that are used for interpolation or that are natural language messages
  * Use single quotes for small symbol-like strings (but break the rules if the strings contain quotes)
  * Use triple double quotes for docstrings and raw string literals for regular expressions even if they aren't needed.
  * Example:

```py
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
```
* Write new code in Python 3.


## Testing with tox

Tox uses py.test under the hood, hence it supports the same syntax for selecting tests.

For further information please consult the `pytest usage docs`_.

To run a particular test class with tox:
```
    $ tox -e py '-k TestFindHooks'
```
To run some tests with names matching a string expression:
```
    $ tox -e py '-k generate'
```
Will run all tests matching "generate", test_generate_files for example.

To run just one method:
```
    $ tox -e py '-k "TestFindHooks and test_find_hook"'
```
To run all tests using various versions of python in virtualenvs defined in tox.ini, just run tox.:
```
    $ tox
```
This configuration file setup the pytest-cov plugin and it is an additional dependency. It generate a coverage report after the tests.

It is possible to tests with some versions of python, to do this the command is:
```
    $ tox -e py27,py34,pypy
```
Will run py.test with the python2.7, python3.4 and pypy interpreters, for example.


## Core Committer Guide

### Vision and Scope

Core committers, use this section to:

* Guide your instinct and decisions as a core committer
* Limit the codebase from growing infinitely

## Command-Line Accessible

* Provides a command-line utility that creates projects from cookiecutters
* Extremely easy to use without having to think too hard
* Flexible for more complex use via optional arguments