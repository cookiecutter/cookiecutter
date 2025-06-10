# How to contribute

## Dependencies

First of all, you need to install `python3.8` or higher. We recommend create a new [conda](https://docs.conda.io/en/latest/) and python3.10 for this project.

Create your conda environment, and then activate it:

```bash
conda create -n python-project python=3.10
conda activate python-project
```

We use `poetry` to manage the [dependencies](https://github.com/python-poetry/poetry).
If you don't have `poetry`, you should install with `pip install poetry`.

To install dependencies and prepare [`pre-commit`](https://pre-commit.com/) hooks you would need to run `install` command:

```bash
make install
make pre-commit-install
```

## Codestyle

After installation you may execute code formatting. We use [ruff](https://github.com/astral-sh/ruff) to format our code.

```bash
make format
```

### Checks

Many checks are configured for this project. Command `make check-codestyle` will check using ruff.

Command `make lint` applies all checks.

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
1. Add tests for the new changes
1. Edit documentation if you have changed something significant
1. Run `make format` to format your changes.
1. Run `make lint` to ensure that types, security and docstrings are okay.

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
