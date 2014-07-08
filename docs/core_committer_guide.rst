Core Committer Guide
====================

.. warning:: This is an early draft and will likely change a lot.

Vision and Scope
-----------------

To help guide us and limit the project from growing infinitely.

TODO

Process: Pull Requests
------------------------

If a pull request is untriaged:

* Look at the roadmap
* Set it for the milestone where it makes the most sense
* Add it to the roadmap

Milestones:

* Follow semantic versioning. See http://semver.org
* If a milestone contains too many pull requests, move some to the next milestone.

How to prioritize pull requests, from most to least important:

#. Fixes for broken tests. Broken means broken on any supported platform or Python version.
#. Minor edits to docs.
#. Bug fixes.
#. Major edits to docs.
#. Features.

Process: Issues
----------------

If an issue is a bug that needs an urgent fix, mark it for the next patch release.
Then either fix it or mark as please-help.

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
B. A coding style that I find simple, minimal, and clean.
C. Access to resources for cross-platform development and testing.
D. Time to devote to the project regularly.
