==================================
Create a Cookiecutter From Scratch
==================================

Step 1: Name Your Cookiecutter
------------------------------

In this tutorial, we are creating *cookiecutter-website-simple*, a cookiecutter
for generating simple, bare-bones websites.

Create the directory for your cookiecutter and cd into it:

.. code-block:: bash

    $ mkdir cookiecutter-website-simple
    $ cd cookiecutter-website-simple/

Step 2: Create `project_slug` Directory
---------------------------------------

Create a directory called `{{ cookiecutter.project_slug }}`.

This value will be replaced with the repo name of projects that you generate
from this cookiecutter.

Step 3: Create Files
--------------------

Inside of `{{ cookiecutter.project_slug }}`, create `index.html`, `site.css`, and
`site.js`.

To be continued...
