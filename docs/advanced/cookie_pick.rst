.. _cookie_pick:

Migrating Template Changes
--------------------------
Oftentimes changes in the template should be migrated to already instantiated projects.
Using git repositories it's possible to create a patch based on the template commits and apply it to the target
repository by using the `cookie-pick` argument::

    cookiecutter --cookie-pick <hexsha> [--cookie-pick-parent <parent hexsha>]

A temporary patch file is created based on the given commit and its direct parent (or another commit specified by
`cookie-pick-parent`), rendered using the context and transferred to the target repository where it's applied.

It's possible to show the last ten commits in the last 30 days by using the `list` option::

    cookiecutter --cookie-pick list

Changes between non-consecutive commits can be migrated using the `cookie-pick-parent` parameter.

Providing the context
~~~~~~~~~~~~~~~~~~~~~
The context used at creation time has to be provided for the migration (or at least the variables for the `output-dir`
and the changes about to be picked). If the creation was the last one for this template, :ref:`Replay <replay-feature>` can be used::

    cookiecutter --replay --cookie-pick <hexsha>

Otherwise you can :ref:`inject the context <injecting-extra-content>` or
use :ref:`the existing context providers <suppressing-command-line-prompts>`.

Error handling
~~~~~~~~~~~~~~
1. If the target directory is not a valid Git repository an error is raised and the patch file's location is given which
can be used to apply it manually.

2. If the patch could not be applied to the target repository the rejected patch is left at the target directory to
manually apply it.