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

* Cover the use cases that the core committers need, and as little as possible beyond that :)
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
* New features require a +1 from 3 core committers

VCS-Hosted Templates
~~~~~~~~~~~~~~~~~~~~~

Cookiecutter project templates are intentionally hosted VCS repos as-is.

* They are easily forkable
* It's easy for users to browse forks and files
* They are searchable via standard Github/Bitbucket/other search interface
* Minimizes the need for packaging-related cruft files
* Easy to create a public project template and host it for free
* Easy to collaborate

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

New features require a +1 from 2 other core committers (besides yourself).

Process: Roadmap
-----------------

The roadmap is https://github.com/audreyr/cookiecutter/milestones?direction=desc&sort=due_date&state=open

Due dates are flexible. Core committers can change them as needed. Note that GitHub sort on them is buggy.

How to number milestones:

* Follow semantic versioning. See http://semver.org

Milestone size:

* If a milestone contains too much, move some to the next milestone.
* Err on the side of more frequent patch releases.

Process: Pull Request merging and HISTORY.rst maintenance
---------------------------------------------------------

If you merge a pull request, you're responsible for updating `AUTHORS.rst` and `HISTORY.rst`

When you're processing the first change after a release, create boilerplate following the existing pattern:

    x.y.z (Development)
    ~~~~~~~~~~~~~~~~~~~

    The goals of this release are TODO: release summary of features

    Features:

    * Feature description, thanks to @contributor (#PR).

    Bug Fixes:

    * Bug fix description, thanks to @contributor (#PR).

    Other changes:

    * Description of the change, thanks to @contributor (#PR). 
                      
    .. _`@contributor`: https://github.com/contributor


Process: Generating CONTRIBUTING.rst
-------------------------------------

From the `cookiecutter` project root::

    $ make contributing

This will generate the following message::

    rm CONTRIBUTING.rst
    touch CONTRIBUTING.rst
    cat docs/contributing.rst >> CONTRIBUTING.rst
    echo "\r\r" >> CONTRIBUTING.rst
    cat docs/types_of_contributions.rst >> CONTRIBUTING.rst
    echo "\r\r" >> CONTRIBUTING.rst
    cat docs/contributor_setup.rst >> CONTRIBUTING.rst
    echo "\r\r" >> CONTRIBUTING.rst
    cat docs/contributor_guidelines.rst >> CONTRIBUTING.rst
    echo "\r\r" >> CONTRIBUTING.rst
    cat docs/contributor_tips.rst >> CONTRIBUTING.rst
    echo "\r\r" >> CONTRIBUTING.rst
    cat docs/core_committer_guide.rst >> CONTRIBUTING.rst
    echo "\r\rAutogenerated from the docs via \`make contributing\`" >> CONTRIBUTING.rst
    echo "WARNING: Don't forget to replace any :ref: statements with literal names"
    WARNING: Don't forget to replace any :ref: statements with literal names

Process: Your own code changes
-------------------------------

All code changes, regardless of who does them, need to be reviewed and merged by someone else.
This rule applies to all the core committers.

Exceptions:

* Minor corrections and fixes to pull requests submitted by others.
* While making a formal release, the release manager can make necessary, appropriate changes.
* Small documentation changes that reinforce existing subject matter. Most commonly being, but not limited to spelling and grammar corrections.

Responsibilities
-----------------

#. Ensure cross-platform compatibility for every change that's accepted. Windows, Mac, Debian & Ubuntu Linux.
#. Ensure that code that goes into core meets all requirements in this checklist: https://gist.github.com/audreyr/4feef90445b9680475f2
#. Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get community feedback.
#. Don't add any classes to the codebase unless absolutely needed. Err on the side of using functions.
#. Keep feature versions as small as possible, preferably one new feature per version.
#. Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See the Python Community Code of Conduct (https://www.python.org/psf/codeofconduct/).

Becoming a Core Committer
--------------------------

Contributors may be given core commit privileges. Preference will be given to those with:

A. Past contributions to Cookiecutter and other open-source projects. Contributions to Cookiecutter include both code (both accepted and pending) and friendly participation in the issue tracker. Quantity and quality are considered.
B. A coding style that the other core committers find simple, minimal, and clean.
C. Access to resources for cross-platform development and testing.
D. Time to devote to the project regularly.
