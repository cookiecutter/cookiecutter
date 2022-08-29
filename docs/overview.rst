========
Overview
========

Cookiecutter takes a template provided as a directory structure with template-files.
Templates can be located in the filesystem, as a ZIP-file or on a VCS-Server (Git/Hg) like GitHub.

It reads a settings file and prompts the user interactively whether or not to change the settings.

Then it takes both and generates an output directory structure from it.

Additionally the template can provide code (Python or shell-script) to be executed before and after generation (pre-gen- and post-gen-hooks).


Input
-----

This is a directory structure for a simple cookiecutter::

    cookiecutter-something/
    ├── {{ cookiecutter.project_name }}/  <--------- Project template
    │   └── ...
    ├── blah.txt                      <--------- Non-templated files/dirs
    │                                            go outside
    │
    └── cookiecutter.json             <--------- Prompts & default values

You must have:

- A ``cookiecutter.json`` file.
- A ``{{ cookiecutter.project_name }}/`` directory, where ``project_name`` is defined in your ``cookiecutter.json``.

Beyond that, you can have whatever files/directories you want.

See https://github.com/audreyfeldroy/cookiecutter-pypackage for a real-world example
of this.

Output
------

This is what will be generated locally, in your current directory::

    mysomething/  <---------- Value corresponding to what you enter at the
    │                         project_name prompt
    │
    └── ...       <-------- Files corresponding to those in your
                            cookiecutter's `{{ cookiecutter.project_name }}/` dir
