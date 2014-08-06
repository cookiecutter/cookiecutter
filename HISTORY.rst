.. :changelog:

History
-------

In Development (Master Branch)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** Up to July 9 only. Need to finish adding material.

Bug Fixes:

* Fixed the contributing file so it displays nicely in Github, thanks to `@pydanny`_.
* Updates 2.6 requirements to include simplejson, thanks to `@saxix`_.
* Avoid unwanted extra spaces in string literal, thanks to `@merwok`_.
* Fix `@unittest.skipIf` error on Python 2.6.
* Let sphinx parse `:param:` properly by inserting newlines #213, thanks to `@mineo`_.
* Fixed Windows test prompt failure by replacing stdin per `@cjrh`_ in #195.
* Made rmtree remove readonly files, thanks to `@pfmoore`_.
* Now using tox to run tests on Appveyor, thanks to `@pfmoore`_ (#241).
* Fixed tests that assumed the system encoding was utf-8, thanks to `@pfmoore`_ (#242, #244).
* Added a tox ini file that uses py.test, thanks to `@pfmoore`_ (#245).

.. _`@merwok`: https://github.com/merwok
.. _`@mineo`: https://github.com/mineo
.. _`@cjrh`: https://github.com/cjrh

Other Changes:

* `@audreyr`_ formally accepted position as **BDFL of cookiecutter**.
* Elevated `@pydanny`_, `@michaeljoseph`_, and `@pfmoore`_ to core committer status.
* Added Core Committer guide, by `@audreyr`_.
* Generated apidocs from `make docs`, by `@audreyr`_.
* Added `contributing` command to the `make docs` function, by `@pydanny`_.
* Refactored contributing documentation, included adding core committer instructions, by `@pydanny`_ and `@audreyr`_.
* Do not convert input prompt to bytes, thanks to `@uranusjr`_ (#192).
* Added troubleshooting info about Python 3.3 tests and tox.
* Added documentation about command line arguments, thanks to `@saxix`_.
* Style cleanups.
* Added environment variable to disable network tests for environments without networking, thanks to `@vincentbernat`_.
* Added Appveyor support to aid Windows integrations, thanks to `@pydanny`_ (#215).
* CONTRIBUTING.rst is now generated via `make contributing`, thanks to `@pydanny`_ (#220).
* Removed unnecessary endoing argument to `json.load`, thanks to `@pfmoore`_ (#234).
* Now generating shell hooks dynamically for Unix/Windows portability, thanks to `@pfmoore`_ (#236).
* Removed non-portable assumptions about directory structure, thanks to `@pfmoore`_ (#238).
* Added a note on portability to the hooks documentation, thanks to `@pfmoore`_ (#239).
* Replaced `unicode_open` with direct use of `io.open`, thanks to `@pfmoore`_ (#229).
* Added more Cookiecutters to the list:

  * `cookiecutter-kivy`_ by `@hackebrot`_
  * BoilerplatePP_ by `@Paspartout`_
  * `cookiecutter-pypackage-minimal`_ by `@borntyping`_
  * `cookiecutter-ansible-role`_ by `@iknite`_
  * `cookiecutter-pylibrary`_ by `@ionelmc`_
  * `cookiecutter-pylibrary-minimal`_ by `@ionelmc`_


.. _`cookiecutter-kivy`: https://github.com/hackebrot/cookiecutter-kivy
.. _`cookiecutter-ansible-role`: https://github.com/iknite/cookiecutter-ansible-role
.. _BoilerplatePP: https://github.com/Paspartout/BoilerplatePP
.. _`cookiecutter-pypackage-minimal`: https://github.com/borntyping/cookiecutter-pypackage-minimal
.. _`cookiecutter-pylibrary`: https://github.com/ionelmc/cookiecutter-pylibrary
.. _`cookiecutter-pylibrary-minimal`: https://github.com/ionelmc/cookiecutter-pylibrary-minimal

.. _`@michaeljoseph`: https://github.com/michaeljoseph
.. _`@iknite`: https://github.com/iknite
.. _`@borntyping`: https://github.com/borntyping
.. _`@Paspartout`: https://github.com/Paspartout
.. _`@pfmoore`: https://github.com/pfmoore
.. _`@audreyr`: https://github.com/audreyr
.. _`@uranusjr`: https://github.com/uranusjr
.. _`@saxix`: https://github.com/saxix
.. _`@hackebrot`: https://github.com/hackebrot
.. _`@ionelmc`: https://github.com/ionelmc



0.7.1 (2014-04-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Bug fixes:

* Use the current Python interpreter to run Python hooks, thanks to
  `@coderanger`_.
* Include tests and documentation in source distribution, thanks to
  `@vincentbernat`_.
* Fix various warnings and missing things in the docs (#129, #130),
  thanks to `@nedbat`_.
* Add command line option to get version (#89), thanks to `@davedash`_
  and `@cyberj`_.

Other changes:

* Add more Cookiecutters to the list:

  * `cookiecutter-avr`_ by `@solarnz`_
  * `cookiecutter-tumblr-theme`_ by `@relekang`_
  * `cookiecutter-django-paas`_ by `@pbacterio`_

.. _`@coderanger`: https://github.com/coderanger
.. _`@vincentbernat`: https://github.com/vincentbernat
.. _`@nedbat`: https://github.com/nedbat
.. _`@davedash`: https://github.com/davedash
.. _`@cyberj`: https://github.com/cyberj

.. _`cookiecutter-avr`: https://github.com/solarnz/cookiecutter-avr
.. _`@solarnz`: https://github.com/solarnz
.. _`cookiecutter-tumblr-theme`: https://github.com/relekang/cookiecutter-tumblr-theme
.. _`@relekang`: https://github.com/relekang
.. _`cookiecutter-django-paas`: https://github.com/pbacterio/cookiecutter-django-paas
.. _`@pbacterio`: https://github.com/pbacterio

0.7.0 (2013-11-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a release with significant improvements and changes. Please read
through this list before you upgrade.

New features:

* Support for --checkout argument, thanks to `@foobacca`_.
* Support for pre-generate and post-generate hooks, thanks to `@raphigaziano`_.
  Hooks are Python or shell scripts that run before and/or after your project
  is generated.
* Support for absolute paths to cookiecutters, thanks to `@krallin`_.
* Support for Mercurial version control system, thanks to `@pokoli`_.
* When a cookiecutter contains invalid Jinja2 syntax, you get a better message
  that shows the location of the TemplateSyntaxError. Thanks to `@benjixx`_.
* Can now prompt the user to enter values during generation from a local
  cookiecutter, thanks to `@ThomasChiroux`_. This is now always the default
  behavior. Prompts can also be supressed with `--no-input`.
* Your cloned cookiecutters are stored by default in your `~/.cookiecutters/`
  directory (or Windows equivalent). The location is configurable. (This is a
  major change from the pre-0.7.0 behavior, where cloned cookiecutters were
  deleted at the end of project generation.) Thanks `@raphigaziano`_.
* User config in a `~/.cookiecutterrc` file, thanks to `@raphigaziano`_.
  Configurable settings are `cookiecutters_dir` and `default_context`.
* File permissions are now preserved during project generation, thanks to
  `@benjixx`_.

Bug fixes:

* Unicode issues with prompts and answers are fixed, thanks to `@s-m-i-t-a`_.
* The test suite now runs on Windows, which was a major effort. Thanks to 
  `@pydanny`_, who collaborated on this with me.

Other changes:

* Quite a bit of refactoring and API changes.
* Lots of documentation improvements. Thanks `@sloria`_, `@alex`_, `@pydanny`_,
  `@freakboy3742`_, `@es128`_, `@rolo`_.
* Better naming and organization of test suite.
* A `CookiecutterCleanSystemTestCase` to use for unit tests affected by the
  user's config and cookiecutters directory.
* Improvements to the project's Makefile.
* Improvements to tests. Thanks `@gperetin`_, `@s-m-i-t-a`_.
* Removal of `subprocess32` dependency. Now using non-context manager version
  of `subprocess.Popen` for Python 2 compatibility.
* Removal of cookiecutter's `cleanup` module.
* A bit of `setup.py` cleanup, thanks to `@oubiga`_.
* Now depends on binaryornot 0.2.0.

.. _`@foobacca`: https://github.com/foobacca/
.. _`@raphigaziano`: https://github.com/raphigaziano/
.. _`@gperetin`: https://github.com/gperetin/
.. _`@krallin`: https://github.com/krallin/
.. _`@pokoli`: https://github.com/pokoli/
.. _`@benjixx`: https://github.com/benjixx/
.. _`@ThomasChiroux`: https://github.com/ThomasChiroux/
.. _`@s-m-i-t-a`: https://github.com/s-m-i-t-a/
.. _`@sloria`: https://github.com/sloria/
.. _`@alex`: https://github.com/alex/
.. _`@pydanny`: https://github.com/pydanny/
.. _`@freakboy3742`: https://github.com/freakboy3742/
.. _`@es128`: https://github.com/es128/
.. _`@rolo`: https://github.com/rolo/
.. _`@oubiga`: https://github.com/oubiga/

0.6.4 (2013-08-21)
~~~~~~~~~~~~~~~~~~

* Windows support officially added.
* Fix TemplateNotFound Exception on Windows (#37).

0.6.3 (2013-08-20)
~~~~~~~~~~~~~~~~~~

* Fix copying of binary files in nested paths (#41), thanks to `@sloria`_.

.. _`@sloria`: https://github.com/sloria/

0.6.2 (2013-08-19)
~~~~~~~~~~~~~~~~~~

* Depend on Jinja2>=2.4 instead of Jinja2==2.7.
* Fix errors on attempt to render binary files. Copy them over from the project
  template without rendering.
* Fix Python 2.6/2.7 `UnicodeDecodeError` when values containing Unicode chars
  are in `cookiecutter.json`.
* Set encoding in Python 3 `unicode_open()` to always be utf-8.

0.6.1 (2013-08-12)
~~~~~~~~~~~~~~~~~~

* Improved project template finding. Now looks for the occurrence of `{{`,
  `cookiecutter`, and `}}` in a directory name.
* Fix help message for input_dir arg at command prompt.
* Minor edge cases found and corrected, as a result of improved test coverage.

0.6.0 (2013-08-08)
~~~~~~~~~~~~~~~~~~

* Config is now in a single `cookiecutter.json` instead of in `json/`.
* When you create a project from a git repo template, Cookiecutter prompts
  you to enter custom values for the fields defined in `cookiecutter.json`.

0.5 (2013-07-28)
~~~~~~~~~~~~~~~~~~

* Friendlier, more simplified command line usage::

    # Create project from the cookiecutter-pypackage/ template
    $ cookiecutter cookiecutter-pypackage/
    
    # Create project from the cookiecutter-pypackage.git repo template
    $ cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

* Can now use Cookiecutter from Python as a package::

    from cookiecutter.main import cookiecutter
    
    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')

* Internal refactor to remove any code that changes the working directory.

0.4 (2013-07-22)
~~~~~~~~~~~~~~~~~~

* Only takes in one argument now: the input directory. The output directory
  is generated by rendering the name of the input directory.
* Output directory cannot be the same as input directory.

0.3 (2013-07-17)
~~~~~~~~~~~~~~~~~~

* Takes in command line args for the input and output directories.

0.2.1 (2013-07-17)
~~~~~~~~~~~~~~~~~~

* Minor cleanup.

0.2 (2013-07-17)
~~~~~~~~~~~~~~~~~~

Bumped to "Development Status :: 3 - Alpha".

* Works with any type of text file.
* Directory names and filenames can be templated.

0.1.0 (2013-07-11)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.

Roadmap
-------

https://github.com/audreyr/cookiecutter/issues/milestones

