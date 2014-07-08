============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. 

.. toctree::
   :numbered:
   :maxdepth: 2

   types_of_contributions
   contributor_setup
   contributor_guidelines
   contributor_tips
   core_committer_guide

Types of Contributions
----------------------

You can contribute in many ways:

Create Cookiecutter Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some other Cookiecutter templates to list in the :ref:`README <readme>` would
be great.

If you create a Cookiecutter template, submit a pull request adding it to
README.rst.

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/audreyr/cookiecutter/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* If you can, provide detailed steps to reproduce the bug.
* If you don't have steps to reproduce the bug, just note your observations in
  as much detail as you can. Questions to start a discussion about the issue
  are welcome.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Cookiecutter could always use more documentation, whether as part of the 
official Cookiecutter docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/audreyr/cookiecutter/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Setting Up the Code for Local Development
-----------------------------------------

Here's how to set up `cookiecutter` for local development.

1. Fork the `cookiecutter` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/cookiecutter.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv cookiecutter
    $ cd cookiecutter/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and flake8::

    $ flake8 cookiecutter tests
    $ python setup.py test
    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Check that the test coverage hasn't dropped::

    coverage run --source cookiecutter setup.py test
    coverage report -m
    coverage html

8. Submit a pull request through the GitHub website.
Contributor Guidelines
-----------------------

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, and PyPy. Check
   https://travis-ci.org/audreyr/cookiecutter/pull_requests and make sure that
   the tests pass for all supported Python versions.

Coding Standards
~~~~~~~~~~~~~~~~

TODO

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

Core Committer Guide
====================

Vision and Scope
-----------------

Core committers, use this section to:

* Guide your instinct and decisions as a core committer
* Limit the codebase from growing infinitely

Command-Line Accessible
~~~~~~~~~~~~~~~~~~~~~~~

* Provides a command-line utility that creates projects from cookiecutters
* Extremely easy to use without having to think too hard
* Flexible for more complex use via optional arguments

API Accessible
~~~~~~~~~~~~~~

* Entirely function-based and stateless (Class-free by intentional design)
* Usable in pieces for developers of template generation tools

Being Jinja2-specific
~~~~~~~~~~~~~~~~~~~~~

* Sets a standard baseline for project template creators, facilitating reuse
* Minimizes the learning curve for those who already use Flask or Django
* Minimizes scope of Cookiecutter codebase

Extensible
~~~~~~~~~~

Being extendable by people with different ideas for Jinja2-based project template tools.

* Entirely function-based
* Aim for statelessness
* Lets anyone write more opinionated tools
    
Freedom for Cookiecutter users to build and extend.

* No officially-maintained cookiecutter templates, only ones by individuals
* Commercial project-friendly licensing, allowing for private cookiecutters and private Cookiecutter-based tools

Fast and Focused
~~~~~~~~~~~~~~~~

Cookiecutter is designed to do one thing, and do that one thing very well.

* Cover the use cases that @audreyr needs, and as little as possible beyond that :)
* Generates project templates from the command-line or API, nothing more
* Minimize internal line of code (LOC) count
* Ultra-fast project generation for high performance downstream tools

Inclusive
~~~~~~~~~

* Cross-platform and cross-version support are more important than features/functionality
* Fixing Windows bugs even if it's a pain, to allow for use by more beginner coders

Stable
~~~~~~

* Aim for 100% test coverage and covering corner cases
* No pull requests will be accepted that drop test coverage on any platform, including Windows
* Conservative decisions patterned after CPython's conservative decisions with stability in mind
* Stable APIs that tool builders can rely on
* New features require a +1 from @audreyr

Process: Pull Requests
------------------------

If a pull request is untriaged:

* Look at the roadmap
* Set it for the milestone where it makes the most sense
* Add it to the roadmap

How to prioritize pull requests, from most to least important:

#. Fixes for broken tests. Broken means broken on any supported platform or Python version.
#. Extra tests to cover corner cases.
#. Minor edits to docs.
#. Bug fixes.
#. Major edits to docs.
#. Features.

Ensure that each pull request meets all requirements in this checklist:
https://gist.github.com/audreyr/4feef90445b9680475f2

Process: Issues
----------------

If an issue is a bug that needs an urgent fix, mark it for the next patch release.
Then either fix it or mark as please-help.

For other issues: encourage friendly discussion, moderate debate, offer your thoughts.

New features require a +1 from @audreyr.

Process: Roadmap
-----------------

How to number milestones:

* Follow semantic versioning. See http://semver.org

Milestone size:

* If a milestone contains too much, move some to the next milestone.
* Err on the side of more frequent patch releases.

Responsibilities
-----------------

#. Give priority to bug fixes over new features. This includes fixes for the Windows tests that broke at some point.
#. Ensure cross-platform compatibility for every change that's accepted. Windows, Mac, Debian & Ubuntu Linux.
#. Ensure that code that goes into core meets all requirements in this checklist: https://gist.github.com/audreyr/4feef90445b9680475f2
#. Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get community feedback.
#. Don't add any classes to the codebase unless absolutely needed. Err on the side of using functions.
#. Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See the Python Community Code of Conduct (https://www.python.org/psf/codeofconduct/).

Becoming a Core Committer
--------------------------

Contributors may be given core commit privileges. Preference will be given to those with:

A. Past contributions to Cookiecutter and other open-source projects. Contributions to Cookiecutter include both code (both accepted and pending) and friendly participation in the issue tracker. Quantity and quality are considered.
B. A coding style that @audreyr finds simple, minimal, and clean.
C. Access to resources for cross-platform development and testing.
D. Time to devote to the project regularly.
Autogenerated from the docs via `make contributing`
