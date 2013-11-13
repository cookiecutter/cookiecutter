========
Overview
========

Input
-----

This is the directory structure for a simple cookiecutter::

    cookiecutter-something/
    ├── {{ cookiecutter.repo_name }}/  <--------- Project template
    │   └── ...
    ├── blah.txt                      <--------- Non-templated files/dirs
    │                                            go outside
    │
    └── cookiecutter.json             <--------- Prompts & default values

You must have:

* A `{{ cookiecutter.repo_name }}/` directory.
* A `cookiecutter.json` file.

Beyond that, you can have whatever files/directories you want.

.. note:: As of Cookiecutter 0.7.0, the top-level directory of your
   cookiecutter must be called `{{ cookiecutter.repo_name }}`. However, in the
   future, this will change.

See https://github.com/audreyr/cookiecutter-pypackage for a real-world example
of this.

Output
------

This is what will be generated locally, in your current directory::

    mysomething/  <---------- Value corresponding to what you enter at the
    │                         repo_name prompt
    │
    └── ...       <-------- Files corresponding to those in your
                            cookiecutter's `{{ cookiecutter.repo_name }}/` dir

