Testing with tox
----------------

Tox uses py.test under the hood, hence it supports the same syntax for selecting tests.

For further information please consult the `pytest usage docs`_.

To run a particular test class with tox::

    $ tox -e py '-k TestFindHooks'

To run some tests with names matching a string expression::

    $ tox -e py '-k generate'

Will run all tests matching "generate", test_generate_files for example.

To run just one method::

    $ tox -e py '-k "TestFindHooks and test_find_hook"'


To run all tests using various versions of python in virtualenvs defined in tox.ini, just run tox.::

    $ tox

This configuration file setup the pytest-cov plugin and it is an additional
dependency. It generate a coverage report after the tests.

It is possible to tests with some versions of python, to do this the command
is::

    $ tox -e py27,py35,pypy

Will run py.test with the python2.7, python3.5 and pypy interpreters, for
example.
