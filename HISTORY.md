# History

History is important, but our current roadmap can be found [here](https://github.com/cookiecutter/cookiecutter/projects)

## 2.6.0 (2024-02-21)

### Minor Changes

* Support Python 3.12 (#1989) @ericof
* Modifying Jinja2 start and end variable strings (#1997) @sacha-c

### CI/CD and QA changes

* Add isort as a pre-commit hook (#1988) @kurtmckee
* Bump actions/setup-python from 4 to 5 (#2000) @dependabot
* Bump actions/upload-artifact from 3 to 4 (#1999) @dependabot
* Quick resolution of #2003 (#2004) @jensens
* Support Python 3.12 (#1989) @ericof
* [pre-commit.ci] pre-commit autoupdate (#1996) @pre-commit-ci
* Quick resolution of #2003 (#2004) @jensens

### Documentation updates

* Support Python 3.12 (#1989) @ericof

### Bugfixes

* Fix regression #2009: Adding value to nested dicts broken (#2010) @jensens
* Fixed errors caused by invalid config files. (#1995) @alanverresen

### This release is made by wonderful contributors:

@alanverresen, @dependabot, @dependabot[bot], @ericof, @jensens, @kurtmckee, @pre-commit-ci, @pre-commit-ci[bot] and @sacha-c


## 2.5.0 (2023-11-21)

### Minor Changes

* Default values can be passed as a dict (#1924) @matveyvarg
* Implement new style for nested templates config (#1981) @ericof

### CI/CD and QA changes

* Bump actions/checkout from 3 to 4 (#1953) @dependabot
* [pre-commit.ci] pre-commit autoupdate (#1977) @pre-commit-ci
* [pre-commit.ci] pre-commit autoupdate (#1957) @pre-commit-ci

### Documentation updates

* Add argument run to pipx command in README.md (#1964) @staeff
* Fix tutorial2 generated HTML (#1971) @aantoin
* Update README.md (#1967) @HarshRanaOC
* Update README.md to fix broken link (#1952) @david-abn
* Update README.md to include installation instructions (#1949) @david-abn
* Update cookiecutter-plone-starter link in readme (#1965) @zahidkizmaz

### Bugfixes

* Fix FileExistsError when using a relative template path (#1968) @pkrueger-cariad
* Fix recursive context overwrites (#1961) @padraic-padraic

### This release is made by wonderful contributors:

@HarshRanaOC, @aantoin, @david-abn, @dependabot, @dependabot[bot], @ericof, @matveyvarg, @padraic-padraic, @pkrueger-cariad, @pre-commit-ci, @pre-commit-ci[bot], @staeff and @zahidkizmaz


## 2.4.0 (2023-09-29)

### Minor Changes

* Gracefully handle files with mixed lined endings (#1942) @EricHripko
* Implement a pre_prompt hook that will run before prompts (#1950) @ericof

### Documentation updates

* Implement a pre_prompt hook that will run before prompts (#1950) @ericof
* update main docstrings to include overwrite_if_exists and skip_if_file_exists (#1947) @david-abn

### This release is made by wonderful contributors:

@EricHripko, @david-abn and @ericof

## 2.3.1 (2023-09-21)

### Minor Changes

* add checkout details to the context (fixes #1759) (#1923) @JonZeolla

### CI/CD and QA changes

* Update the black pre-commit hook URL and version (#1934) @kurtmckee
* Use UTF-8 for file reading/writing (#1937) @rmartin16

### Documentation updates

* Add missing "parent dir" symbol in tutorial 2 (#1932) @tvoirand
* Remove colons from exemplary prompt messages (#1912) @paduszyk
* docs: add install instruction for Void Linux (#1917) @tranzystorek-io

### Bugfixes

* Fix nested templates in Git repository (#1922) @BTatlock
* Fix prompt counter. (#1940) @ericof
* Fix variables with null default not being required (#1919) (#1920) @limtis0

### This release is made by wonderful contributors:

@BTatlock, @JonZeolla, @ericof, @kurtmckee, @limtis0, @paduszyk, @rmartin16, @tranzystorek-io and @tvoirand

## 2.3.0 (2023-08-03)

### Minor Changes

* Improve style of prompts using `rich` (#1901) @vemonet

### CI/CD and QA changes

* Bump paambaati/codeclimate-action from 4.0.0 to 5.0.0 (#1908) @dependabot
* [pre-commit.ci] pre-commit autoupdate (#1907) @pre-commit-ci

### Bugfixes

* Fix replay (#1904) @vemonet
* Support multichoice overwrite (#1903) @Meepit

### This release is made by wonderful contributors:

@Meepit, @dependabot, @dependabot[bot], @ericof, @pre-commit-ci, @pre-commit-ci[bot] and @vemonet

## 2.2.3 (2023-07-11)
### Changes

### Minor Changes

* Add support for adding human-readable labels for choices when defining multiple choices questions (#1898) @vemonet

* Prompt with replay file (#1758) @w1ndblow

### CI/CD and QA changes

* Set cookiecutter/VERSION.txt as source of truth for version number (#1896) @ericof
* [pre-commit.ci] pre-commit autoupdate (#1897) @pre-commit-ci

### Bugfixes

* Fix issue where the prompts dict was not passed for yes_no questions (#1895) @vemonet
* Set cookiecutter/VERSION.txt as source of truth for version number (#1896) @ericof

### This release is made by wonderful contributors:

@ericof, @pre-commit-ci, @pre-commit-ci[bot], @vemonet and @w1ndblow

## 2.2.2 (2023-07-10)

### CI/CD and QA changes

* Improve gitignore (#1889) @audreyfeldroy
* Add warning for jinja2_time (#1890) @henryiii

### This release is made by wonderful contributors:

@audreyfeldroy, @ericof and @henryiii


## 2.2.0 (2023-07-06)

### Changes

* Added timeout on request.get() for ensuring that if a recipient serve… (#1772) @openrefactory
* Fixing Carriage Return Line Feed (CRLF) order in docs #1792 (#1793) @Lahiry
* Reduce I/O (#1877) @kurtmckee
* Remove a pre-commit hook special case (#1875) @kurtmckee
* Remove universal bdist_wheel option; use "python -m build" (#1739) @mwtoews
* Remove unused import from post-generate hook script example (#1795) @KAZYPinkSaurus
* Standardize newlines for all platforms (#1870) @kurtmckee
* feat: Add resolved template repository path as _repo_dir to the context (#1771) @tmeckel

### Minor Changes

* Added support for providing human-readable prompts to the different variables (#1881) @vemonet
* Added: Boolean variable support in JSON (#1626) @liortct
* Added: CLI option to keep project files on failure. (#1669) @MaciejPatro
* Added: Support partially overwrite keys in nested dict (#1692) @cksac
* Added: Templates inheritance (#1485) @simobasso
* Code quality: Tests upgrade: Use pathlib for files read/write (#1718) @insspb
* Inline jinja2-time extension code (#1779) @tranzystorek-io
* Support Python 3.11 (#1850) @kurtmckee
* Support nested config files (#1770) @dariocurr
* preserves original options in `_cookiecutter` (#1874) @kjaymiller

### CI/CD and QA changes

* Add a Dependabot config to autoupdate GitHub workflow actions (#1851) @kurtmckee
* Added: Readthedocs build config (#1707) @insspb
* Bump actions/setup-python from 3 to 4 (#1854) @dependabot
* Bump paambaati/codeclimate-action from 3.0.0 to 4.0.0 (#1853) @dependabot
* CI/CD: Tox -> Nox: Added nox configuration (#1706) @insspb
* CI/CD: Tox -> Nox: Github actions definition minimized + Sync nox and github actions (#1714) @insspb
* CI/CD: Tox -> Nox: Makefile update: Removed watchmedo and sed dependency, tox replaced with nox (#1713) @insspb
* CI/CD: Updated .pre-commit-config.yaml to use latest hooks versions (#1712) @insspb
* Code quality: Core files: Added exception reason reraise when exception class changed (PEP 3134) (#1719) @insspb
* Code quality: Tests upgrade: Use pathlib for files read/write (#1718) @insspb
* Code quality: core files: Format replaced with f-strings (#1716) @insspb
* Code quality: find.py refactored and type annotated (#1721) @insspb
* Code quality: tests files: Simplify statements fixes (#1717) @insspb
* Code quality: utils.make_sure_path_exists refactored and type annotated (#1722) @insspb
* Fixed: recommonmark replaced with myst, as recommonmark is deprecated (#1709) @insspb
* Pretty-format JSON files (#1864) @kurtmckee
* Rename `master` to `main` so CI runs correctly on merge (#1852) @kurtmckee
* Standardize EOF newlines (#1876) @kurtmckee
* Update `.gitignore` and cite where it was copied from (#1879) @kurtmckee
* Update base docs, remove tox (#1858) @ericof
* Update pre-commit hook versions (#1849) @kurtmckee
* Updated: Release drafter configuration (#1704) @insspb
* Use tox (#1866) @kurtmckee
* Verify an expected warning is raised (#1869) @kurtmckee
* fixed failing lint ci action by updating repo of flake8 (#1838) @Tamronimus

### Documentation updates

* Add jinja env docs (#1872) @pamelafox
* Documentation extension: Create a Cookiecutter From Scratch tutorial (#1592) @miro-jelaska
* Easy PR! Fix typos and add minor doc updates (#1741) @Alex0Blackwell
* Expand cli documentation relating to the no-input flag (#1543) (#1587) @jeremyswerdlow
* Fix @audreyr to @audreyfeldroy github account rename (#1604) @ri0t
* Fixed broken links to jinja docs (#1691) @insspb
* Fixed minor typos in docs (#1753) @segunb
* Fixed: Python code block in the replay documentation (#1715) @juhannc
* Fixed: recommonmark replaced with myst, as recommonmark is deprecated (#1709) @insspb
* Improve Docs Readability (#1690) @ryanrussell
* Update base docs, remove tox (#1858) @ericof
* Updated: Boolean Variables documentation and docstrings (#1705) @italomaia
* docs: fix simple typo, shat -> that (#1749) @timgates42
* fixing badge display problem (#1798) @Paulokim1

### Bugfixes

* Fixed the override not working with copy only dir #1650 (#1651) @zhongdai
* Fixed: Removed mention of packages versions, to exclude dependabot warnings alerts (#1711) @insspb
* cleanup files if panics during hooks - bugfix (#1760) @liortct

### This release is made by wonderful contributors:

@Alex0Blackwell, @KAZYPinkSaurus, @Lahiry, @MaciejPatro, @Paulokim1, @Tamronimus, @cksac, @cookies-xor-cream, @dariocurr, @dependabot, @dependabot[bot], @ericof, @insspb, @italomaia, @jeremyswerdlow, @juhannc, @kjaymiller, @kurtmckee, @liortct, @miro-jelaska, @mwtoews, @openrefactory, @pamelafox, @ri0t, @ryanrussell, @segunb, @simobasso, @timgates42, @tmeckel, @tranzystorek-io, @vemonet and @zhongdai


## 2.1.1 (2022-06-01)

### Documentation updates

* Fix local extensions documentation (#1686) @alkatar21

### Bugfixes

* Sanitize Mercurial branch information before checkout. (#1689) @ericof

### This release is made by wonderfull contributors:

@alkatar21, @ericof and @jensens


## 2.1.0 (2022-05-30)

### Changes

* Move contributors and backers to credits section (#1599) @doobrie
* test_generate_file_verbose_template_syntax_error fixed (#1671) @MaciejPatro
* Removed changes related to setuptools_scm (#1629) @ozer550
* Feature/local extensions (#1240) @mwesterhof

### CI/CD and QA changes

* Check manifest: pre-commit, fixes, cleaning (#1683) @jensens
* Follow PyPA guide to release package using GitHub Actions. (#1682) @ericof

### Documentation updates

* Fix typo in dict_variables.rst (#1680) @ericof
* Documentation overhaul (#1677) @jensens
* Fixed incorrect link on docs. (#1649) @luzfcb

### Bugfixes

* Restore accidentally deleted support for click 8.x (#1643) @jaklan

### This release was made possible by our wonderful contributors:

@doobrie, @jensens, @ericof, @luzfcb

## 2.0.2 (2021-12-27)

*Remark: This release never made it to official PyPI*

* Fix Python version number in cookiecutter --version and test on Python 3.10 (#1621) @ozer550
* Removed changes related to setuptools_scm (#1629) @audreyfeldroy @ozer550

## 2.0.1 (2021-12-11)

*Remark: This release never made it to official PyPI*

### Breaking Changes

* Release preparation for 2.0.1rc1 (#1608) @audreyfeldroy
* Replace poyo with pyyaml. (#1489) @dHannasch
* Added: Path templates will be rendered when copy_without_render used (#839) @noirbizarre
* Added: End of line detection and configuration. (#1407) @insspb
* Remove support for python2.7 (#1386) @ssbarnea

### Minor Changes

* Adopt setuptools-scm packaging (#1577) @ssbarnea
* Log the error message when git clone fails, not just the return code (#1505) @logworthy
* allow jinja 3.0.0 (#1548) @wouterdb
* Added uuid extension to be able to generate uuids (#1493) @jonaswre
* Alert user if choice is invalid (#1496) @dHannasch
* Replace poyo with pyyaml. (#1489) @dHannasch
* update AUTHOR lead (#1532) @HosamAlmoghraby
* Add Python 3.9 (#1478) @gliptak
* Added: --list-installed cli option, listing already downloaded cookiecutter packages (#1096) @chrisbrake
* Added: Jinja2 Environment extension on files generation stage (#1419) @insspb
* Added: --replay-file cli option, for replay file distributing (#906) @Cadair
* Added: _output_dir to cookiecutter context (#1034) @Casyfill
* Added: CLI option to ignore hooks (#992) @rgreinho
* Changed: Generated projects can use multiple type hooks at same time. (sh + py) (#974) @milonimrod
* Added: Path templates will be rendered when copy_without_render used (#839) @noirbizarre
* Added: End of line detection and configuration. (#1407) @insspb
* Making code python 3 only: Remove python2 u' sign, fix some strings (#1402) @insspb
* py3: remove futures, six and encoding (#1401) @insspb
* Render variables starting with an underscore. (#1339) @smoothml
* Tests refactoring: test_utils write issues fixed #1405 (#1406) @insspb

### CI/CD and QA changes

* enable branch coverage (#1542) @simobasso
* Make release-drafter diff only between master releases (#1568) @SharpEdgeMarshall
* ensure filesystem isolation during tests execution (#1564) @simobasso
* add safety ci step (#1560) @simobasso
* pre-commit: add bandit hook (#1559) @simobasso
* Replace tmpdir in favour of tmp_path (#1545) @SharpEdgeMarshall
* Fix linting in CI (#1546) @SharpEdgeMarshall
* Coverage 100% (#1526) @SharpEdgeMarshall
* Run coverage with matrix (#1521) @SharpEdgeMarshall
* Lint rst files (#1443) @ssbarnea
* Python3: Changed io.open to build-in open (PEP3116) (#1408) @insspb
* Making code python 3 only: Remove python2 u' sign, fix some strings (#1402) @insspb
* py3: remove futures, six and encoding (#1401) @insspb
* Removed: Bumpversion, setup.py arguments. (#1404) @insspb
* Tests refactoring: test_utils write issues fixed #1405 (#1406) @insspb
* Added: Automatic PyPI deploy on tag creation (#1400) @insspb
* Changed: Restored coverage reporter (#1399) @insspb

### Documentation updates

* Fix pull requests checklist reference (#1537) @glumia
* Fix author name (#1544) @HosamAlmoghraby
* Add missing contributors (#1535) @glumia
* Update CONTRIBUTING.md (#1529) @glumia
* Update LICENSE (#1519) @simobasso
* docs: rewrite the conditional files / directories example description. (#1437) @lyz-code
* Fix incorrect years in release history (#1473) @graue70
* Add slugify in the default extensions list (#1470) @oncleben31
* Renamed cookiecutter.package to API (#1442) @grrlic
* Fixed wording detail (#1427) @steltenpower
* Changed: CLI Commands documentation engine (#1418) @insspb
* Added: Example for conditional files / directories in hooks (#1397) @xyb
* Changed: README.md PyPI URLs changed to the modern PyPI last version (#1391) @brettcannon
* Fixed: Comma in README.md (#1390) @Cy-dev-tex
* Fixed: Replaced no longer maintained pipsi by pipx (#1395) @ndclt

### Bugfixes

* Add support for click 8.x (#1569) @cjolowicz
* Force click<8.0.0 (#1562) @SharpEdgeMarshall
* Remove direct dependency on markupsafe (#1549) @ssbarnea
* fixes prompting private rendered dicts (#1504) @juhuebner
* User's JSON parse error causes ugly Python exception #809 (#1468) @noone234
* config: set default on missing default_context key (#1516) @simobasso
* Fixed: Values encoding on Windows (#1414) @agateau
* Fixed: Fail with gitolite repositories (#1144) @javiersanp
* MANIFEST: Fix file name extensions (#1387) @sebix

### Deprecations

* Removed: Bumpversion, setup.py arguments. (#1404) @insspb
* Removed support for Python 3.6 and PyPy (#1608) @audreyfeldroy

### This release was made possible by our wonderful contributors:

@Cadair, @Casyfill, @Cy-dev-tex, @HosamAlmoghraby, @SharpEdgeMarshall, @agateau, @audreyfeldroy, @brettcannon, @chrisbrake, @cjolowicz, @dHannasch, @gliptak, @glumia, @graue70, @grrlic, @insspb, @javiersanp, @jonaswre, @jsoref, @Jthevos, @juhuebner, @logworthy, @lyz-code, @milonimrod, @ndclt, @noirbizarre, @noone234, @oncleben31, @ozer550, @rgreinho, @sebix, @Sahil-101, @simobasso, @smoothml, @ssbarnea, @steltenpower, @wouterdb, @xyb, Christopher Wolfe and Hosam Almoghraby ( RIAG Digital )

## 1.7.2 (2020-04-21)

* Fixed: Jinja2&Six version limits causing build errors with ansible project [@insspb](https://github.com/insspb) (#1385)

## 1.7.1 (2020-04-21)

This release was focused on internal code and CI/CD changes. During this release
all code was verified to match pep8, pep257 and other code-styling guides.
Project CI/CD was significantly changed, Windows platform checks based on Appveyor
engine was replaced by GitHub actions tests. Appveyor was removed. Also our
CI/CD was extended with Mac builds, to verify project builds on Apple devices.

Important Changes:

* Added: Added debug messages for get_user_config [@ssbarnea](https://github.com/ssbarnea) (#1357)
* Multiple templates per one repository feature added. [@RomHartmann](https://github.com/RomHartmann) (#1224, #1063)
* Update replay.py json.dump indent for easy viewing [@nicain](https://github.com/nicain) (#1293)
* 'future' library replaced with 'six' as a more lightweight python porting library [@asottile](https://github.com/asottile) (#941)
* Added extension: Slugify template filter [@ppanero](https://github.com/ppanero) (#1336)
* Added command line option: `--skip-if-file-exists`, allow to skip the existing files when doing `overwrite_if_exists`. [@chhsiao1981](https://github.com/chhsiao1981) (#1076)
* Some packages versions limited to be compatible with python2.7 and python 3.5 [@insspb](https://github.com/insspb) (#1349)

Internal CI/CD and tests changes:

* Coverage comment in future merge requests disabled [@ssbarnea](https://github.com/ssbarnea) (#1279)
* Fixed Python 3.8 travis tests and setup.py message [@insspb](https://github.com/insspb) (#1295, #1297)
* Travis builds extended with Windows setup for all supported python versions [@insspb](https://github.com/insspb) (#1300, #1301)
* Update .travis.yml to be compatible with latest travis cfg specs [@luzfcb](https://github.com/luzfcb) (#1346)
* Added new test to improve tests coverage [@amey589](https://github.com/amey589) (#1023)
* Added missed coverage lines highlight to pytest-coverage report [@insspb](https://github.com/insspb) (#1352)
* pytest-catchlog package removed from test_requirements, as now it is included in pytest [@insspb](https://github.com/insspb) (#1347)
* Fixed `cov-report` tox invocation environment [@insspb](https://github.com/insspb) (#1350)
* Added: Release drafter support and configuration to exclude changelog update work and focus on development [@ssbarnea](https://github.com/ssbarnea) [@insspb](https://github.com/insspb) (#1356, #1362)
* Added: CI/CD steps for Github actions to speedup CI/CD [@insspb](https://github.com/insspb) (#1360)
* Removed: Appveyor CI/CD completely removed [@insspb](https://github.com/insspb) [@ssbarnea](https://github.com/ssbarnea) [@insspb](https://github.com/insspb) (#1363, #1367)

Code style and docs changes:

* Added black formatting verification on lint stage + project files reformatting [@ssbarnea](https://github.com/ssbarnea) [@insspb](https://github.com/insspb) (#1368)
* Added pep257 docstring for tests/* files [@insspb](https://github.com/insspb) (#1369, #1370, #1371, #1372, #1373, #1374, #1375, #1376, #1377, #1378, #1380, #1381)
* Added pep257 docstring for tests/conftests.py [@kishan](https://github.com/kishan3) (#1272, #1263)
* Added pep257 docstring for tests/replay/conftest.py [@kishan](https://github.com/kishan3) (#1270, #1268)
* Added pep257 docstring for docs/__init__.py [@kishan](https://github.com/kishan3) (#1273, #1265)
* Added missing docstring headers to all files [@croesnick](https://github.com/croesnick) (#1269, #1283)
* Gitter links replaced by Slack in README [@browniebroke](https://github.com/browniebroke) (#1282)
* flake8-docstrings tests added to CI/CD [@ssbarnea](https://github.com/ssbarnea) (#1284)
* Activated pydocstyle rule: D401 - First line should be in imperative mood [@ssbarnea](https://github.com/ssbarnea) (#1285)
* Activated pydocstyle rule: D200 - One-line docstring should fit on one line with quotes [@ssbarnea](https://github.com/ssbarnea) (#1288)
* Activated pydocstyle rule: D202 - No blank lines allowed after function docstring [@ssbarnea](https://github.com/ssbarnea) (#1288)
* Activated pydocstyle rule: D205 - 1 blank line required between summary line and description [@ssbarnea](https://github.com/ssbarnea) (#1286, #1287)
* Activated pydocstyle rule: ABS101 [@ssbarnea](https://github.com/ssbarnea) (#1288)
* Replaced click documentation links to point to version 7 [@igorbasko01](https://github.com/igorbasko01) (#1303)
* Updated submodule link to latest version with documentation links fix [@DanBoothDev](https://github.com/DanBoothDev) (#1388)
* Fixed links in main README file. [@insspb](https://github.com/insspb) (#1342)
* Fix indentation of .cookiecutterrc in README.md [@mhsekhavat](https://github.com/mhsekhavat) (#1322)
* Changed format of loggers invocation [@insspb](https://github.com/insspb) (#1307)

## 1.7.0 (2019-12-22) Old friend

Important Changes:

* Drop support for EOL Python 3.4, thanks to [@jamescurtin](https://github.com/jamescurtin) and [@insspb](https://github.com/insspb) (#1024)
* Drop support for EOL Python 3.3, thanks to [@hugovk](https://github.com/hugovk) (#1024)
* Increase the minimum click version to 7.0, thanks to [@rly](https://github.com/rly) and [@luzfcb](https://github.com/luzfcb) (#1168)

Other Changes:

* PEP257 fixing docstrings in exceptions.py. Thanks to [@MinchinWeb](https://github.com/MinchinWeb) (#1237)
* PEP257 fixing docstrings in replay.py. Thanks to [@kishan](https://github.com/kishan3) (#1234)
* PEP257 fixing docstrings in test_unzip.py. Thanks to [@tonytheleg](https://github.com/tonytheleg) and [@insspb](https://github.com/insspb) (#1236, #1262)
* Fixed tests sequence for appveyor, to exclude file not found bug. Thanks to [@insspb](https://github.com/insspb) (#1257)
* Updates REAMDE.md with svg badge for appveyor. Thanks to [@sobolevn](https://github.com/sobolevn) (#1254)
* Add missing {% endif %} to Choice Variables example. Thanks to [@mattstibbs](https://github.com/mattstibbs) (#1249)
* Core documentation converted to Markdown format thanks to [@wagnernegrao](https://github.com/wagnernegrao), [@insspb](https://github.com/insspb) (#1216)
* Tests update: use sys.executable when invoking python in python 3 only environment thanks to [@vincentbernat](https://github.com/vincentbernat) (#1221)
* Prevent `click` API v7.0 from showing choices when already shown, thanks to [@rly](https://github.com/rly) and [@luzfcb](https://github.com/luzfcb) (#1168)
* Test the codebase with python3.8 beta on tox and travis-ci (#1206), thanks to [@mihrab34](https://github.com/mihrab34)
* Add a [CODE\_OF\_CONDUCT.md](https://github.com/audreyfeldroy/cookiecutter/blob/master/CODE_OF_CONDUCT.md) file to the project, thanks to [@andreagrandi](https://github.com/andreagrandi) (#1009)
* Update docstrings in `cookiecutter/main.py`, `cookiecutter/__init__.py`, and `cookiecutter/log.py` to follow the PEP 257 style guide, thanks to [@meahow](https://github.com/meahow) (#998, #999, #1000)
* Update docstrings in `cookiecutter/utils.py` to follow the PEP 257 style guide, thanks to [@dornheimer](https://github.com/dornheimer)(#1026)
* Fix grammar in *Choice Variables* documentation, thanks to [@jubrilissa](https://github.com/jubrilissa) (#1011)
* Update installation docs with links to the Windows Subsystem and GNU utilities, thanks to [@Nythiennzo](https://github.com/Nythiennzo) for the PR and [@BruceEckel](https://github.com/BruceEckel) for the review (#1016)
* Upgrade flake8 to version 3.5.0, thanks to [@cclauss](https://github.com/cclauss) (#1038)
* Update tutorial with explanation for how cookiecutter finds the template file, thanks to [@accraze](https://github.com/accraze)(#1025)
* Update CI config files to use `TOXENV` environment variable, thanks to [@asottile](https://github.com/asottile) (#1019)
* Improve user documentation for writing hooks, thanks to [@jonathansick](https://github.com/jonathansick) (#1057)
* Make sure to preserve the order of items in the generated cookiecutter context, thanks to [@hackebrot](https://github.com/hackebrot) (#1074)
* Fixed DeprecationWarning for a regular expression on python 3.6, thanks to [@reinout](https://github.com/reinout) (#1124)
* Document use of cookiecutter-template topic on GitHub, thanks to [@ssbarnea](https://github.com/ssbarnea) (#1189)
* Update README badge links, thanks to [@luzfcb](https://github.com/luzfcb) (#1207)
* Update prompt.py to match pep257 guidelines, thanks to [@jairideout](https://github.com/jairideout) (#1105)
* Update link to Jinja2 extensions documentation, thanks to [@dacog](https://github.com/dacog) (#1193)
* Require pip 9.0.0 or newer for tox environments, thanks to [@hackebrot](https://github.com/hackebrot) (#1215)
* Use io.open contextmanager when reading hook files, thanks to [@jcb91](https://github.com/jcb91) (#1147)
* Add more cookiecutter templates to the mix:
  * [cookiecutter-python-cli](https://github.com/xuanluong/cookiecutter-python-cli) by [@xuanluong](https://github.com/xuanluong) (#1003)
  * [cookiecutter-docker-science](https://github.com/docker-science/cookiecutter-docker-science) by [@takahi-i](https://github.com/takahi-i) (#1040)
  * [cookiecutter-flask-skeleton](https://github.com/realpython/cookiecutter-flask-skeleton) by [@mjhea0](https://github.com/mjhea0) (#1052)
  * [cookiecutter-awesome](https://github.com/Pawamoy/cookiecutter-awesome) by [@Pawamoy](https://github.com/Pawamoy) (#1051)
  * [cookiecutter-flask-ask](https://github.com/chrisvoncsefalvay/cookiecutter-flask-ask) by [@machinekoder](https://github.com/machinekoder) (#1056)
  * [cookiecutter-data-driven-journalism](https://github.com/jastark/cookiecutter-data-driven-journalism) by [@JAStark](https://github.com/JAStark) (#1020)
  * [cookiecutter-tox-plugin](https://github.com/tox-dev/cookiecutter-tox-plugin) by [@obestwalter](https://github.com/obestwalter) (#1103)
  * [cookiecutter-django-dokku](https://github.com/mashrikt/cookiecutter-django-dokku) by [@mashrikt](https://github.com/mashrikt) (#1093)

## 1.6.0 (2017-10-15) Tim Tam

New Features:

* Include template path or template URL in cookiecutter context under `_template`, thanks to [@aroig](https://github.com/aroig) (#774)
* Add a URL abbreviation for GitLab template projects, thanks to [@hackebrot](https://github.com/hackebrot) (#963)
* Add option to use templates from Zip files or Zip URLs, thanks to [@freakboy3742](https://github.com/freakboy3742) (#961)

Bug Fixes:

* Fix an issue with missing default template abbreviations for when a user defined custom abbreviations, thanks to [@noirbizarre](https://github.com/noirbizarre) for the issue report and [@hackebrot](https://github.com/hackebrot) for the fix (#966, #967)
* Preserve existing output directory on project generation failure, thanks to [@ionelmc](https://github.com/ionelmc) for the report and
[@michaeljoseph](https://github.com/michaeljoseph) for the fix (#629, #964)
* Fix Python 3.x error handling for `git` operation failures, thanks to [@jmcarp](https://github.com/jmcarp) (#905)

Other Changes:

* Fix broken link to *Copy without Render* docs, thanks to [@coreysnyder04](https://github.com/coreysnyder04) (#912)
* Improve debug log message for when a hook is not found, thanks to [@raphigaziano](https://github.com/raphigaziano/) (#160)
* Fix module summary and `expand_abbreviations()` doc string as per pep257, thanks to [@terryjbates](https://github.com/terryjbates)
(#772)
* Update doc strings in `cookiecutter/cli.py` and `cookiecutter/config.py` according to pep257, thanks to [@terryjbates](https://github.com/terryjbates) (#922, #931)
* Update doc string for `is_copy_only_path()` according to pep257, thanks to [@mathagician](https://github.com/mathagician) and
[@terryjbates](https://github.com/terryjbates) (#935, #949)
* Update doc strings in `cookiecutter/extensions.py` according to pep257, thanks to [@meahow](https://github.com/meahow) (#996)
* Fix miscellaneous issues with building docs, thanks to [@stevepiercy](https://github.com/stevepiercy) (#889)
* Re-implement Makefile and update several make rules, thanks to [@hackebrot](https://github.com/hackebrot) (#930)
* Fix broken link to pytest docs, thanks to [@eyalev](https://github.com/eyalev) for the issue report and [@devstrat](https://github.com/devstrat) for the fix (#939, #940)
* Add `test_requirements.txt` file for easier testing outside of tox, thanks to [@ramnes](https://github.com/ramnes) (#945)
* Improve wording in *copy without render* docs, thanks to [@eyalev](https://github.com/eyalev) (#938)
* Fix a number of typos, thanks to [@delirious-lettuce](https://github.com/delirious-lettuce) (#968)
* Improved *extra context* docs by noting that extra context keys must be present in the template\'s `cookiecutter.json`, thanks to
[@karantan](https://github.com/karantan) for the report and fix (#863, #864)
* Added more cookiecutter templates to the mix:
  * [cookiecutter-kata-cpputest](https://github.com/13coders/cookiecutter-kata-cpputest) by [@13coders](https://github.com/13coders) (#901)
  * [cookiecutter-kata-gtest](https://github.com/13coders/cookiecutter-kata-gtest) by [@13coders](https://github.com/13coders) (#901)
  * [cookiecutter-pyramid-talk-python-starter](https://github.com/mikeckennedy/cookiecutter-pyramid-talk-python-starter) by [@mikeckennedy](https://github.com/mikeckennedy) (#915)
  * [cookiecutter-android](https://github.com/alexfu/cookiecutter-android) by [@alexfu](https://github.com/alexfu) (#890)
  * [cookiecutter-lux-python](https://github.com/alexkey/cookiecutter-lux-python) by [@alexkey](https://github.com/alexkey) (#895)
  * [cookiecutter-git](https://github.com/webevllc/cookiecutter-git) by [@tuxredux](https://github.com/tuxredux) (#921)
  * [cookiecutter-ansible-role-ci](https://github.com/ferrarimarco/cookiecutter-ansible-role) by [@ferrarimarco](https://github.com/ferrarimarco) (#903)
  * [cookiecutter\_dotfile](https://github.com/bdcaf/cookiecutter_dotfile) by [@bdcaf](https://github.com/bdcaf) (#925)
  * [painless-continuous-delivery](https://github.com/painless-software/painless-continuous-delivery) by [@painless-software](https://github.com/painless-software)
        (#927)
  * [cookiecutter-molecule](https://github.com/retr0h/cookiecutter-molecule) by [@retr0h](https://github.com/retr0h) (#954)
  * [sublime-snippet-package-template](https://github.com/agenoria/sublime-snippet-package-template) by [@agenoria](https://github.com/agenoria) (#956)
  * [cookiecutter-conda-python](https://github.com/conda/cookiecutter-conda-python) by [@conda](https://github.com/conda) (#969)
  * [cookiecutter-flask-minimal](https://github.com/candidtim/cookiecutter-flask-minimal) by [@candidtim](https://github.com/candidtim) (#977)
  * [cookiecutter-pypackage-rust-cross-platform-publish](https://github.com/mckaymatt/cookiecutter-pypackage-rust-cross-platform-publish) by [@mckaymatt](https://github.com/mckaymatt) (#957)
  * [cookie-cookie](https://github.com/tuxredux/cookie-cookie) by [@tuxredux](https://github.com/tuxredux) (#951)
  * [cookiecutter-telegram-bot](https://github.com/Ars2014/cookiecutter-telegram-bot) by [@Ars2014](https://github.com/Ars2014) (#984)
  * [python-project-template](https://github.com/Kwpolska/python-project-template) by [@Kwpolska](https://github.com/Kwpolska) (#986)
  * [wemake-django-template](https://github.com/wemake-services/wemake-django-template) by [@wemake-services](https://github.com/wemake-services) (#990)
  * [cookiecutter-raml](https://github.com/genzj/cookiecutter-raml) by [@genzj](https://github.com/genzj) (#994)
  * [cookiecutter-anyblok-project](https://github.com/AnyBlok/cookiecutter-anyblok-project) by [@AnyBlok](https://github.com/AnyBlok) (#988)
  * [cookiecutter-devenv](https://bitbucket.org/greenguavalabs/cookiecutter-devenv.git) by [@greenguavalabs](https://bitbucket.org/greenguavalabs) (#991)

## 1.5.1 (2017-02-04) Alfajor

New Features:

* Major update to installation documentation, thanks to [@stevepiercy](https://github.com/stevepiercy) (#880)

Bug Fixes:

* Resolve an issue around default values for dict variables, thanks to [@e-kolpakov](https://github.com/e-kolpakov) for raising the issue and [@hackebrot](https://github.com/hackebrot) for the PR (#882, #884)

Other Changes:

* Contributor documentation reST fixes, thanks to [@stevepiercy](https://github.com/stevepiercy) (#878)
* Added more cookiecutter templates to the mix:
  * [widget-cookiecutter](https://github.com/jupyter/widget-cookiecutter) by [@willingc](https://github.com/willingc) (#781)
  * [cookiecutter-django-foundation](https://github.com/Parbhat/cookiecutter-django-foundation) by [@Parbhat](https://github.com/Parbhat) (#804)
  * [cookiecutter-tornado](https://github.com/hkage/cookiecutter-tornado) by [@hkage](https://github.com/hkage) (#807)
  * [cookiecutter-django-ansible](https://github.com/HackSoftware/cookiecutter-django-ansible) by [@Ivaylo-Bachvarov](https://github.com/Ivaylo-Bachvarov)(#816)
  * [CICADA](https://github.com/TAMU-CPT/CICADA) by [@elenimijalis](https://github.com/elenimijalis) (#840)
  * [cookiecutter-tf-module](https://github.com/DualSpark/cookiecutter-tf-module) by [@VDuda](https://github.com/VDuda) (#843)
  * [cookiecutter-pyqt4](https://github.com/aeroaks/cookiecutter-pyqt4) by [@aeroaks](https://github.com/aeroaks) (#847)
  * [cookiecutter-golang](https://github.com/lacion/cookiecutter-golang) by [@mjhea0](https://github.com/mjhea0) and [@lacion](https://github.com/lacion) (#872, #873)
  * [cookiecutter-elm](https://github.com/m-x-k/cookiecutter-elm.git), [cookiecutter-java](https://github.com/m-x-k/cookiecutter-java.git) and [cookiecutter-spring-boot](https://github.com/m-x-k/cookiecutter-spring-boot.git) by [@m-x-k](https://github.com/m-x-k) (#879)

## 1.5.0 (2016-12-18) Alfajor

The primary goal of this release was to add command-line support for passing extra context, address minor bugs and make a number of
improvements.

New Features:

* Inject extra context with command-line arguments, thanks to [@msabramo](https://github.com/msabramo) and [@michaeljoseph](https://github.com/michaeljoseph) (#666).
* Updated conda installation instructions to work with the new conda-forge distribution of Cookiecutter, thanks to [@pydanny](https://github.com/pydanny) and especially [@bollwyvl](https://github.com/bollwyvl) (#232, #705).
* Refactor code responsible for interaction with version control systems and raise better error messages, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#778).
* Add support for executing cookiecutter using `python -m cookiecutter` or from a checkout/zip file, thanks to [@brettcannon](https://github.com/brettcannon) (#788).
* New CLI option `--debug-file PATH` to store a log file on disk. By default no log file is written. Entries for `DEBUG` level and     higher. Thanks to [@hackebrot](https://github.com/hackebrot)(#792).
* Existing templates in a user\'s `cookiecutters_dir` (default is `~/.cookiecutters/`) can now be referenced by directory name, thanks
to [@michaeljoseph](https://github.com/michaeljoseph) (#825).
* Add support for dict values in `cookiecutter.json`, thanks to [@freakboy3742](https://github.com/freakboy3742) and [@hackebrot](https://github.com/hackebrot) (#815, #858).
* Add a `jsonify` filter to default jinja2 extensions that json.dumps a Python object into a string, thanks to [@aroig](https://github.com/aroig) (#791).

Bug Fixes:

* Fix typo in the error logging text for when a hook did not exit successfully, thanks to [@luzfcb](https://github.com/luzfcb)    (#656)
* Fix an issue around **replay** file names when **cookiecutter** is used with a relative path to a template, thanks to    [@eliasdorneles](https://github.com/eliasdorneles) for raising the issue and [@hackebrot](https://github.com/hackebrot) for the PR (#752, #753)
* Ignore hook files with tilde-suffixes, thanks to [@hackebrot](https://github.com/hackebrot) (#768)
* Fix a minor issue with the code that generates a name for a template, thanks to [@hackebrot](https://github.com/hackebrot)(#798)
* Handle empty hook file or other OS errors, thanks to [@christianmlong](https://github.com/christianmlong) for raising this bug and [@jcarbaugh](https://github.com/jcarbaugh) and [@hackebrot](https://github.com/hackebrot) for the fix (#632, #729, #862)
* Resolve an issue with custom extensions not being loaded for `pre_gen_project` and `post_gen_project` hooks, thanks to [@cheungnj](https://github.com/cheungnj) (#860)

Other Changes:

* Remove external dependencies from tests, so that tests can be run w/o network connection, thanks to [@hackebrot](https://github.com/hackebrot) (#603)
* Remove execute permissions on Python files, thanks to [@mozillazg](https://github.com/mozillazg) (#650)
* Report code coverage info from AppVeyor build to codecov, thanks to [@ewjoachim](https://github.com/ewjoachim) (#670)
* Documented functions and methods lacking documentation, thanks to [@pydanny](https://github.com/pydanny) (#673)
* Documented `__init__` methods for Environment objects, thanks to [@pydanny](https://github.com/pydanny) (#677)
* Updated whichcraft to 0.4.0, thanks to [@pydanny](https://github.com/pydanny).
* Updated documentation link to Read the Docs, thanks to [@natim](https://github.com/Natim) (#687)
* Moved cookiecutter templates and added category links, thanks to [@willingc](https://github.com/willingc) (#674)
* Added Github Issue Template, thanks to [@luzfcb](https://github.com/luzfcb) (#700)
* Added `ssh` repository examples, thanks to [@pokoli](https://github.com/pokoli/) (#702)
* Fix links to the cookiecutter-data-science template and its documentation, thanks to [@tephyr](https://github.com/tephyr) for the PR and [@willingc](https://github.com/willingc) for the review (#711, #714)
* Update link to docs for Django\'s `--template` command line option, thanks to [@purplediane](https://github.com/purplediane) (#754)
* Create *hook backup files* during the tests as opposed to having them as static files in the repository, thanks to [@hackebrot](https://github.com/hackebrot) (#789)

* Applied PEP 257 docstring conventions to:
  * `environment.py`, thanks to [@terryjbates](https://github.com/terryjbates) (#759)
  * `find.py`, thanks to [@terryjbates](https://github.com/terryjbates) (#761)
  * `generate.py`, thanks to [@terryjbates](https://github.com/terryjbates) (#764)
  * `hooks.py`, thanks to [@terryjbates](https://github.com/terryjbates) (#766)
  * `repository.py`, thanks to [@terryjbates](https://github.com/terryjbates) (#833)
  * `vcs.py`, thanks to [@terryjbates](https://github.com/terryjbates) (#831)

* Fix link to the Tryton cookiecutter, thanks to [@cedk](https://github.com/cedk) and [@nicoe](https://github.com/nicoe) (#697, #698)
* Added PyCon US 2016 sponsorship to README, thanks to [@purplediane](https://github.com/purplediane) (#720)
* Added a sprint contributor doc, thanks to [@phoebebauer](https://github.com/phoebebauer) (#727)
* Converted readthedocs links (.org -\> .io), thanks to [@adamchainz](https://github.com/adamchainz) (#718)
* Added Python 3.6 support, thanks to [@suledev](https://github.com/suledev) (#728)
* Update occurrences of `repo_name` in documentation, thanks to [@palmerev](https://github.com/palmerev) (#734)
* Added case studies document, thanks to [@pydanny](https://github.com/pydanny) (#735)
* Added first steps cookiecutter creation tutorial, thanks to [@BruceEckel](https://github.com/BruceEckel) (#736)
* Reorganised tutorials and setup git submodule to external tutorial, thanks to [@dot2dotseurat](https://github.com/dot2dotseurat) (#740)
* Debian installation instructions, thanks to [@ivanlyon](https://github.com/ivanlyon) (#738)
* Usage documentation typo fix., thanks to [@terryjbates](https://github.com/terryjbates) (#739)
* Updated documentation copyright date, thanks to [@zzzirk](https://github.com/zzzirk) (#747)
* Add a make rule to update git submodules, thanks to [@hackebrot](https://github.com/hackebrot) (#746)
* Split up advanced usage docs, thanks to [@zzzirk](https://github.com/zzzirk) (#749)
* Documentation for the `no_input` option, thanks to [@pokoli](https://github.com/pokoli/) (#701)
* Remove unnecessary shebangs from python files, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#763)
* Refactor cookiecutter template identification, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#777)
* Add a `cli_runner` test fixture to simplify CLI tests, thanks to [@hackebrot](https://github.com/hackebrot) (#790)
* Add a check to ensure cookiecutter repositories have JSON context, thanks to [@michaeljoseph](https://github.com/michaeljoseph)(#782)
* Rename the internal function that determines whether a file should be rendered, thanks to [@audreyfeldroy](https://github.com/audreyfeldroy) for raising the issue and [@hackebrot](https://github.com/hackebrot)for the PR (#741, #802)
* Fix typo in docs, thanks to [@mwarkentin](https://github.com/mwarkentin) (#828)
* Fix broken link to *Invoke* docs, thanks to [@B3QL](https://github.com/B3QL) (#820)
* Add documentation to `render_variable` function in `prompt.py`, thanks to [@pydanny](https://github.com/pydanny) (#678)
* Fix python3.6 travis-ci and tox configuration, thanks to [@luzfcb](https://github.com/luzfcb) (#844)
* Add missing encoding declarations to python files, thanks to [@andytom](https://github.com/andytom) (#852)
* Disable poyo logging for tests, thanks to [@hackebrot](https://github.com/hackebrot) (#855)
* Remove pycache directories in make clean-pyc, thanks to [@hackebrot](https://github.com/hackebrot) (#849)
* Refactor hook system to only find the requested hook, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#834)
* Add tests for custom extensions in `pre_gen_project` and `post_gen_project` hooks, thanks to [@hackebrot](https://github.com/hackebrot) (#856)
* Make the build reproducible by avoiding nondeterministic keyword arguments, thanks to [@lamby](https://github.com/lamby) and [@hackebrot](https://github.com/hackebrot) (#800, #861)
* Extend CLI help message and point users to the github project to engage with the community, thanks to [@hackebrot](https://github.com/hackebrot) (#859)

* Added more cookiecutter templates to the mix:
  * [cookiecutter-funkload-friendly](https://github.com/tokibito/cookiecutter-funkload-friendly) by [@tokibito](https://github.com/tokibito) (#657)
  * [cookiecutter-reveal.js](https://github.com/keimlink/cookiecutter-reveal.js) by [@keimlink](https://github.com/keimlink) (#660)
  * [cookiecutter-python-app](https://github.com/mdklatt/cookiecutter-python-app) by [@mdklatt](https://github.com/mdklatt) (#659)
  * [morepath-cookiecutter](https://github.com/morepath/morepath-cookiecutter) by [@href](https://github.com/href) (#672)
  * [hovercraft-slides](https://github.com/Springerle/hovercraft-slides) by [@jhermann](https://github.com/jhermann) (#665)
  * [cookiecutter-es6-package](https://github.com/ratson/cookiecutter-es6-package) by [@ratson](https://github.com/ratson) (#667)
  * [cookiecutter-webpack](https://github.com/hzdg/cookiecutter-webpack) by [@hzdg](https://github.com/hzdg) (#668)
  * [cookiecutter-django-herokuapp](https://github.com/dulaccc/cookiecutter-django-herokuapp) by [@dulaccc](https://github.com/dulaccc) (#374)
  * [cookiecutter-django-aws-eb](https://github.com/dolphinkiss/cookiecutter-django-aws-eb) by [@peterlauri](https://github.com/peterlauri) (#626)
  * [wagtail-starter-kit](https://github.com/tkjone/wagtail-starter-kit) by [@tkjone](https://github.com/tkjone) (#658)
  * [cookiecutter-dpf-effect](https://github.com/SpotlightKid/cookiecutter-dpf-effect) by [@SpotlightKid](https://github.com/SpotlightKid) (#663)
  * [cookiecutter-dpf-audiotk](https://github.com/SpotlightKid/cookiecutter-dpf-audiotk) by [@SpotlightKid](https://github.com/SpotlightKid) (#663)
  * [cookiecutter-template](https://github.com/eviweb/cookiecutter-template) by [@eviweb](https://github.com/eviweb) (#664)
  * [cookiecutter-angular2](https://github.com/matheuspoleza/cookiecutter-angular2) by [@matheuspoleza](https://github.com/matheuspoleza) (#675)
  * [cookiecutter-data-science](http://drivendata.github.io/cookiecutter-data-science/) by [@pjbull](https://github.com/pjbull) (#680)
  * [cc\_django\_ember\_app](https://bitbucket.org/levit_scs/cc_django_ember_app) by [@nanuxbe](https://github.com/nanuxbe) (#686)
  * [cc\_project\_app\_drf](https://bitbucket.org/levit_scs/cc_project_app_drf) by [@nanuxbe](https://github.com/nanuxbe) (#686)
  * [cc\_project\_app\_full\_with\_hooks](https://bitbucket.org/levit_scs/cc_project_app_full_with_hooks) by [@nanuxbe](https://github.com/nanuxbe) (#686)
  * [beat-generator](https://github.com/elastic/beat-generator) by [@ruflin](https://github.com/ruflin) (#695)
  * [cookiecutter-scala](https://github.com/Plippe/cookiecutter-scala) by [@Plippe](https://github.com/Plippe) (#751)
  * [cookiecutter-snakemake-analysis-pipeline](https://github.com/xguse/cookiecutter-snakemake-analysis-pipeline) by [@xguse](https://github.com/xguse) (#692)
  * [cookiecutter-py3tkinter](https://github.com/ivanlyon/cookiecutter-py3tkinter) by [@ivanlyon](https://github.com/ivanlyon) (#730)
  * [pyramid-cookiecutter-alchemy](https://github.com/Pylons/pyramid-cookiecutter-alchemy) by [@stevepiercy](https://github.com/stevepiercy) (#745)
  * [pyramid-cookiecutter-starter](https://github.com/Pylons/pyramid-cookiecutter-starter) by [@stevepiercy](https://github.com/stevepiercy) (#745)
  * [pyramid-cookiecutter-zodb](https://github.com/Pylons/pyramid-cookiecutter-zodb) by [@stevepiercy](https://github.com/stevepiercy) (#745)
  * [substanced-cookiecutter](https://github.com/Pylons/substanced-cookiecutter) by [@stevepiercy](https://github.com/stevepiercy) (#745)
  * [cookiecutter-simple-django-cn](https://github.com/shenyushun/cookiecutter-simple-django-cn) by [@shenyushun](https://github.com/shenyushun) (#765)
  * [cookiecutter-pyqt5](https://github.com/mandeepbhutani/cookiecutter-pyqt5) by [@mandeepbhutani](https://github.com/mandeepbhutani) (#797)
  * [cookiecutter-xontrib](https://github.com/laerus/cookiecutter-xontrib) by [@laerus](https://github.com/laerus) (#817)
  * [cookiecutter-reproducible-science](https://github.com/mkrapp/cookiecutter-reproducible-science) by [@mkrapp](https://github.com/mkrapp) (#826)
  * [cc-automated-drf-template](https://github.com/TAMU-CPT/cc-automated-drf-template) by [@elenimijalis](https://github.com/elenimijalis) (#832)

## 1.4.0 (2016-03-20) Shortbread

The goal of this release is changing to a strict Jinja2 environment, paving the way to more awesome in the future, as well as adding support
for Jinja2 extensions.

New Features:

* Added support for Jinja2 extension support, thanks to [@hackebrot](https://github.com/hackebrot) (#617).
* Now raises an error if Cookiecutter tries to render a template that contains an undefined variable. Makes generation more robust and
secure (#586). Work done by [@hackebrot](https://github.com/hackebrot) (#111, #586, #592)
* Uses strict Jinja2 env in prompt, thanks to [@hackebrot](https://github.com/hackebrot) (#598, #613)
* Switched from pyyaml/ruamel.yaml libraries that were problematic across platforms to the pure Python [poyo](https://pypi.python.org/pypi/poyo) library, thanks to [@hackebrot](https://github.com/hackebrot) (#557, #569, #621)
* User config values for `cookiecutters_dir` and `replay_dir` now support environment variable and user home expansion, thanks to   [@nfarrar](https://github.com/nfarrar) for the suggestion and [@hackebrot](https://github.com/hackebrot) for the PR (#640,#642)
* Add [jinja2-time](https://pypi.python.org/pypi/jinja2-time) as default extension for dates and times in templates via `{% now 'utc' %}`,thanks to [@hackebrot](https://github.com/hackebrot) (#653)

Bug Fixes:

* Provided way to define options that have no defaults, thanks to [@johtso](https://github.com/johtso) (#587, #588)
* Make sure that `replay.dump()` and `replay.load()` use the correct user config, thanks to [@hackebrot](https://github.com/hackebrot)
(#590, #594)
* Added correct CA bundle for Git on Appveyor, thanks to [@maiksensi](https://github.com/maiksensi) (#599, #602)
* Open `HISTORY.rst` with `utf-8` encoding when reading the changelog, thanks to [@0-wiz-0](https://github.com/0-wiz-0) for submitting the issue and [@hackebrot](https://github.com/hackebrot) for the fix (#638, #639)
* Fix repository indicators for [privaterepository](http://cookiecutter.readthedocs.io/en/latest/usage.html#works-with-private-repos)
urls, thanks to [@habnabit](https://github.com/habnabit) for the fix (#595) and [@hackebrot](https://github.com/hackebrot) for the
tests (#655)

Other Changes:

* Set path before running tox, thanks to [@maiksensi](https://github.com/maiksensi) (#615, #620)
* Removed xfail in test\_cookiecutters, thanks to [@hackebrot](https://github.com/hackebrot) (#618)
* Removed django-cms-plugin on account of 404 error, thanks to [@mativs](https://github.com/mativs) and [@pydanny](https://github.com/pydanny) (#593)
* Fixed docs/usage.rst, thanks to [@macrotim](https://github.com/macrotim) (#604)
* Update .gitignore to latest Python.gitignore and ignore PyCharm files, thanks to [@audreyfeldroy](https://github.com/audreyfeldroy)
* Use open context manager to read context\_file in generate() function, thanks to [@hackebrot](https://github.com/hackebrot)
(#607, #608)
* Added documentation for choice variables, thanks to [@maiksensi](https://github.com/maiksensi) (#611)
* Set up Scrutinizer to check code quality, thanks to [@audreyfeldroy](https://github.com/audreyfeldroy)
* Drop distutils support in setup.py, thanks to [@hackebrot](https://github.com/hackebrot) (#606, #609)
* Change cookiecutter-pypackage-minimal link, thanks to [@kragniz](https://github.com/kragniz) (#614)
* Fix typo in one of the template\'s description, thanks to [@ryanfreckleton](https://github.com/ryanfreckleton) (#643)
* Fix broken link to [\_copy\_without\_render](http://cookiecutter.readthedocs.io/en/latest/advanced_usage.html#copy-without-render)
    in *troubleshooting.rst*, thanks to [@ptim](https://github.com/ptim) (#647)

* Added more cookiecutter templates to the mix:
  * [cookiecutter-pipproject](https://github.com/wdm0006/cookiecutter-pipproject) by [@wdm0006](https://github.com/wdm0006) (#624)
  * [cookiecutter-flask-2](https://github.com/wdm0006/cookiecutter-flask) by [@wdm0006](https://github.com/wdm0006) (#624)
  * [cookiecutter-kotlin-gradle](https://github.com/thomaslee/cookiecutter-kotlin-gradle) by [@thomaslee](https://github.com/thomaslee) (#622)
  * [cookiecutter-tryton-fulfilio](https://github.com/fulfilio/cookiecutter-tryton) by [@cedk](https://github.com/cedk) (#631)
  * [django-starter](https://github.com/tkjone/django-starter) by [@tkjone](https://github.com/tkjone) (#635)
  * [django-docker-bootstrap](https://github.com/legios89/django-docker-bootstrap) by [@legios89](https://github.com/legios89) (#636)
  * [cookiecutter-mediawiki-extension](https://github.com/JonasGroeger/cookiecutter-mediawiki-extension) by [@JonasGroeger](https://github.com/JonasGroeger) (#645)
  * [cookiecutter-django-gulp](https://github.com/valerymelou/cookiecutter-django-gulp) by [@valerymelou](https://github.com/valerymelou) (#648)

## 1.3.0 (2015-11-10) Pumpkin Spice

The goal of this release is to extend the user config feature and to make hook execution more robust.

New Features:

* Abort project generation if `pre_gen_project` or `post_gen_project` hook scripts fail, thanks to [@eliasdorneles](https://github.com/eliasdorneles) (#464, #549)
* Extend user config capabilities with additional cli options `--config-file` and `--default-config` and environment variable   `COOKIECUTTER_CONFIG`, thanks to [@jhermann](https://github.com/jhermann), [@pfmoore](https://github.com/pfmoore), and [@hackebrot](https://github.com/hackebrot) (#258, #424, #565)

Bug Fixes:

* Fixed conditional dependencies for wheels in setup.py, thanks to [@hackebrot](https://github.com/hackebrot) (#557, #568)
* Reverted skipif markers to use correct reasons (bug fixed in pytest), thanks to [@hackebrot](https://github.com/hackebrot)
(#574)

Other Changes:

* Improved path and documentation for rendering the Sphinx documentation, thanks to [@eliasdorneles](https://github.com/eliasdorneles) and [@hackebrot](https://github.com/hackebrot) (#562, #583)
* Added additional help entrypoints, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#563, #492)
* Added Two Scoops Academy to the README, thanks to [@hackebrot](https://github.com/hackebrot) (#576)
* Now handling trailing slash on URL, thanks to [@ramiroluz](https://github.com/ramiroluz) (#573, #546)
* Support for testing x86 and x86-64 architectures on appveyor, thanks to [@maiksensi](https://github.com/maiksensi) (#567)
* Made tests work without installing Cookiecutter, thanks to [@vincentbernat](https://github.com/vincentbernat) (#550)
* Encoded the result of the hook template to utf8, thanks to [@ionelmc](https://github.com/ionelmc) (#577. #578)
* Added test for \_run\_hook\_from\_repo\_dir, thanks to [@hackebrot](https://github.com/hackebrot) (#579, #580)
* Implemented bumpversion, thanks to [@hackebrot](https://github.com/hackebrot) (#582)
* Added more cookiecutter templates to the mix:
  * [cookiecutter-octoprint-plugin](https://github.com/OctoPrint/cookiecutter-octoprint-plugin) by [@foosel](https://github.com/foosel) (#560)
  * [wagtail-cookiecutter-foundation](https://github.com/chrisdev/wagtail-cookiecutter-foundation) by [@chrisdev](https://github.com/chrisdev), et al. (#566)

## 1.2.1 (2015-10-18) Zimtsterne

*Zimtsterne are cinnamon star cookies.*

New Feature:

* Returns rendered project dir, thanks to [@hackebrot](https://github.com/hackebrot) (#553)

Bug Fixes:

* Factor in *choice* variables (as introduced in 1.1.0) when using a user config or extra context, thanks to [@ionelmc](https://github.com/ionelmc) and [@hackebrot](https://github.com/hackebrot) (#536, #542).

Other Changes:

* Enable py35 support on Travis by using Python 3.5 as base Python ([@maiksensi](https://github.com/maiksensi) / #540)
* If a filename is empty, do not generate. Log instead ([@iljabauer](https://github.com/iljabauer) / #444)
* Fix tests as per last changes in [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage), thanks to [@eliasdorneles](https://github.com/eliasdorneles)(#555).
* Removed deprecated cookiecutter-pylibrary-minimal from the list, thanks to [@ionelmc](https://github.com/ionelmc) (#556)
* Moved to using rualmel.yaml instead of PyYAML, except for Windows users on Python 2.7, thanks
    to [@pydanny](https://github.com/pydanny) (#557)

*Why 1.2.1 instead of 1.2.0? There was a problem in the distribution that we pushed to PyPI. Since you can\'t replace previous files uploaded to PyPI, we deleted the files on PyPI and released 1.2.1.*

## 1.1.0 (2015-09-26) Snickerdoodle

The goals of this release were ```copy without render``` and a few additional command-line options such as ```--overwrite-if-exists```, ```---replay```, and ```output-dir```.

Features:

* Added [copy without render](http://cookiecutter.readthedocs.io/en/latest/advanced_usage.html#copy-without-render) feature, making it much easier for developers of Ansible, Salt Stack, and other recipe-based tools to work with Cookiecutter. Thanks to [@osantana](https://github.com/osantana) and [@LucianU](https://github.com/LucianU) for their innovation, as well as [@hackebrot](https://github.com/hackebrot) for fixing the Windows problems (#132, #184, #425).
* Added specify output directory, thanks to [@tony](https://github.com/tony) and [@hackebrot](https://github.com/hackebrot) (#531, #452).
* Abort template rendering if the project output directory already exists, thanks to [@lgp171188](https://github.com/lgp171188)
(#470, #471).
* Add a flag to overwrite existing output directory, thanks to [@lgp171188](https://github.com/lgp171188) for the implementation (#495) and [@schacki](https://github.com/schacki), [@ionelmc](https://github.com/ionelmc), [@pydanny](https://github.com/pydanny) and [@hackebrot](https://github.com/hackebrot) for submitting issues and code reviews (#475, #493).
* Remove test command in favor of tox, thanks to [@hackebrot](https://github.com/hackebrot) (#480).
* Allow cookiecutter invocation, even without installing it, via `python -m cookiecutter.cli`, thanks to [@vincentbernat](https://github.com/vincentbernat) and [@hackebrot](https://github.com/hackebrot) (#449, #487).
* Improve the type detection handler for online and offline repositories, thanks to [@charlax](https://github.com/charlax)
(#490).
* Add replay feature, thanks to [@hackebrot](https://github.com/hackebrot) (#501).
* Be more precise when raising an error for an invalid user config file, thanks to [@vaab](https://github.com/vaab) and [@hackebrot](https://github.com/hackebrot) (#378, #528).
* Added official Python 3.5 support, thanks to [@pydanny](https://github.com/pydanny) and [@hackebrot](https://github.com/hackebrot) (#522).
* Added support for *choice* variables and switch to click style prompts, thanks to [@hackebrot](https://github.com/hackebrot) (#441, #455).

Other Changes:

* Updated click requirement to \< 6.0, thanks to [@pydanny](https://github.com/pydanny) (#473).
* Added landscape.io flair, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#439).
* Descriptions of PEP8 specifications and milestone management, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#440).
  * Added alternate installation options in the documentation, thanks to [@pydanny](https://github.com/pydanny) (#117, #315).
* The test of the which() function now tests against the date command, thanks to [@vincentbernat](https://github.com/vincentbernat) (#446)
* Ensure file handles in setup.py are closed using with statement, thanks to [@svisser](https://github.com/svisser) (#280).
* Removed deprecated and fully extraneous compat.is\_exe() function, thanks to [@hackebrot](https://github.com/hackebrot) (#485).
* Disabled sudo in .travis, thanks to [@hackebrot](https://github.com/hackebrot) (#482).
* Switched to shields.io for problematic badges, thanks to [@pydanny](https://github.com/pydanny) (#491).
* Added whichcraft and removed `compat.which()`, thanks to [@pydanny](https://github.com/pydanny) (#511).
* Changed to export tox environment variables to codecov, thanks to [@maiksensi](https://github.com/maiksensi). (#508).
* Moved to using click version command, thanks to [@hackebrot](https://github.com/hackebrot) (#489).
* Don\'t use unicode\_literals to please click, thanks to [@vincentbernat](https://github.com/vincentbernat) (#503).
* Remove warning for Python 2.6 from \_\_init\_\_.py, thanks to [@hackebrot](https://github.com/hackebrot).
* Removed compat.py module, thanks to [@hackebrot](https://github.com/hackebrot).
* Added future to requirements, thanks to [@hackebrot](https://github.com/hackebrot).
* Fixed problem where expanduser does not resolve \"\~\" correctly on windows 10 using tox, thanks to [@maiksensi](https://github.com/maiksensi). (#527)

* Added more cookiecutter templates to the mix:
  * [cookiecutter-beamer](https://github.com/luismartingil/cookiecutter-beamer) by [@luismartingil](https://github.com/luismartingil) (#307)
  * [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin) by [@pytest-dev](https://github.com/pytest-dev) and
        [@hackebrot](https://github.com/hackebrot) (#481)
  * [cookiecutter-csharp-objc-binding](https://github.com/SandyChapman/cookiecutter-csharp-objc-binding) by [@SandyChapman](https://github.com/SandyChapman) (#460)
  * [cookiecutter-flask-foundation](https://github.com/JackStouffer/cookiecutter-Flask-Foundation) by [@JackStouffer](https://github.com/JackStouffer) (#457)
  * [cookiecutter-tryton-fulfilio](https://github.com/fulfilio/cookiecutter-tryton) by [@fulfilio](https://github.com/fulfilio) (#465)
  * [cookiecutter-tapioca](https://github.com/vintasoftware/cookiecutter-tapioca) by [@vintasoftware](https://github.com/vintasoftware) (#496)
  * [cookiecutter-sublime-text-3-plugin](https://github.com/kkujawinski/cookiecutter-sublime-text-3-plugin) by [@kkujawinski](https://github.com/kkujawinski) (#500)
  * [cookiecutter-muffin](https://github.com/drgarcia1986/cookiecutter-muffin) by [@drgarcia1986](https://github.com/drgarcia1986) (#494)
  * [cookiecutter-django-rest](https://github.com/agconti/cookiecutter-django-rest) by [@agconti](https://github.com/agconti) (#520)
  * [cookiecutter-es6-boilerplate](https://github.com/agconti/cookiecutter-es6-boilerplate) by [@agconti](https://github.com/agconti) (#521)
  * [cookiecutter-tampermonkey](https://github.com/christabor/cookiecutter-tampermonkey) by [@christabor](https://github.com/christabor) (#516)
  * [cookiecutter-wagtail](https://github.com/torchbox/cookiecutter-wagtail) by [@torchbox](https://github.com/torchbox) (#533)

## 1.0.0 (2015-03-13) Chocolate Chip

The goals of this release was to formally remove support for Python 2.6 and continue the move to using py.test.

Features:

* Convert the unittest suite to py.test for the sake of comprehensibility, thanks to [@hackebrot](https://github.com/hackebrot) (#322, #332, #334, #336, #337, #338, #340, #341, #343, #345, #347, #351, #412, #413, #414).
* Generate pytest coverage, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#326).
* Documenting of Pull Request merging and HISTORY.rst maintenance, thanks to [@michaeljoseph](https://github.com/michaeljoseph)
(#330).
* Large expansions to the tutorials thanks to [@hackebrot](https://github.com/hackebrot) (#384)
* Switch to using Click for command-line options, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#391, #393).
* Added support for working with private repos, thanks to [@marctc](https://github.com/marctc) (#265).
* Wheel configuration thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#118).

Other Changes:

* Formally removed support for 2.6, thanks to [@pydanny](https://github.com/pydanny) (#201).
* Moved to codecov for continuous integration test coverage and badges, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#71, #369).
* Made JSON parsing errors easier to debug, thanks to [@rsyring](https://github.com/rsyring) and [@mark0978](https://github.com/mark0978) (#355, #358, #388).
* Updated to Jinja 2.7 or higher in order to control trailing new lines in templates, thanks to [@sfermigier](https://github.com/sfermigier) (#356).
* Tweaked flake8 to ignore e731, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#390).
* Fixed failing Windows tests and corrected AppVeyor badge link thanks to [@msabramo](https://github.com/msabramo) (#403).

* Added more Cookiecutters to the list:
  * [cookiecutter-scala-spark](https://github.com/jpzk/cookiecutter-scala-spark) by [@jpzk](https://github.com/jpzk)
  * [cookiecutter-atari2600](https://github.com/joeyjoejoejr/cookiecutter-atari2600) by [@joeyjoejoejr](https://github.com/joeyjoejoejr)
  * [cookiecutter-bottle](https://github.com/avelino/cookiecutter-bottle) by [@avelino](https://github.com/avelino)
  * [cookiecutter-latex-article](https://github.com/Kreger51/cookiecutter-latex-article) by [@Kreger51](https://github.com/Kreger51)
  * [cookiecutter-django-rest-framework](https://github.com/jpadilla/cookiecutter-django-rest-framework) by [@jpadilla](https://github.com/jpadilla)
  * [cookiedozer](https://github.com/hackebrot/cookiedozer) by [@hackebrot](https://github.com/hackebrot)

## 0.9.0 (2015-01-13)

The goals of this release were to add the ability to Jinja2ify the cookiecutter.json default values, and formally launch support for Python 3.4.

Features:

* Python 3.4 is now a first class citizen, thanks to everyone.
* cookiecutter.json values are now rendered Jinja2 templates, thanks to \@bollwyvl (#291).
* Move to py.test, thanks to [@pfmoore](https://github.com/pfmoore) (#319) and [@ramiroluz](https://github.com/ramiroluz) (#310).
* Add PendingDeprecation warning for users of Python 2.6, as support for it is gone in Python 2.7, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#201).

Bug Fixes:

* Corrected typo in Makefile, thanks to [@inglesp](https://github.com/inglesp) (#297).
* Raise an exception when users don\'t have git or hg installed, thanks to [@pydanny](https://github.com/pydanny) (#303).

Other changes:

* Creation of [gitter](https://gitter.im/audreyr/cookiecutter) account for logged chat, thanks to [@michaeljoseph](https://github.com/michaeljoseph).
* Added ReadTheDocs badge, thanks to [@michaeljoseph](https://github.com/michaeljoseph).
* Added AppVeyor badge, thanks to [@pydanny](https://github.com/pydanny)
* Documentation and PyPI trove classifier updates, thanks to [@thedrow](https://github.com/thedrow) (#323 and #324)

## 0.8.0 (2014-10-30)

The goal of this release was to allow for injection of extra context via the Cookiecutter API, and to fix minor bugs.

Features:

* cookiecutter() now takes an optional extra\_context parameter, thanks to [@michaeljoseph](https://github.com/michaeljoseph), [@fcurella](https://github.com/fcurella), [@aventurella](https://github.com/aventurella),  [@emonty](https://github.com/emonty), [@schacki](https://github.com/schacki), [@ryanolson](https://github.com/ryanolson), [@pfmoore](https://github.com/pfmoore), [@pydanny](https://github.com/pydanny), [@audreyfeldroy](https://github.com/audreyfeldroy) (#260).
* Context is now injected into hooks, thanks to [@michaeljoseph](https://github.com/michaeljoseph) and [@dinopetrone](https://github.com/dinopetrone).
* Moved all Python 2/3 compatibility code into cookiecutter.compat, making the eventual move to six easier, thanks to [@michaeljoseph](https://github.com/michaeljoseph) (#60, #102).
* Added cookiecutterrc defined aliases for cookiecutters, thanks to [@pfmoore](https://github.com/pfmoore) (#246)
* Added flake8 to tox to check for pep8 violations, thanks to [@natim](https://github.com/Natim).

Bug Fixes:

* Newlines at the end of files are no longer stripped, thanks to [@treyhunner](https://github.com/treyhunner) (#183).
* Cloning prompt suppressed by respecting the ```no\_input``` flag, thanks to [@trustrachel](https://github.com/trustrachel) (#285)
* With Python 3, input is no longer converted to bytes, thanks to [@uranusjr](https://github.com/uranusjr) (#98).

Other Changes:

* Added more Cookiecutters to the list:
  * [Python-iOS-template](https://github.com/pybee/Python-iOS-template) by [@freakboy3742](https://github.com/freakboy3742)
  * [Python-Android-template](https://github.com/pybee/Python-Android-template) by [@freakboy3742](https://github.com/freakboy3742)
  * [cookiecutter-djangocms-plugin](https://github.com/mishbahr/cookiecutter-djangocms-plugin) by [@mishbahr](https://github.com/mishbahr)
  * [cookiecutter-pyvanguard](https://github.com/robinandeer/cookiecutter-pyvanguard) by [@robinandeer](https://github.com/robinandeer)

## 0.7.2 (2014-08-05)

The goal of this release was to fix cross-platform compatibility, primarily Windows bugs that had crept in during the addition of new
features. As of this release, Windows is a first-class citizen again, now complete with continuous integration.

Bug Fixes:

* Fixed the contributing file so it displays nicely in Github, thanks to [@pydanny](https://github.com/pydanny).
* Updates 2.6 requirements to include simplejson, thanks to [@saxix](https://github.com/saxix).
* Avoid unwanted extra spaces in string literal, thanks to [@merwok](https://github.com/merwok).
* Fix @unittest.skipIf error on Python 2.6.
* Let sphinx parse :param: properly by inserting newlines #213, thanks to [@mineo](https://github.com/mineo).
* Fixed Windows test prompt failure by replacing stdin per [@cjrh](https://github.com/cjrh) in #195.
* Made rmtree remove readonly files, thanks to [@pfmoore](https://github.com/pfmoore).
* Now using tox to run tests on Appveyor, thanks to [@pfmoore](https://github.com/pfmoore) (#241).
* Fixed tests that assumed the system encoding was utf-8, thanks to [@pfmoore](https://github.com/pfmoore) (#242, #244).
* Added a tox ini file that uses py.test, thanks to [@pfmoore](https://github.com/pfmoore) (#245).

Other Changes:

* [@audreyfeldroy](https://github.com/audreyfeldroy) formally accepted position as **BDFL of cookiecutter**.
* Elevated [@pydanny](https://github.com/pydanny), [@michaeljoseph](https://github.com/michaeljoseph), and [@pfmoore](https://github.com/pfmoore) to core committer status.
* Added Core Committer guide, by [@audreyfeldroy](https://github.com/audreyfeldroy).
* Generated apidocs from make docs, by [@audreyfeldroy](https://github.com/audreyfeldroy).
* Added contributing command to the makedocs function, by [@pydanny](https://github.com/pydanny).
* Refactored contributing documentation, included adding core committer instructions, by [@pydanny](https://github.com/pydanny) and [@audreyfeldroy](https://github.com/audreyfeldroy).
* Do not convert input prompt to bytes, thanks to [@uranusjr](https://github.com/uranusjr) (#192).
* Added troubleshooting info about Python 3.3 tests and tox.
* Added documentation about command line arguments, thanks to [@saxix](https://github.com/saxix).
* Style cleanups.
* Added environment variable to disable network tests for environments without networking, thanks to [@vincentbernat](https://github.com/vincentbernat).
* Added Appveyor support to aid Windows integrations, thanks to [@pydanny](https://github.com/pydanny) (#215).
* CONTRIBUTING.rst is now generated via make contributing, thanks to [@pydanny](https://github.com/pydanny) (#220).
* Removed unnecessary endoing argument to json.load, thanks to [@pfmoore](https://github.com/pfmoore) (#234).
* Now generating shell hooks dynamically for Unix/Windows portability, thanks to [@pfmoore](https://github.com/pfmoore) (#236).
* Removed non-portable assumptions about directory structure, thanks to [@pfmoore](https://github.com/pfmoore) (#238).
* Added a note on portability to the hooks documentation, thanks to [@pfmoore](https://github.com/pfmoore) (#239).
* Replaced unicode\_open with direct use of io.open, thanks to [@pfmoore](https://github.com/pfmoore) (#229).
* Added more Cookiecutters to the list:
  * [cookiecutter-kivy](https://github.com/hackebrot/cookiecutter-kivy) by [@hackebrot](https://github.com/hackebrot)
  * [BoilerplatePP](https://github.com/Paspartout/BoilerplatePP) by [@Paspartout](https://github.com/Paspartout)
  * [cookiecutter-pypackage-minimal](https://github.com/kragniz/cookiecutter-pypackage-minimal) by [@borntyping](https://github.com/borntyping)
  * [cookiecutter-ansible-role](https://github.com/iknite/cookiecutter-ansible-role) by [@iknite](https://github.com/iknite)
  * [cookiecutter-pylibrary](https://github.com/ionelmc/cookiecutter-pylibrary) by [@ionelmc](https://github.com/ionelmc)
  * [cookiecutter-pylibrary-minimal](https://github.com/ionelmc/cookiecutter-pylibrary-minimal) by [@ionelmc](https://github.com/ionelmc)

## 0.7.1 (2014-04-26)

Bug fixes:

* Use the current Python interpreter to run Python hooks, thanks to [@coderanger](https://github.com/coderanger).
* Include tests and documentation in source distribution, thanks to [@vincentbernat](https://github.com/vincentbernat).
* Fix various warnings and missing things in the docs (#129, #130), thanks to [@nedbat](https://github.com/nedbat).
* Add command line option to get version (#89), thanks to [@davedash](https://github.com/davedash) and [@cyberj](https://github.com/cyberj).

Other changes:

* Add more Cookiecutters to the list:
  * [cookiecutter-avr](https://github.com/solarnz/cookiecutter-avr) by [@solarnz](https://github.com/solarnz)
  * [cookiecutter-tumblr-theme](https://github.com/relekang/cookiecutter-tumblr-theme) by [@relekang](https://github.com/relekang)
  * [cookiecutter-django-paas](https://github.com/pbacterio/cookiecutter-django-paas) by [@pbacterio](https://github.com/pbacterio)

## 0.7.0 (2013-11-09)

This is a release with significant improvements and changes. Please read through this list before you upgrade.

New features:

* Support for \--checkout argument, thanks to [@foobacca](https://github.com/foobacca/).
* Support for pre-generate and post-generate hooks, thanks to [@raphigaziano](https://github.com/raphigaziano/). Hooks are Python or shell scripts that run before and/or after your project is generated.
* Support for absolute paths to cookiecutters, thanks to [@krallin](https://github.com/krallin/).
* Support for Mercurial version control system, thanks to [@pokoli](https://github.com/pokoli/).
* When a cookiecutter contains invalid Jinja2 syntax, you get a better message that shows the location of the TemplateSyntaxError. Thanks
to [@benjixx](https://github.com/benjixx/).
* Can now prompt the user to enter values during generation from a local cookiecutter, thanks to [@ThomasChiroux](https://github.com/ThomasChiroux/). This is now always the default behavior. Prompts can also be suppressed with ```--no-input```.
* Your cloned cookiecutters are stored by default in your ~/.cookiecutters/ directory (or Windows equivalent). The location is configurable. (This is a major change from the pre-0.7.0 behavior, where cloned cookiecutters were deleted at the end of project generation.) Thanks [@raphigaziano](https://github.com/raphigaziano/).
* User config in a \~/.cookiecutterrc file, thanks to [@raphigaziano](https://github.com/raphigaziano/). Configurable settings are cookiecutters\_dir and default\_context.
* File permissions are now preserved during project generation, thanks to [@benjixx](https://github.com/benjixx/).

Bug fixes:

* Unicode issues with prompts and answers are fixed, thanks to [@s-m-i-t-a](https://github.com/s-m-i-t-a/).
* The test suite now runs on Windows, which was a major effort. Thanks to [@pydanny](https://github.com/pydanny), who collaborated on this with me.

Other changes:

* Quite a bit of refactoring and API changes.
* Lots of documentation improvements. Thanks [@sloria](https://github.com/sloria/), [@alex](https://github.com/alex/), [@pydanny](https://github.com/pydanny), [@freakboy3742](https://github.com/freakboy3742), [@es128](https://github.com/es128/), [@rolo](https://github.com/rolo/).
* Better naming and organization of test suite.
* A CookiecutterCleanSystemTestCase to use for unit tests affected by the user\'s config and cookiecutters directory.
* Improvements to the project\'s Makefile.
* Improvements to tests. Thanks [@gperetin](https://github.com/gperetin/), [@s-m-i-t-a](https://github.com/s-m-i-t-a/).
* Removal of subprocess32 dependency. Now using non-context manager version of subprocess.Popen for Python 2 compatibility.
* Removal of cookiecutter\'s cleanup module.
* A bit of setup.py cleanup, thanks to [@oubiga](https://github.com/oubiga/).
* Now depends on binaryornot 0.2.0.

## 0.6.4 (2013-08-21)

* Windows support officially added.
* Fix TemplateNotFound Exception on Windows (#37).

## 0.6.3 (2013-08-20)

* Fix copying of binary files in nested paths (#41), thanks to [@sloria](https://github.com/sloria/).

## 0.6.2 (2013-08-19)

* Depend on Jinja2\>=2.4 instead of Jinja2==2.7.
* Fix errors on attempt to render binary files. Copy them over from the project template without rendering.
* Fix Python 2.6/2.7 UnicodeDecodeError when values containing Unicode chars are in cookiecutter.json.
* Set encoding in Python 3 unicode_open() to always be utf-8.

## 0.6.1 (2013-08-12)

* Improved project template finding. Now looks for the occurrence of {{,cookiecutter, and }} in a directory name.
* Fix help message for input_dir arg at command prompt.
* Minor edge cases found and corrected, as a result of improved test coverage.

## 0.6.0 (2013-08-08)

* Config is now in a single ```cookiecutter.json``` instead of in ```json/```.
* When you create a project from a git repo template, Cookiecutter prompts you to enter custom values for the fields defined in ```cookiecutter.json```.

## 0.5 (2013-07-28)

* Friendlier, more simplified command line usage:

```bash
    # Create project from the cookiecutter-pypackage/ template
    $ cookiecutter cookiecutter-pypackage/
    # Create project from the cookiecutter-pypackage.git repo template
    $ cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage.git
```

* Can now use Cookiecutter from Python as a package:

```python
    from cookiecutter.main import cookiecutter

    # Create project from the cookiecutter-pypackage/ template
    cookiecutter('cookiecutter-pypackage/')

    # Create project from the cookiecutter-pypackage.git repo template
    cookiecutter('https://github.com/audreyfeldroy/cookiecutter-pypackage.git')
```

* Internal refactor to remove any code that changes the working
    directory.

## 0.4 (2013-07-22)

* Only takes in one argument now: the input directory. The output directory is generated by rendering the name of the input directory.
* Output directory cannot be the same as input directory.

## 0.3 (2013-07-17)

* Takes in command line args for the input and output directories.

## 0.2.1 (2013-07-17)

* Minor cleanup.

## 0.2 (2013-07-17)

Bumped to "Development Status :: 3 - Alpha".

* Works with any type of text file.
* Directory names and filenames can be templated.

## 0.1.0 (2013-07-11)

* First release on PyPI.
