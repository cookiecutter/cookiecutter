## Cookiecutter 2.7.1: The One Where It Knows Its Own Name

You know that thing where you release an album, it's on the shelves, people are buying it, and then someone points out the spine says it's your previous album? That's what happened with Cookiecutter 2.7.0. We put out the long-awaited release with 27 improvements and 17 contributors, and `cookiecutter -V` proudly announced: **2.6.0**.

```
$ cookiecutter -V
Cookiecutter 2.6.0

$ # narrator voice: it was not 2.6.0
```

Go on, run this and see for yourself that the 2.7.1 release knows its own version number now:

```bash
uv tool upgrade cookiecutter
```

### What's fixed

**`cookiecutter -V` now reports the real version.** Rather than patch `VERSION.txt`, this release removes it entirely. The version is now read from package metadata at runtime, so `pyproject.toml` is the single source of truth and there's nothing left to drift. Thanks [@bollwyvl](https://github.com/bollwyvl) for the bug report PR and for suggesting the `importlib.metadata` approach, and thanks [@tranzystorekk](https://github.com/tranzystorekk) for filing [#2195](https://github.com/cookiecutter/cookiecutter/issues/2195)!

### What's better

**CI runs each Python version as its own job.** Tests for 3.10 through 3.14 used to run sequentially inside a single job per OS, which pushed Windows past 30 minutes. Each version now runs in parallel with a 15-minute timeout. Windows tests focus on the boundary versions (3.10 and 3.14) since intermediate versions add little signal beyond Ubuntu and macOS.

### Contributors

[@audreyfeldroy](https://audrey.feldroy.com) (Audrey M. Roy Greenfeld) and [@pydanny](https://daniel.feldroy.com) (Daniel Roy Greenfeld) built this release, with help from Claude roleplaying as David Bowie.

Thanks to [@bollwyvl](https://github.com/bollwyvl) (Nicholas Bollweg) for the version fix PR and the `importlib.metadata` suggestion, and [@tranzystorekk](https://github.com/tranzystorekk) for reporting the version mismatch.
