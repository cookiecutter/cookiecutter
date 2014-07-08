Tips
----

To run a particular test::

    $ python -m unittest tests.test_find.TestFind.test_find_template

To run a subset of tests::

    $ python -m unittest tests.test_find

Troubleshooting for Contributors
---------------------------------

Python 3.3 tests fail locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Try upgrading Tox to the latest version. I noticed that they were failing
locally with Tox 1.5 but succeeding when I upgraded to Tox 1.7.1.
