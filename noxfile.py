"""Nox tool configuration file.

Nox is Tox tool replacement.
"""
import shutil
from pathlib import Path

import nox

nox.options.keywords = "not docs"


def base_install(session):
    """Create basic environment setup for tests and linting."""
    session.install("-r", "test_requirements.txt")
    session.install("-e", ".")
    return session


@nox.session(python="3.10")
def lint(session):
    """Run linting check locally."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def tests(session):
    """Run test suite with pytest."""
    session = base_install(session)
    session.run(
        "pytest",
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-branch",
        "--cov-fail-under=100",
    )


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def safety_tests(session):
    """Run safety tests."""
    session = base_install(session)
    session.run("safety", "check", "--full-report")


@nox.session(python="3.10")
def documentation_tests(session):
    """Run documentation tests."""
    return docs(session, batch_run=True)


@nox.session(python="3.10")
def docs(session, batch_run: bool = False):
    """Build the documentation or serve documentation interactively."""
    shutil.rmtree(Path("docs").joinpath("_build"), ignore_errors=True)
    session.install("-r", "docs/requirements.txt")
    session.install("-e", ".")
    session.cd("docs")
    sphinx_args = ["-b", "html", "-W", ".", "_build/html"]

    if not session.interactive or batch_run:
        sphinx_cmd = "sphinx-build"
    else:
        sphinx_cmd = "sphinx-autobuild"
        sphinx_args.extend(
            [
                "--open-browser",
                "--port",
                "9812",
                "--watch",
                "../*.md",
                "--watch",
                "../*.rst",
                "--watch",
                "../*.py",
                "--watch",
                "../cookiecutter",
            ]
        )

    session.run(sphinx_cmd, *sphinx_args)
