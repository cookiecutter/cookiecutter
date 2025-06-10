# Guide for python_project, the owners of the repository 😀

**👉 You can delete this file after reading and operating the instructions.**

## 1. Very first steps

### 1.1. Initialize your code

1. Initialize `git` inside your repo:

```bash
cd python-project && git init
```

2. If you don't have `Poetry`. 

Conda environment is is recommended.

```bash
conda create -n python-project python==3.10
```

Please activate python of current project and install run:

```bash
conda activate python-project
pip install poetry
```

3. Initialize poetry and `pre-commit` hooks:

```bash
make install
```

If you obtain a timeout error when installing, you can try to append an image source config in `poetry.toml`. The following example is tsinghua image source.

```toml
[[tool.poetry.source]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
priority = "default"
```

4. Run the codestyle to polish your code:

```bash
make format
```

5. Upload initial code to GitHub:

```bash
git add .
git commit -m ":tada: Initial commit"
git branch -M main
git remote add origin https://github.com/python_project/python-project.git
git push -u origin main
```

### 1.2. Set up bots

When you create this repository, you have already set up the following bots, so that you can use it in relevant GitHub repository.

- [Dependabot](https://docs.github.com/en/github/administering-a-repository/enabling-and-disabling-version-updates#enabling-github-dependabot-version-updates): will create a pull request to update the dependencies. You can also enable it to automatically merge the pull request after the CI/CD passes. You can configure it in `.github/dependabot.yml`.
- [Stale bot](https://github.com/apps/stale): Automatically closes abandoned issues after a period of inactivity. You can configure it in `.github/.stale.yml`.
- [first-interaction](./.github/workflows/greetings.yml): will comment on the first issue or pull request from a new contributor. You can configure it in `.github/workflows/greetings.yml`.

> ❗ **first-interaction** requires `pull_requests:write`, but by default `GITHUB_TOKEN` has this value set to read-only. You need to do the following to enable it:
> - Go to the repository settings
> - Open the "Actions" tab
> - Click on "Read and write permissions" and enable "Actions: Read and write permissions"
> ![img.png](assets/images/img_1.png)


### 1.3. Poetry

This project use Poetry to manage dependencies. Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. 

Want to know more about Poetry? Check [its documentation](https://python-poetry.org/docs/).

<details>
<summary>Details about Poetry</summary>
<p>

Poetry's [commands](https://python-poetry.org/docs/cli/#commands) are very intuitive and easy to learn, like:

- `poetry add numpy@latest` add a new dependency.
- `poetry run pytest` run tests.
- `poetry publish --build` publish your package.

etc
</p>
</details>

### 1.4. Building and releasing your package (Optional)

You can build and release your package to PyPI. Building a new version of the application contains steps:

- Bump the version of your package `poetry version <version>`. You can pass the new version explicitly, or a rule such as `major`, `minor`, or `patch`. For more details, refer to the [Semantic Versions](https://semver.org/) standard.
- Make a commit to `GitHub`.
- Create a `GitHub release`.
- And... publish 🙂 `poetry publish --build`

## 🎯 2. What's next

Well, that's up to you 💪🏻. I can only recommend the packages and articles that helped me.

- [`Typer`](https://github.com/tiangolo/typer) is great for creating CLI applications.
- [`Rich`](https://github.com/willmcgugan/rich) makes it easy to add beautiful formatting in the terminal.
- [`Pydantic`](https://github.com/samuelcolvin/pydantic/) – data validation and settings management using Python type hinting.
- [`Loguru`](https://github.com/Delgan/loguru) makes logging (stupidly) simple.
- [`tqdm`](https://github.com/tqdm/tqdm) – fast, extensible progress bar for Python and CLI.
- [`IceCream`](https://github.com/gruns/icecream) is a little library for sweet and creamy debugging.
- [`orjson`](https://github.com/ijl/orjson) – ultra fast JSON parsing library.
- [`Returns`](https://github.com/dry-python/returns) makes you function's output meaningful, typed, and safe!
- [`Hydra`](https://github.com/facebookresearch/hydra) is a framework for elegantly configuring complex applications.
- [`FastAPI`](https://github.com/tiangolo/fastapi) is a type-driven asynchronous web framework.

Articles:

- [Open Source Guides](https://opensource.guide/).
- [A handy guide to financial support for open source](https://github.com/nayafia/lemonade-stand)
- [GitHub Actions Documentation](https://help.github.com/en/actions).
- Maybe you would like to add [gitmoji](https://gitmoji.carloscuesta.me/) to commit names. This is really funny. 😄

## 🚀 3. Features

### 3.1. Development features

- Supports for `Python 3.8` and higher.
- [`Poetry`](https://python-poetry.org/) as the dependencies manager. See configuration in [`pyproject.toml`](https://github.com/python_project/python-project/blob/main/pyproject.toml) and [`setup.cfg`](https://github.com/python_project/python-project/blob/main/setup.cfg).
- Faster formatter tool, automatic codestyle with [`ruff`](https://github.com/astral-sh/ruff) to replace [`black`](https://github.com/psf/black), [`isort`](https://github.com/timothycrosley/isort) and [`pyupgrade`](https://github.com/asottile/pyupgrade).
- Ready-to-use [`pre-commit`](https://pre-commit.com/) hooks with code-formatting.
- Type checks with  [`ruff`](https://github.com/astral-sh/ruff); docstring checks with [`darglint`](https://github.com/terrencepreilly/darglint); security checks with [`safety`](https://github.com/pyupio/safety) and [`bandit`](https://github.com/PyCQA/bandit)
- Testing with [`pytest`](https://docs.pytest.org/en/latest/).
- Ready-to-use [`.editorconfig`](https://github.com/python_project/python-project/blob/main/.editorconfig), [`.dockerignore`](https://github.com/python_project/python-project/blob/main/.dockerignore), and [`.gitignore`](https://github.com/python_project/python-project/blob/main/.gitignore). You don't have to worry about those things.

### 3.2. Deployment features

- `GitHub` integration: issue and pr templates.
- `Github Actions` with predefined [build workflow](https://github.com/python_project/python-project/blob/main/.github/workflows/build.yml) as the default CI/CD.
- Everything is already set up for security checks, codestyle checks, code formatting, testing, linting, docker builds, etc with [`Makefile`](https://github.com/python_project/python-project/blob/main/Makefile#L89). More details in [makefile-usage](#makefile-usage).
- [Dockerfile](https://github.com/python_project/python-project/blob/main/docker/Dockerfile) for your package.
- Always up-to-date dependencies with [`@dependabot`](https://dependabot.com/). You will only [enable it](https://docs.github.com/en/github/administering-a-repository/enabling-and-disabling-version-updates#enabling-github-dependabot-version-updates).
- Automatic drafts of new releases with [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). You may see the list of labels in [`release-drafter.yml`](https://github.com/python_project/python-project/blob/main/.github/release-drafter.yml). Works perfectly with [Semantic Versions](https://semver.org/) specification.

### 3.3. Open source community features

- Ready-to-use [Pull Requests templates](https://github.com/python_project/python-project/blob/main/.github/PULL_REQUEST_TEMPLATE.md) and several [Issue templates](https://github.com/python_project/python-project/tree/main/.github/ISSUE_TEMPLATE).
- Files such as: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` are generated automatically.
- [`Stale bot`](https://github.com/apps/stale) that closes abandoned issues after a period of inactivity. (You will only [need to setup free plan](https://github.com/marketplace/stale)). Configuration is [here](https://github.com/python_project/python-project/blob/main/.github/.stale.yml).
- [Semantic Versions](https://semver.org/) specification with [`Release Drafter`](https://github.com/marketplace/actions/release-drafter).


## 📈 4. Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/python_project/python-project/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/python_project/python-project/blob/main/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.


**👉 Remember delete this file after reading and operating the instructions.**
