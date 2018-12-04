.. :changelog:

History
-------

1.7.0 (????-??-??) ???????
~~~~~~~~~~~~~~~~~~~~~~~~~~

Important Changes:

* Drop support for EOL Python 3.3, thanks to `@hugovk`_ (#1024)

.. _`@hugovk`: https://github.com/hugovk

Other Changes:

* Add a `CODE_OF_CONDUCT.md`_ file to the project, thanks to
  `@andreagrandi`_ (#1009)
* Update docstrings in ``cookiecutter/main.py``, ``cookiecutter/__init__.py``,
  and ``cookiecutter/log.py`` to follow the PEP 257 style guide, thanks to
  `@meahow`_ (#998, #999, #1000)
* Update docstrings in ``cookiecutter/utils.py`` to follow the PEP 257 style
  guide, thanks to `@dornheimer`_ (#1026)
* Fix grammar in *Choice Variables* documentation, thanks to `@jubrilissa`_
  (#1011)
* Update installation docs with links to the Windows Subsystem and GNU
  utilities, thanks to `@Nythiennzo`_ for the PR and `@BruceEckel`_ for the
  review (#1016)
* Upgrade flake8 to version 3.5.0, thanks to `@cclauss`_ (#1038)
* Update tutorial with explanation for how cookiecutter finds the template
  file, thanks to `@accraze`_ (#1025)
* Update CI config files to use ``TOXENV`` environment variable, thanks to
  `@asottile`_ (#1019)
* Improve user documentation for writing hooks, thanks to `@jonathansick`_
  (#1057)
* Make sure to preserve the order of items in the generated cookiecutter
  context, thanks to `@hackebrot`_ (#1074)
* Add more cookiecutter templates to the mix:

  * `cookiecutter-python-cli`_ by `@xuanluong`_ (#1003)
  * `cookiecutter-docker-science`_ by `@takahi-i`_ (#1040)
  * `cookiecutter-flask-skeleton`_ by `@mjhea0`_ (#1052)
  * `cookiecutter-awesome`_ by `@Pawamoy`_ (#1051)
  * `cookiecutter-flask-ask`_ by `@machinekoder`_ (#1056)
  * `cookiecutter-data-driven-journalism`_ by `@JAStark`_ (#1020)
  * `cookiecutter-tox-plugin`_ by `@obestwalter`_ (#1103)

.. _`cookiecutter-python-cli`: https://github.com/xuanluong/cookiecutter-python-cli
.. _`cookiecutter-docker-science`: https://github.com/docker-science/cookiecutter-docker-science
.. _`cookiecutter-flask-skeleton`: https://github.com/realpython/cookiecutter-flask-skeleton
.. _`cookiecutter-awesome`: https://github.com/Pawamoy/cookiecutter-awesome
.. _`cookiecutter-flask-ask`: https://github.com/chrisvoncsefalvay/cookiecutter-flask-ask
.. _`cookiecutter-data-driven-journalism`: https://github.com/jastark/cookiecutter-data-driven-journalism
.. _`cookiecutter-tox-plugin`: https://github.com/tox-dev/cookiecutter-tox-plugin

.. _`CODE_OF_CONDUCT.md`: https://github.com/audreyr/cookiecutter/blob/master/CODE_OF_CONDUCT.md

.. _`@xuanluong`: https://github.com/xuanluong
.. _`@andreagrandi`: https://github.com/andreagrandi
.. _`@jubrilissa`: https://github.com/jubrilissa
.. _`@Nythiennzo`: https://github.com/Nythiennzo
.. _`@takahi-i`: https://github.com/takahi-i
.. _`@dornheimer`: https://github.com/dornheimer
.. _`@Pawamoy`: https://github.com/Pawamoy
.. _`@cclauss`: https://github.com/cclauss
.. _`@accraze`: https://github.com/accraze
.. _`@asottile`: https://github.com/asottile
.. _`@jonathansick`: https://github.com/jonathansick
.. _`@machinekoder`: https://github.com/machinekoder
.. _`@JAStark`: https://github.com/JAStark
.. _`@obestwalter`: https://github.com/obestwalter


1.6.0 (2017-10-15) Tim Tam
~~~~~~~~~~~~~~~~~~~~~~~~~~

New Features:

* Include template path or template URL in cookiecutter context under
  ``_template``, thanks to `@aroig`_ (#774)
* Add a URL abbreviation for GitLab template projects, thanks to `@hackebrot`_
  (#963)
* Add option to use templates from Zip files or Zip URLs, thanks to
  `@freakboy3742`_ (#961)

Bug Fixes:

* Fix an issue with missing default template abbreviations for when a user
  defined custom abbreviations, thanks to `@noirbizarre`_ for the issue report
  and `@hackebrot`_ for the fix (#966, #967)
* Preserve existing output directory on project generation failure, thanks to
  `@ionelmc`_ for the report and `@michaeljoseph`_ for the fix (#629, #964)
* Fix Python 3.x error handling for ``git`` operation failures, thanks to `@jmcarp`_
  (#905)

Other Changes:

* Fix broken link to *Copy without Render* docs, thanks to `@coreysnyder04`_
  (#912)
* Improve debug log message for when a hook is not found, thanks to
  `@raphigaziano`_ (#160)
* Fix module summary and ``expand_abbreviations()`` doc string as per pep257,
  thanks to `@terryjbates`_ (#772)
* Update doc strings in ``cookiecutter/cli.py`` and ``cookiecutter/config.py``
  according to pep257, thanks to `@terryjbates`_ (#922, #931)
* Update doc string for ``is_copy_only_path()`` according to pep257, thanks to
  `@mathagician`_ and `@terryjbates`_ (#935, #949)
* Update doc strings in ``cookiecutter/extensions.py`` according to pep257,
  thanks to `@meahow`_ (#996)
* Fix miscellaneous issues with building docs, thanks to `@stevepiercy`_ (#889)
* Re-implement Makefile and update several make rules, thanks to `@hackebrot`_
  (#930)
* Fix broken link to pytest docs, thanks to `@eyalev`_ for the issue report and
  `@devstrat`_ for the fix (#939, #940)
* Add ``test_requirements.txt`` file for easier testing outside of tox, thanks
  to `@ramnes`_ (#945)
* Improve wording in *copy without render* docs, thanks to `@eyalev`_ (#938)
* Fix a number of typos, thanks to `@delirious-lettuce`_ (#968)
* Improved *extra context* docs by noting that extra context keys must be
  present in the template's ``cookiecutter.json``, thanks to `@karantan`_ for
  the report and fix (#863, #864)
* Added more cookiecutter templates to the mix:

  * `cookiecutter-kata-cpputest`_ by `@13coders`_ (#901)
  * `cookiecutter-kata-gtest`_ by `@13coders`_ (#901)
  * `cookiecutter-pyramid-talk-python-starter`_ by `@mikeckennedy`_ (#915)
  * `cookiecutter-android`_ by `@alexfu`_ (#890)
  * `cookiecutter-lux-python`_ by `@alexkey`_ (#895)
  * `cookiecutter-git`_ by `@tuxredux`_ (#921)
  * `cookiecutter-ansible-role-ci`_ by `@ferrarimarco`_ (#903)
  * `cookiecutter_dotfile`_ by `@bdcaf`_ (#925)
  * `painless-continuous-delivery`_ by `@painless-software`_ (#927)
  * `cookiecutter-molecule`_ by `@retr0h`_ (#954)
  * `sublime-snippet-package-template`_ by `@agenoria`_ (#956)
  * `cookiecutter-conda-python`_ by `@conda`_ (#969)
  * `cookiecutter-flask-minimal`_ by `@candidtim`_ (#977)
  * `cookiecutter-pypackage-rust-cross-platform-publish`_ by `@mckaymatt`_ (#957)
  * `cookie-cookie`_ by `@tuxredux`_ (#951)
  * `cookiecutter-telegram-bot`_ by `@Ars2014`_ (#984)
  * `python-project-template`_ by `@Kwpolska`_ (#986)
  * `wemake-django-template`_ by `@wemake-services`_ (#990)
  * `cookiecutter-raml`_ by `@genzj`_ (#994)
  * `cookiecutter-anyblok-project`_ by `@AnyBlok`_ (#988)
  * `cookiecutter-devenv`_ by `@greenguavalabs`_ (#991)

.. _`cookiecutter-kata-gtest`: https://github.com/13coders/cookiecutter-kata-gtest
.. _`cookiecutter-kata-cpputest`: https://github.com/13coders/cookiecutter-kata-cpputest
.. _`cookiecutter-pyramid-talk-python-starter`: https://github.com/mikeckennedy/cookiecutter-pyramid-talk-python-starter
.. _`cookiecutter-android`: https://github.com/alexfu/cookiecutter-android
.. _`cookiecutter-lux-python`: https://github.com/alexkey/cookiecutter-lux-python
.. _`cookiecutter-git`: https://github.com/webevllc/cookiecutter-git
.. _`cookiecutter_dotfile`: https://github.com/bdcaf/cookiecutter_dotfile
.. _`cookiecutter-ansible-role-ci`: https://github.com/ferrarimarco/cookiecutter-ansible-role
.. _`painless-continuous-delivery`: https://github.com/painless-software/painless-continuous-delivery
.. _`cookiecutter-molecule`: https://github.com/retr0h/cookiecutter-molecule
.. _`sublime-snippet-package-template`: https://github.com/agenoria/sublime-snippet-package-template
.. _`cookiecutter-conda-python`: https://github.com/conda/cookiecutter-conda-python
.. _`cookiecutter-flask-minimal`: https://github.com/candidtim/cookiecutter-flask-minimal
.. _`cookiecutter-pypackage-rust-cross-platform-publish`: https://github.com/mckaymatt/cookiecutter-pypackage-rust-cross-platform-publish
.. _`cookie-cookie`: https://github.com/tuxredux/cookie-cookie
.. _`cookiecutter-telegram-bot`: https://github.com/Ars2014/cookiecutter-telegram-bot
.. _`python-project-template`: https://github.com/Kwpolska/python-project-template
.. _`wemake-django-template`: https://github.com/wemake-services/wemake-django-template
.. _`cookiecutter-raml`: https://github.com/genzj/cookiecutter-raml
.. _`cookiecutter-anyblok-project`: https://github.com/AnyBlok/cookiecutter-anyblok-project
.. _`cookiecutter-devenv`: https://bitbucket.org/greenguavalabs/cookiecutter-devenv.git

.. _`@13coders`: https://github.com/13coders
.. _`@coreysnyder04`: https://github.com/coreysnyder04
.. _`@mikeckennedy`: https://github.com/mikeckennedy
.. _`@alexfu`: https://github.com/alexfu
.. _`@alexkey`: https://github.com/alexkey
.. _`@tuxredux`: https://github.com/tuxredux
.. _`@ferrarimarco`: https://github.com/ferrarimarco
.. _`@eyalev`: https://github.com/eyalev
.. _`@devstrat`: https://github.com/devstrat
.. _`@mathagician`: https://github.com/mathagician
.. _`@bdcaf`: https://github.com/bdcaf
.. _`@ramnes`: https://github.com/ramnes
.. _`@painless-software`: https://github.com/painless-software
.. _`@retr0h`: https://github.com/retr0h
.. _`@agenoria`: https://github.com/agenoria
.. _`@noirbizarre`: https://github.com/noirbizarre
.. _`@delirious-lettuce`: https://github.com/delirious-lettuce
.. _`@conda`: https://github.com/conda
.. _`@candidtim`: https://github.com/candidtim
.. _`@mckaymatt`: https://github.com/mckaymatt
.. _`@karantan`: https://github.com/karantan
.. _`@jmcarp`: https://github.com/jmcarp
.. _`@Ars2014`: https://github.com/Ars2014
.. _`@Kwpolska`: https://github.com/Kwpolska
.. _`@wemake-services`: https://github.com/wemake-services
.. _`@genzj`: https://github.com/genzj
.. _`@AnyBlok`: https://github.com/AnyBlok
.. _`@greenguavalabs`: https://bitbucket.org/greenguavalabs
.. _`@meahow`: https://github.com/meahow

1.5.1 (2017-02-04) Alfajor
~~~~~~~~~~~~~~~~~~~~~~~~~~

New Features:

* Major update to installation documentation, thanks to `@stevepiercy`_ (#880)

Bug Fixes:

* Resolve an issue around default values for dict variables, thanks to
  `@e-kolpakov`_ for raising the issue and `@hackebrot`_ for the PR (#882,
  #884)

Other Changes:

* Contributor documentation reST fixes, thanks to `@stevepiercy`_ (#878)
* Added more cookiecutter templates to the mix:

  * `widget-cookiecutter`_ by `@willingc`_ (#781)
  * `cookiecutter-django-foundation`_ by `@Parbhat`_ (#804)
  * `cookiecutter-tornado`_ by `@hkage`_ (#807)
  * `cookiecutter-django-ansible`_ by `@Ivaylo-Bachvarov`_ (#816)
  * `CICADA`_ by `@elenimijalis`_ (#840)
  * `cookiecutter-tf-module`_ by `@VDuda`_ (#843)
  * `cookiecutter-pyqt4`_ by `@aeroaks`_ (#847)
  * `cookiecutter-golang`_ by `@mjhea0`_ and `@lacion`_ (#872, #873)
  * `cookiecutter-elm`_, `cookiecutter-java`_ and `cookiecutter-spring-boot`_ by `@m-x-k`_ (#879)

.. _`@Parbhat`: https://github.com/Parbhat
.. _`@hkage`: https://github.com/hkage
.. _`@Ivaylo-Bachvarov`: https://github.com/Ivaylo-Bachvarov
.. _`@elenimijalis`: https://github.com/elenimijalis
.. _`@VDuda`: https://github.com/VDuda
.. _`@aeroaks`: https://github.com/aeroaks
.. _`@mjhea0`: https://github.com/mjhea0
.. _`@lacion`: https://github.com/lacion
.. _`@m-x-k`: https://github.com/m-x-k
.. _`@e-kolpakov`: https://github.com/e-kolpakov

.. _`widget-cookiecutter`: https://github.com/jupyter/widget-cookiecutter
.. _`cookiecutter-django-foundation`: https://github.com/Parbhat/cookiecutter-django-foundation
.. _`cookiecutter-tornado`: https://github.com/hkage/cookiecutter-tornado
.. _`cookiecutter-django-ansible`: https://github.com/HackSoftware/cookiecutter-django-ansible
.. _`CICADA`: https://github.com/TAMU-CPT/CICADA
.. _`cookiecutter-tf-module`: https://github.com/DualSpark/cookiecutter-tf-module
.. _`cookiecutter-pyqt4`: https://github.com/aeroaks/cookiecutter-pyqt4
.. _`cookiecutter-golang`: https://github.com/lacion/cookiecutter-golang
.. _`cookiecutter-elm`: https://github.com/m-x-k/cookiecutter-elm.git
.. _`cookiecutter-java`: https://github.com/m-x-k/cookiecutter-java.git
.. _`cookiecutter-spring-boot`: https://github.com/m-x-k/cookiecutter-spring-boot.git


1.5.0 (2016-12-18) Alfajor
~~~~~~~~~~~~~~~~~~~~~~~~~~

The primary goal of this release was to add command-line support for passing
extra context, address minor bugs and make a number of improvements.

New Features:

* Inject extra context with command-line arguments, thanks to `@msabramo`_ and
  `@michaeljoseph`_ (#666).
* Updated conda installation instructions to work with the new conda-forge
  distribution of Cookiecutter, thanks to `@pydanny`_ and especially
  `@bollwyvl`_ (#232, #705).
* Refactor code responsible for interaction with version control systems and
  raise better error messages, thanks to `@michaeljoseph`_ (#778).
* Add support for executing cookiecutter using ``python -m cookiecutter`` or
  from a checkout/zip file, thanks to `@brettcannon`_ (#788).
* New CLI option ``--debug-file PATH`` to store a log file on disk. By default
  no log file is written.  Entries for ``DEBUG`` level and higher. Thanks to
  `@hackebrot`_ (#792).
* Existing templates in a user's ``cookiecutters_dir`` (default is
  ``~/.cookiecutters/``) can now be referenced by directory name, thanks to
  `@michaeljoseph`_ (#825).
* Add support for dict values in ``cookiecutter.json``, thanks to
  `@freakboy3742`_ and `@hackebrot`_ (#815, #858).
* Add a ``jsonify`` filter to default jinja2 extensions that json.dumps a
  Python object into a string, thanks to `@aroig`_ (#791).

Bug Fixes:

* Fix typo in the error logging text for when a hook did not exit successfully,
  thanks to `@luzfcb`_ (#656)
* Fix an issue around **replay** file names when **cookiecutter** is used with
  a relative path to a template, thanks to `@eliasdorneles`_ for raising the
  issue and `@hackebrot`_ for the PR (#752, #753)
* Ignore hook files with tilde-suffixes, thanks to `@hackebrot`_ (#768)
* Fix a minor issue with the code that generates a name for a template, thanks
  to `@hackebrot`_ (#798)
* Handle empty hook file or other OS errors, thanks to `@christianmlong`_ for
  raising this bug and `@jcarbaugh`_ and `@hackebrot`_ for the fix (#632, #729,
  #862)
* Resolve an issue with custom extensions not being loaded for
  ``pre_gen_project`` and ``post_gen_project`` hooks, thanks to `@cheungnj`_
  (#860)

Other Changes:

* Remove external dependencies from tests, so that tests can be run w/o network
  connection, thanks to `@hackebrot`_ (#603)
* Remove execute permissions on Python files, thanks to `@mozillazg`_ (#650)
* Report code coverage info from AppVeyor build to codecov, thanks to
  `@ewjoachim`_ (#670)
* Documented functions and methods lacking documentation, thanks to `@pydanny`_
  (#673)
* Documented ``__init__`` methods for Environment objects, thanks to
  `@pydanny`_ (#677)
* Updated whichcraft to 0.4.0, thanks to `@pydanny`_.
* Updated documentation link to Read the Docs, thanks to `@natim`_ (#687)
* Moved cookiecutter templates and added category links, thanks to
  `@willingc`_ (#674)
* Added Github Issue Template, thanks to `@luzfcb`_ (#700)
* Added ``ssh`` repository examples, thanks to `@pokoli`_ (#702)
* Fix links to the cookiecutter-data-science template and its documentation,
  thanks to `@tephyr`_ for the PR and `@willingc`_ for the review (#711, #714)
* Update link to docs for Django's ``--template`` command line option, thanks
  to `@purplediane`_ (#754)
* Create *hook backup files* during the tests as opposed to having them as
  static files in the repository, thanks to `@hackebrot`_ (#789)
* Applied PEP 257 docstring conventions to:

  * ``environment.py``, thanks to `@terryjbates`_ (#759)
  * ``find.py``, thanks to `@terryjbates`_ (#761)
  * ``generate.py``, thanks to `@terryjbates`_ (#764)
  * ``hooks.py``, thanks to `@terryjbates`_ (#766)
  * ``repository.py``, thanks to `@terryjbates`_ (#833)
  * ``vcs.py``, thanks to `@terryjbates`_ (#831)

* Fix link to the Tryton cookiecutter, thanks to `@cedk`_
  and `@nicoe`_ (#697, #698)
* Added PyCon US 2016 sponsorship to README, thanks to `@purplediane`_ (#720)
* Added a sprint contributor doc, thanks to `@phoebebauer`_ (#727)
* Converted readthedocs links (.org -> .io), thanks to `@adamchainz`_ (#718)
* Added Python 3.6 support, thanks to `@suledev`_ (#728)
* Update occurrences of ``repo_name`` in documentation, thanks to
  `@palmerev`_ (#734)
* Added case studies document, thanks to `@pydanny`_ (#735)
* Added first steps cookiecutter creation tutorial, thanks to
  `@BruceEckel`_ (#736)
* Reorganised tutorials and setup git submodule to external tutorial, thanks
  to `@dot2dotseurat`_ (#740)
* Debian installation instructions, thanks to `@ivanlyon`_ (#738)
* Usage documentation typo fix., thanks to `@terryjbates`_ (#739)
* Updated documentation copyright date, thanks to `@zzzirk`_ (#747)
* Add a make rule to update git submodules, thanks to `@hackebrot`_ (#746)
* Split up advanced usage docs, thanks to `@zzzirk`_ (#749)
* Documentation for the ``no_input`` option, thanks to `@pokoli`_ (#701)
* Remove unnecessary shebangs from python files, thanks to `@michaeljoseph`_
  (#763)
* Refactor cookiecutter template identification, thanks to `@michaeljoseph`_
  (#777)
* Add a ``cli_runner`` test fixture to simplify CLI tests, thanks to
  `@hackebrot`_ (#790)
* Add a check to ensure cookiecutter repositories have JSON context, thanks to
  `@michaeljoseph`_ (#782)
* Rename the internal function that determines whether a file should be
  rendered, thanks to `@audreyr`_ for raising the issue and `@hackebrot`_ for
  the PR (#741, #802)
* Fix typo in docs, thanks to `@mwarkentin`_ (#828)
* Fix broken link to *Invoke* docs, thanks to `@B3QL`_ (#820)
* Add documentation to ``render_variable`` function in ``prompt.py``, thanks to
  `@pydanny`_ (#678)
* Fix python3.6 travis-ci and tox configuration, thanks to `@luzfcb`_ (#844)
* Add missing encoding declarations to python files, thanks to `@andytom`_
  (#852)
* Disable poyo logging for tests, thanks to `@hackebrot`_ (#855)
* Remove pycache directories in make clean-pyc, thanks to `@hackebrot`_ (#849)
* Refactor hook system to only find the requested hook, thanks to
  `@michaeljoseph`_ (#834)
* Add tests for custom extensions in ``pre_gen_project`` and
  ``post_gen_project`` hooks, thanks to `@hackebrot`_ (#856)
* Make the build reproducible by avoiding nondeterministic keyword arguments,
  thanks to `@lamby`_ and `@hackebrot`_ (#800, #861)
* Extend CLI help message and point users to the github project to engage with
  the community, thanks to `@hackebrot`_ (#859)
* Added more cookiecutter templates to the mix:

  * `cookiecutter-funkload-friendly`_ by `@tokibito`_ (#657)
  * `cookiecutter-reveal.js`_ by `@keimlink`_ (#660)
  * `cookiecutter-python-app`_ by `@mdklatt`_ (#659)
  * `morepath-cookiecutter`_ by `@href`_ (#672)
  * `hovercraft-slides`_ by `@jhermann`_ (#665)
  * `cookiecutter-es6-package`_ by `@ratson`_ (#667)
  * `cookiecutter-webpack`_ by `@hzdg`_ (#668)
  * `cookiecutter-django-herokuapp`_ by `@dulaccc`_ (#374)
  * `cookiecutter-django-aws-eb`_ by `@peterlauri`_ (#626)
  * `wagtail-starter-kit`_ by `@tkjone`_ (#658)
  * `cookiecutter-dpf-effect`_ by `@SpotlightKid`_ (#663)
  * `cookiecutter-dpf-audiotk`_ by `@SpotlightKid`_ (#663)
  * `cookiecutter-template`_ by `@eviweb`_ (#664)
  * `cookiecutter-angular2`_ by `@matheuspoleza`_ (#675)
  * `cookiecutter-data-science`_ by `@pjbull`_ (#680)
  * `cc_django_ember_app`_ by `@nanuxbe`_ (#686)
  * `cc_project_app_drf`_ by `@nanuxbe`_ (#686)
  * `cc_project_app_full_with_hooks`_ by `@nanuxbe`_ (#686)
  * `beat-generator`_ by `@ruflin`_ (#695)
  * `cookiecutter-scala`_ by `@Plippe`_ (#751)
  * `cookiecutter-snakemake-analysis-pipeline`_ by `@xguse`_ (#692)
  * `cookiecutter-py3tkinter`_ by `@ivanlyon`_ (#730)
  * `pyramid-cookiecutter-alchemy`_ by `@stevepiercy`_ (#745)
  * `pyramid-cookiecutter-starter`_ by `@stevepiercy`_ (#745)
  * `pyramid-cookiecutter-zodb`_ by `@stevepiercy`_ (#745)
  * `substanced-cookiecutter`_ by `@stevepiercy`_ (#745)
  * `cookiecutter-simple-django-cn`_ by `@shenyushun`_ (#765)
  * `cookiecutter-pyqt5`_ by `@mandeepbhutani`_ (#797)
  * `cookiecutter-xontrib`_ by `@laerus`_ (#817)
  * `cookiecutter-reproducible-science`_ by `@mkrapp`_ (#826)
  * `cc-automated-drf-template`_ by `@elenimijalis`_ (#832)

.. _`@keimlink`: https://github.com/keimlink
.. _`@luzfcb`: https://github.com/luzfcb
.. _`@tokibito`: https://github.com/tokibito
.. _`@mozillazg`: https://github.com/mozillazg
.. _`@mdklatt`: https://github.com/mdklatt
.. _`@ewjoachim`: https://github.com/ewjoachim
.. _`@href`: https://github.com/href
.. _`@jhermann`: https://github.com/jhermann
.. _`@ratson`: https://github.com/ratson
.. _`@hzdg`: https://github.com/hzdg
.. _`@dulaccc`: :https://github.com/dulaccc
.. _`@peterlauri`: https://github.com/peterlauri
.. _`@SpotlightKid`: https://github.com/SpotlightKid
.. _`@eviweb`: https://github.com/eviweb
.. _`@willingc`: https://github.com/willingc
.. _`@matheuspoleza`: https://github.com/matheuspoleza
.. _`@pjbull`: https://github.com/pjbull
.. _`@nanuxbe`: https://github.com/nanuxbe
.. _`@ruflin`: https://github.com/ruflin
.. _`@tephyr`: https://github.com/tephyr
.. _`@bollwyvl`: https://github.com/bollwyvl
.. _`@purplediane`: https://github.com/purplediane
.. _`@Plippe`: https://github.com/Plippe
.. _`@terryjbates`: https://github.com/terryjbates
.. _`@cedk`: https://github.com/cedk
.. _`@nicoe`: https://github.com/nicoe
.. _`@phoebebauer`: https://github.com/phoebebauer
.. _`@adamchainz`: https://github.com/adamchainz
.. _`@suledev`: https://github.com/suledev
.. _`@palmerev`: https://github.com/palmerev
.. _`@BruceEckel`: https://github.com/BruceEckel
.. _`@dot2dotseurat`: https://github.com/dot2dotseurat
.. _`@ivanlyon`: https://github.com/ivanlyon
.. _`@zzzirk`: https://github.com/zzzirk
.. _`@xguse`: https://github.com/xguse
.. _`@stevepiercy`: https://github.com/stevepiercy
.. _`@shenyushun`: https://github.com/shenyushun
.. _`@brettcannon`: https://github.com/brettcannon
.. _`@mandeepbhutani`: https://github.com/mandeepbhutani
.. _`@mwarkentin`: https://github.com/mwarkentin
.. _`@B3QL`: https://github.com/B3QL
.. _`@laerus`: https://github.com/laerus
.. _`@mkrapp`: https://github.com/mkrapp
.. _`@elenimijalis`: https://github.com/elenimijalis
.. _`@andytom`: https://github.com/andytom
.. _`@lamby`: https://github.com/lamby
.. _`@christianmlong`: https://github.com/christianmlong
.. _`@jcarbaugh`: https://github.com/jcarbaugh
.. _`@cheungnj`: https://github.com/cheungnj
.. _`@aroig`: https://github.com/aroig

.. _`cookiecutter-pyqt5`: https://github.com/mandeepbhutani/cookiecutter-pyqt5
.. _`cookiecutter-funkload-friendly`: https://github.com/tokibito/cookiecutter-funkload-friendly
.. _`cookiecutter-reveal.js`: https://github.com/keimlink/cookiecutter-reveal.js
.. _`cookiecutter-python-app`: https://github.com/mdklatt/cookiecutter-python-app
.. _`morepath-cookiecutter`: https://github.com/morepath/morepath-cookiecutter
.. _`hovercraft-slides`: https://github.com/Springerle/hovercraft-slides
.. _`cookiecutter-es6-package`: https://github.com/ratson/cookiecutter-es6-package
.. _`cookiecutter-webpack`: https://github.com/hzdg/cookiecutter-webpack
.. _`cookiecutter-django-herokuapp`: https://github.com/dulaccc/cookiecutter-django-herokuapp
.. _`cookiecutter-django-aws-eb`: https://github.com/dolphinkiss/cookiecutter-django-aws-eb
.. _`wagtail-starter-kit`: https://github.com/tkjone/wagtail-starter-kit
.. _`cookiecutter-dpf-effect`: https://github.com/SpotlightKid/cookiecutter-dpf-effect
.. _`cookiecutter-dpf-audiotk`: https://github.com/SpotlightKid/cookiecutter-dpf-audiotk
.. _`cookiecutter-template`: https://github.com/eviweb/cookiecutter-template
.. _`cookiecutter-angular2`: https://github.com/matheuspoleza/cookiecutter-angular2
.. _`cookiecutter-data-science`: http://drivendata.github.io/cookiecutter-data-science/
.. _`cc_django_ember_app`: https://bitbucket.org/levit_scs/cc_django_ember_app
.. _`cc_project_app_drf`: https://bitbucket.org/levit_scs/cc_project_app_drf
.. _`cc_project_app_full_with_hooks`: https://bitbucket.org/levit_scs/cc_project_app_full_with_hooks
.. _`beat-generator`: https://github.com/elastic/beat-generator
.. _`cookiecutter-scala`: https://github.com/Plippe/cookiecutter-scala
.. _`cookiecutter-snakemake-analysis-pipeline`: https://github.com/xguse/cookiecutter-snakemake-analysis-pipeline
.. _`cookiecutter-py3tkinter`: https://github.com/ivanlyon/cookiecutter-py3tkinter
.. _`pyramid-cookiecutter-alchemy`: https://github.com/Pylons/pyramid-cookiecutter-alchemy
.. _`pyramid-cookiecutter-starter`: https://github.com/Pylons/pyramid-cookiecutter-starter
.. _`pyramid-cookiecutter-zodb`: https://github.com/Pylons/pyramid-cookiecutter-zodb
.. _`substanced-cookiecutter`: https://github.com/Pylons/substanced-cookiecutter
.. _`cookiecutter-simple-django-cn`: https://github.com/shenyushun/cookiecutter-simple-django-cn
.. _`cookiecutter-xontrib`: https://github.com/laerus/cookiecutter-xontrib
.. _`cookiecutter-reproducible-science`: https://github.com/mkrapp/cookiecutter-reproducible-science
.. _`cc-automated-drf-template`: https://github.com/TAMU-CPT/cc-automated-drf-template


1.4.0 (2016-03-20) Shortbread
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal of this release is changing to a strict Jinja2 environment, paving the
way to more awesome in the future, as well as adding support for Jinja2
extensions.

New Features:

* Added support for Jinja2 extension support, thanks to `@hackebrot`_ (#617).
* Now raises an error if Cookiecutter tries to render a template that contains an undefined variable. Makes generation more robust and secure (#586). Work done by `@hackebrot`_ (#111, #586, #592)
* Uses strict Jinja2 env in prompt, thanks to `@hackebrot`_ (#598, #613)
* Switched from pyyaml/ruamel.yaml libraries that were problematic across platforms to the pure Python poyo_ library, thanks to `@hackebrot`_ (#557, #569, #621)
* User config values for ``cookiecutters_dir`` and ``replay_dir`` now support
  environment variable and user home expansion, thanks to `@nfarrar`_ for the
  suggestion and `@hackebrot`_ for the PR (#640, #642)
* Add `jinja2-time`_ as default extension for dates and times in templates via
  ``{% now 'utc' %}``, thanks to `@hackebrot`_ (#653)

Bug Fixes:

* Provided way to define options that have no defaults, thanks to `@johtso`_ (#587, #588)
* Make sure that ``replay.dump()`` and ``replay.load()`` use the correct user config, thanks to `@hackebrot`_ (#590, #594)
* Added correct CA bundle for Git on Appveyor, thanks to `@maiksensi`_ (#599, #602)
* Open ``HISTORY.rst`` with ``utf-8`` encoding when reading the changelog,
  thanks to `@0-wiz-0`_ for submitting the issue and `@hackebrot`_ for the fix
  (#638, #639)
* Fix repository indicators for `private repository`_ urls, thanks to
  `@habnabit`_ for the fix (#595) and `@hackebrot`_ for the tests (#655)

.. _poyo: https://pypi.python.org/pypi/poyo
.. _`jinja2-time`: https://pypi.python.org/pypi/jinja2-time
.. _`private repository`: http://cookiecutter.readthedocs.io/en/latest/usage.html#works-with-private-repos

Other Changes:

* Set path before running tox, thanks to `@maiksensi`_ (#615, #620)
* Removed xfail in test_cookiecutters, thanks to `@hackebrot`_ (#618)
* Removed django-cms-plugin on account of 404 error, thanks to `@mativs`_ and `@pydanny`_ (#593)
* Fixed docs/usage.rst, thanks to `@macrotim`_ (#604)
* Update .gitignore to latest Python.gitignore and ignore PyCharm files, thanks to `@audreyr`_
* Use open context manager to read context_file in generate() function, thanks to `@hackebrot`_ (#607, #608)
* Added documentation for choice variables, thanks to `@maiksensi`_ (#611)
* Set up Scrutinizer to check code quality, thanks to `@audreyr`_
* Drop distutils support in setup.py, thanks to `@hackebrot`_ (#606, #609)
* Change cookiecutter-pypackage-minimal link, thanks to `@kragniz`_ (#614)
* Fix typo in one of the template's description, thanks to `@ryanfreckleton`_ (#643)
* Fix broken link to `_copy_without_render`_ in *troubleshooting.rst*, thanks
  to `@ptim`_ (#647)

* Added more cookiecutter templates to the mix:

  * `cookiecutter-pipproject`_ by `@wdm0006`_ (#624)
  * `cookiecutter-flask-2`_ by `@wdm0006`_ (#624)
  * `cookiecutter-kotlin-gradle`_ by `@thomaslee`_ (#622)
  * `cookiecutter-tryton-fulfilio`_ by `@cedk`_ (#631)
  * `django-starter`_ by `@tkjone`_ (#635)
  * `django-docker-bootstrap`_ by `@legios89`_ (#636)
  * `cookiecutter-mediawiki-extension`_ by `@JonasGroeger`_ (#645)
  * `cookiecutter-django-gulp`_ by `@valerymelou`_ (#648)


.. _`@macrotim`: https://github.com/macrotim
.. _`@wdm0006`: https://github.com/wdm0006
.. _`@thomaslee`: https://github.com/thomaslee
.. _`@kragniz`: https://github.com/kragniz
.. _`@ryanfreckleton`: https://github.com/ryanfreckleton
.. _`@cedk`: https://github.com/cedk
.. _`@johtso`: https://github.com/johtso
.. _`@legios89`: https://github.com/legios89
.. _`@0-wiz-0`: https://github.com/0-wiz-0
.. _`@tkjone`: https://github.com/tkjone
.. _`@nfarrar`: https://github.com/nfarrar
.. _`@ptim`: https://github.com/ptim
.. _`@JonasGroeger`: https://github.com/JonasGroeger
.. _`@valerymelou`: https://github.com/valerymelou
.. _`@habnabit`: https://github.com/habnabit

.. _`cookiecutter-kotlin-gradle`: https://github.com/thomaslee/cookiecutter-kotlin-gradle
.. _`cookiecutter-pipproject`: https://github.com/wdm0006/cookiecutter-pipproject
.. _`cookiecutter-flask-2`: https://github.com/wdm0006/cookiecutter-flask
.. _`django-starter`: https://github.com/tkjone/django-starter
.. _`django-docker-bootstrap`: https://github.com/legios89/django-docker-bootstrap
.. _`cookiecutter-mediawiki-extension`: https://github.com/JonasGroeger/cookiecutter-mediawiki-extension
.. _`cookiecutter-django-gulp`: https://github.com/valerymelou/cookiecutter-django-gulp
.. _`cookiecutter-tryton-fulfilio`: https://github.com/fulfilio/cookiecutter-tryton

.. _`_copy_without_render`: http://cookiecutter.readthedocs.io/en/latest/advanced_usage.html#copy-without-render

1.3.0 (2015-11-10) Pumpkin Spice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal of this release is to extend the user config feature and to make hook execution more robust.

New Features:

* Abort project generation if ``pre_gen_project`` or ``post_gen_project`` hook scripts fail, thanks to `@eliasdorneles`_ (#464, #549)
* Extend user config capabilities with additional cli options ``--config-file``
  and ``--default-config`` and environment variable ``COOKIECUTTER_CONFIG``, thanks to `@jhermann`_, `@pfmoore`_, and `@hackebrot`_ (#258, #424, #565)

Bug Fixes:

* Fixed conditional dependencies for wheels in setup.py, thanks to `@hackebrot`_ (#557, #568)
* Reverted skipif markers to use correct reasons (bug fixed in pytest), thanks to `@hackebrot`_ (#574)


Other Changes:

* Improved path and documentation for rendering the Sphinx documentation, thanks to `@eliasdorneles`_ and `@hackebrot`_ (#562, #583)
* Added additional help entrypoints, thanks to `@michaeljoseph`_ (#563, #492)
* Added Two Scoops Academy to the README, thanks to `@hackebrot`_ (#576)
* Now handling trailing slash on URL, thanks to `@ramiroluz`_ (#573, #546)
* Support for testing x86 and x86-64 architectures on appveyor, thanks to `@maiksensi`_ (#567)
* Made tests work without installing Cookiecutter, thanks to `@vincentbernat`_ (#550)
* Encoded the result of the hook template to utf8, thanks to `@ionelmc`_ (#577. #578)
* Added test for _run_hook_from_repo_dir, thanks to `@hackebrot`_ (#579, #580)
* Implemented bumpversion, thanks to `@hackebrot`_ (#582)
* Added more cookiecutter templates to the mix:

  * `cookiecutter-octoprint-plugin`_ by `@foosel`_ (#560)
  * `wagtail-cookiecutter-foundation`_ by `@chrisdev`_, et al. (#566)

.. _`@foosel`: https://github.com/foosel
.. _`@chrisdev`: https://github.com/chrisdev
.. _`@jhermann`: https://github.com/jhermann

.. _`cookiecutter-octoprint-plugin`: https://github.com/OctoPrint/cookiecutter-octoprint-plugin
.. _`wagtail-cookiecutter-foundation`: https://github.com/chrisdev/wagtail-cookiecutter-foundation


1.2.1 (2015-10-18) Zimtsterne
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Zimtsterne are cinnamon star cookies*

New Feature:

* Returns rendered project dir, thanks to `@hackebrot`_ (#553)

Bug Fixes:

* Factor in *choice* variables (as introduced in 1.1.0) when using a user config or extra context, thanks to `@ionelmc`_ and `@hackebrot`_ (#536, #542).

Other Changes:

* Enable py35 support on Travis by using Python 3.5 as base Python (`@maiksensi`_ / #540)
* If a filename is empty, do not generate. Log instead (`@iljabauer`_ / #444)
* Fix tests as per last changes in `cookiecutter-pypackage`_, thanks to `@eliasdorneles`_ (#555).
* Removed deprecated cookiecutter-pylibrary-minimal from the list, thanks to `@ionelmc`_ (#556)
* Moved to using `rualmel.yaml` instead of `PyYAML`, except for Windows users on Python 2.7, thanks to `@pydanny`_ (#557)

.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`@iljabauer`: https://github.com/iljabauer
.. _`@eliasdorneles`: https://github.com/eliasdorneles

*Why 1.2.1 instead of 1.2.0? There was a problem in the distribution that we pushed to PyPI. Since you can't replace previous files uploaded to PyPI, we deleted the files on PyPI and released 1.2.1.*


1.1.0 (2015-09-26) Snickerdoodle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goals of this release were `copy without render` and a few additional command-line options such as `--overwrite-if-exists`, `—replay`, and `output-dir`.

Features:

* Added `copy without render`_ feature, making it much easier for developers of Ansible, Salt Stack, and other recipe-based tools to work with Cookiecutter. Thanks to `@osantana`_ and `@LucianU`_ for their innovation, as well as `@hackebrot`_ for fixing the Windows problems (#132, #184, #425).
* Added `specify output directory`, thanks to `@tony`_ and `@hackebrot`_ (#531, #452).
* Abort template rendering if the project output directory already exists, thanks to `@lgp171188`_ (#470, #471).
* Add a flag to overwrite existing output directory, thanks to `@lgp171188`_ for the implementation (#495) and `@schacki`_, `@ionelmc`_, `@pydanny`_ and `@hackebrot`_ for submitting issues and code reviews (#475, #493).
* Remove test command in favor of tox, thanks to `@hackebrot`_ (#480).
* Allow cookiecutter invocation, even without installing it, via ``python -m cookiecutter.cli``, thanks to  `@vincentbernat`_ and `@hackebrot`_ (#449, #487).
* Improve the type detection handler for online and offline repositories, thanks to `@charlax`_ (#490).
* Add replay feature, thanks to `@hackebrot`_ (#501).
* Be more precise when raising an error for an invalid user config file, thanks to `@vaab`_ and `@hackebrot`_ (#378, #528).
* Added official Python 3.5 support, thanks to `@pydanny`_ and `@hackebrot`_ (#522).
* Added support for *choice* variables and switch to click style prompts, thanks to `@hackebrot`_ (#441, #455).

Other Changes:

* Updated click requirement to < 6.0, thanks to `@pydanny`_ (#473).
* Added landscape.io flair, thanks to `@michaeljoseph`_ (#439).
* Descriptions of PEP8 specifications and milestone management, thanks to `@michaeljoseph`_ (#440).
  * Added alternate installation options in the documentation, thanks to `@pydanny`_  (#117, #315).
* The test of the `which()` function now tests against the `date` command, thanks to `@vincentbernat`_ (#446)
* Ensure file handles in setup.py are closed using with statement, thanks to `@svisser`_ (#280).
* Removed deprecated and fully extraneous `compat.is_exe()` function, thanks to `@hackebrot`_ (#485).
* Disabled sudo in .travis, thanks to `@hackebrot`_ (#482).
* Switched to shields.io for problematic badges, thanks to `@pydanny`_ (#491).
* Added whichcraft and removed ``compat.which()``, thanks to `@pydanny`_ (#511).
* Changed to export tox environment variables to codecov, thanks to `@maiksensi`_. (#508).
* Moved to using click version command, thanks to `@hackebrot`_ (#489).
* Don't use unicode_literals to please click, thanks to `@vincentbernat`_ (#503).
* Remove warning for Python 2.6 from __init__.py, thanks to `@hackebrot`_.
* Removed `compat.py` module, thanks to `@hackebrot`_.
* Added `future` to requirements, thanks to `@hackebrot`_.
* Fixed problem where expanduser does not resolve "~" correctly on windows 10 using tox, thanks to `@maiksensi`_. (#527)
* Added more cookiecutter templates to the mix:

  * `cookiecutter-beamer`_ by `@luismartingil`_ (#307)
  * `cookiecutter-pytest-plugin`_ by `@pytest-dev`_ and `@hackebrot`_ (#481)
  * `cookiecutter-csharp-objc-binding`_ by `@SandyChapman`_ (#460)
  * `cookiecutter-flask-foundation`_ by `@JackStouffer`_ (#457)
  * `cookiecutter-tryton-fulfilio`_ by `@fulfilio`_ (#465)
  * `cookiecutter-tapioca`_ by `@vintasoftware`_ (#496)
  * `cookiecutter-sublime-text-3-plugin`_ by `@kkujawinski`_ (#500)
  * `cookiecutter-muffin`_ by `@drgarcia1986`_ (#494)
  * `cookiecutter-django-rest`_ by `@agconti`_ (#520)
  * `cookiecutter-es6-boilerplate`_ by `@agconti`_ (#521)
  * `cookiecutter-tampermonkey`_ by `@christabor`_ (#516)
  * `cookiecutter-wagtail`_ by `@torchbox`_ (#533)

.. _`@maiksensi`: https://github.com/maiksensi
.. _`copy without render`: http://cookiecutter.readthedocs.io/en/latest/advanced_usage.html#copy-without-render
.. _`@osantana`: https://github.com/osantana
.. _`@LucianU`: https://github.com/LucianU
.. _`@svisser`: https://github.com/svisser
.. _`@lgp171188`: https://github.com/lgp171188
.. _`@SandyChapman`: https://github.com/SandyChapman
.. _`@JackStouffer`: https://github.com/JackStouffer
.. _`@fulfilio`: https://github.com/fulfilio
.. _`@vintasoftware`: https://github.com/vintasoftware
.. _`@kkujawinski`: https://github.com/kkujawinski
.. _`@charlax`: https://github.com/charlax
.. _`@drgarcia1986`: https://github.com/drgarcia1986
.. _`@agconti`: https://github.com/agconti
.. _`@vaab`: https://github.com/vaab
.. _`@christabor`: https://github.com/christabor
.. _`@torchbox`: https://github.com/torchbox
.. _`@tony`: https://github.com/tony

.. _`cookiecutter-beamer`: https://github.com/luismartingil/cookiecutter-beamer
.. _`@luismartingil`: https://github.com/luismartingil
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`@pytest-dev`: https://github.com/pytest-dev
.. _`cookiecutter-csharp-objc-binding`: https://github.com/SandyChapman/cookiecutter-csharp-objc-binding
.. _`cookiecutter-flask-foundation`: https://github.com/JackStouffer/cookiecutter-Flask-Foundation
.. _`cookiecutter-tryton-fulfilio`: https://github.com/fulfilio/cookiecutter-tryton
.. _`cookiecutter-tapioca`: https://github.com/vintasoftware/cookiecutter-tapioca
.. _`cookiecutter-sublime-text-3-plugin`: https://github.com/kkujawinski/cookiecutter-sublime-text-3-plugin
.. _`cookiecutter-muffin`: https://github.com/drgarcia1986/cookiecutter-muffin
.. _`cookiecutter-django-rest`: https://github.com/agconti/cookiecutter-django-rest
.. _`cookiecutter-es6-boilerplate`: https://github.com/agconti/cookiecutter-es6-boilerplate
.. _`cookiecutter-tampermonkey`: https://github.com/christabor/cookiecutter-tampermonkey
.. _`cookiecutter-wagtail`: https://github.com/torchbox/cookiecutter-wagtail

1.0.0 (2015-03-13) Chocolate Chip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goals of this release was to formally remove support for Python 2.6 and continue the move to using py.test.

Features:

* Convert the unittest suite to py.test for the sake of comprehensibility, thanks to `@hackebrot`_ (#322, #332, #334, #336, #337, #338, #340, #341, #343, #345, #347, #351, #412, #413, #414).
* Generate pytest coverage, thanks to `@michaeljoseph`_ (#326).
* Documenting of Pull Request merging and HISTORY.rst maintenance, thanks to `@michaeljoseph`_ (#330).
* Large expansions to the tutorials thanks to `@hackebrot`_ (#384)
* Switch to using Click for command-line options, thanks to `@michaeljoseph`_ (#391, #393).
* Added support for working with private repos, thanks to `@marctc`_ (#265).
* Wheel configuration thanks to `@michaeljoseph`_ (#118).

Other Changes:

* Formally removed support for 2.6, thanks to `@pydanny`_ (#201).
* Moved to codecov for continuous integration test coverage and badges, thanks to `@michaeljoseph`_ (#71, #369).
* Made JSON parsing errors easier to debug, thanks to `@rsyring`_ and `@mark0978`_ (#355, #358, #388).
* Updated to Jinja 2.7 or higher in order to control trailing new lines in templates, thanks to `@sfermigier`_ (#356).
* Tweaked flake8 to ignore e731, thanks to `@michaeljoseph`_ (#390).
* Fixed failing Windows tests and corrected AppVeyor badge link thanks to `@msabramo`_ (#403).
* Added more Cookiecutters to the list:

  * `cookiecutter-scala-spark`_ by `@jpzk`_
  * `cookiecutter-atari2600`_ by `@joeyjoejoejr`_
  * `cookiecutter-bottle`_ by `@avelino`_
  * `cookiecutter-latex-article`_ by `@Kreger51`_
  * `cookiecutter-django-rest-framework`_ by `@jpadilla`_
  * `cookiedozer`_ by `@hackebrot`_

.. _`@msabramo`: https://github.com/msabramo
.. _`@marctc`: https://github.com/marctc
.. _`cookiedozer`: https://github.com/hackebrot/cookiedozer
.. _`@jpadilla`: https://github.com/jpadilla
.. _`cookiecutter-django-rest-framework`: https://github.com/jpadilla/cookiecutter-django-rest-framework
.. _`cookiecutter-latex-article`: https://github.com/Kreger51/cookiecutter-latex-article
.. _`@Kreger51`: https://github.com/Kreger51
.. _`@rsyring`: https://github.com/rsyring
.. _`@mark0978`: https://github.com/mark0978
.. _`cookiecutter-bottle`: https://github.com/avelino/cookiecutter-bottle
.. _`@avelino`: https://github.com/avelino
.. _`@joeyjoejoejr`: https://github.com/joeyjoejoejr
.. _`cookiecutter-atari2600`: https://github.com/joeyjoejoejr/cookiecutter-atari2600
.. _`@sfermigier`: https://github.com/sfermigier
.. _`cookiecutter-scala-spark`: https://github.com/jpzk/cookiecutter-scala-spark
.. _`@jpzk`: https://github.com/jpzk

0.9.0 (2015-01-13)
~~~~~~~~~~~~~~~~~~~

The goals of this release were to add the ability to Jinja2ify the `cookiecutter.json` default values, and formally launch support for Python 3.4.

Features:

* Python 3.4 is now a first class citizen, thanks to everyone.
* `cookiecutter.json` values are now rendered Jinja2 templates, thanks to @bollwyvl (#291).
* Move to `py.test`, thanks to `@pfmoore`_ (#319) and `@ramiroluz`_ (#310).
* Add `PendingDeprecation` warning for users of Python 2.6, as support for it is gone in Python 2.7, thanks to `@michaeljoseph`_ (#201).

Bug Fixes:

* Corrected typo in `Makefile`, thanks to `@inglesp`_ (#297).
* Raise an exception when users don't have `git` or `hg` installed, thanks to `@pydanny`_ (#303).

Other changes:

* Creation of `gitter`_ account for logged chat, thanks to `@michaeljoseph`_.
* Added ReadTheDocs badge, thanks to `@michaeljoseph`_.
* Added AppVeyor badge, thanks to `@pydanny`_
* Documentation and PyPI trove classifier updates, thanks to `@thedrow`_ (#323 and #324)

.. _`gitter`: https://gitter.im/audreyr/cookiecutter
.. _`@inglesp`: https://github.com/inglesp
.. _`@ramiroluz`: https://github.com/ramiroluz
.. _`@thedrow`: https://github.com/thedrow
.. _`@hackebrot`: https://github.com/hackebrot

0.8.0 (2014-10-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal of this release was to allow for injection of extra context via the
Cookiecutter API, and to fix minor bugs.

Features:

* `cookiecutter()` now takes an optional `extra_context` parameter, thanks to `@michaeljoseph`_, `@fcurella`_, `@aventurella`_, `@emonty`_, `@schacki`_, `@ryanolson`_, `@pfmoore`_, `@pydanny`_, `@audreyr`_ (#260).
* Context is now injected into hooks, thanks to `@michaeljoseph`_ and `@dinopetrone`_.
* Moved all Python 2/3 compatability code into `cookiecutter.compat`, making the eventual move to `six` easier, thanks to `@michaeljoseph`_ (#60, #102).
* Added `cookiecutterrc` defined aliases for cookiecutters, thanks to `@pfmoore`_ (#246)
* Added `flake8` to tox to check for pep8 violations, thanks to `@natim`_.

Bug Fixes:

* Newlines at the end of files are no longer stripped, thanks to `@treyhunner`_ (#183).
* Cloning prompt suppressed by respecting the `no_input` flag, thanks to `@trustrachel`_ (#285)
* With Python 3, input is no longer converted to bytes, thanks to `@uranusjr`_ (#98).

Other Changes:

* Added more Cookiecutters to the list:

  * `Python-iOS-template`_ by `@freakboy3742`_
  * `Python-Android-template`_ by `@freakboy3742`_
  * `cookiecutter-djangocms-plugin`_ by `@mishbahr`_
  * `cookiecutter-pyvanguard`_ by `@robinandeer`_

.. _`Python-iOS-template`: https://github.com/pybee/Python-iOS-template
.. _`Python-Android-template`: https://github.com/pybee/Python-Android-template
.. _`cookiecutter-djangocms-plugin`: https://github.com/mishbahr/cookiecutter-djangocms-plugin
.. _`cookiecutter-pyvanguard`: https://github.com/robinandeer/cookiecutter-pyvanguard

.. _`@trustrachel`: https://github.com/trustrachel
.. _`@robinandeer`: https://github.com/robinandeer
.. _`@mishbahr`: https://github.com/mishbahr
.. _`@freakboy3742`: https://github.com/freakboy3742
.. _`@treyhunner`: https://github.com/treyhunner
.. _`@pfmoore`: https://github.com/pfmoore
.. _`@fcurella`: https://github.com/fcurella
.. _`@aventurella`: https://github.com/aventurella
.. _`@emonty`: https://github.com/emonty
.. _`@schacki`: https://github.com/schacki
.. _`@ryanolson`: https://github.com/ryanolson
.. _`@Natim`: https://github.com/Natim
.. _`@dinopetrone`: https://github.com/dinopetrone

0.7.2 (2014-08-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal of this release was to fix cross-platform compatibility, primarily
Windows bugs that had crept in during the addition of new features. As of this
release, Windows is a first-class citizen again, now complete with continuous
integration.

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
.. _`cookiecutter-pypackage-minimal`: https://github.com/kragniz/cookiecutter-pypackage-minimal
.. _`cookiecutter-pylibrary`: https://github.com/ionelmc/cookiecutter-pylibrary
.. _`cookiecutter-pylibrary-minimal`: https://github.com/ionelmc/cookiecutter-pylibrary-minimal

.. _`@Paspartout`: https://github.com/Paspartout
.. _`@audreyr`: https://github.com/audreyr
.. _`@borntyping`: https://github.com/borntyping
.. _`@hackebrot`: https://github.com/hackebrot
.. _`@iknite`: https://github.com/iknite
.. _`@ionelmc`: https://github.com/ionelmc
.. _`@michaeljoseph`: https://github.com/michaeljoseph
.. _`@pfmoore`: https://github.com/pfmoore
.. _`@pydanny`: https://github.com/pydanny
.. _`@saxix`: https://github.com/saxix
.. _`@uranusjr`: https://github.com/uranusjr
.. _`@mativs`: https://github.com/mativs



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

https://github.com/audreyr/cookiecutter/milestones?direction=desc&sort=due_date&state=open
