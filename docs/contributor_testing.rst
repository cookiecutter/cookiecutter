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

    $ tox -e py27,py34,pypy

Will run py.test with the python2.7, python3.4 and pypy interpreters, for
example.

Troubleshooting for Contributors
---------------------------------

Python 3.3 tests fail locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Try upgrading Tox to the latest version. I noticed that they were failing
locally with Tox 1.5 but succeeding when I upgraded to Tox 1.7.1.

.. _`pytest usage docs`: https://pytest.org/latest/usage.html#specifying-tests-selecting-tests
