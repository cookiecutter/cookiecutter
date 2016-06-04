========
Overview
========

Input
-----

This is the directory structure for a simple cookiecutter::

    cookiecutter-something/
    ├── {{ cookiecutter.project_name }}/  <--------- Project template
    │   └── ...
    ├── blah.txt                      <--------- Non-templated files/dirs
    │                                            go outside
    │
    └── cookiecutter.json             <--------- Prompts & default values

You must have:

* A `cookiecutter.json` file.
* A `{{ cookiecutter.project_name }}/` directory, where
  `project_name` is defined in your `cookiecutter.json`.

Beyond that, you can have whatever files/directories you want.

See https://github.com/audreyr/cookiecutter-pypackage for a real-world example
of this.

Output
------

This is what will be generated locally, in your current directory::

    mysomething/  <---------- Value corresponding to what you enter at the
    │                         project_name prompt
    │
    └── ...       <-------- Files corresponding to those in your
                            cookiecutter's `{{ cookiecutter.project_name }}/` dir
