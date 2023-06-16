"""Nox tool configuration file.

Nox is Tox tool replacement.
"""

import os
import shutil
import sys
from pathlib import Path

import nox

nox.options.keywords = "not docs"


# At the time of writing, nox on Windows cannot reliably find installed Python versions,
# nor can it distinguish between PyPy and CPython versions.
#
# As a workaround, the following code attempts to find CPython versions
# in their default install locations.
target_python_versions = ["3.7", "3.8", "3.9", "3.10", "3.11"]
pythons = []
default_python_version = "3.10"
if not sys.platform.lower().startswith("win"):
    pythons = target_python_versions
else:
    for version in target_python_versions:
        stripped_version = version.replace(".", "")

        # Prefer 64-bit versions.
        path = Path(os.environ["PROGRAMFILES"]) / f"Python{stripped_version}/python.exe"
        if path.is_file():
            pythons.append(str(path))
            if version == default_python_version:
                default_python_version = str(path)
            continue

        # Allow 32-bit versions.
        path_x86 = (
            Path(os.environ["PROGRAMFILES(x86)"])
            / f"Python{stripped_version}/python.exe"
        )
        if path_x86.is_file():
            pythons.append(str(path))
            if version == default_python_version:
                default_python_version = str(path)
            continue

        # Fallback to whatever version nox can find.
        pythons.append(version)


def base_install(session):
    """Create basic environment setup for tests and linting."""
    session.install("-r", "test_requirements.txt")
    session.install("-e", ".")
    return session


@nox.session(python=default_python_version)
def lint(session):
    """Run linting check locally."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session(python=pythons)
def tests(session):
    """Run test suite with pytest."""
    session = base_install(session)
    posargs = session.posargs or ""
    session.run(
        "pytest",
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-branch",
        "--cov-fail-under=100",
        *posargs,
    )


@nox.session(python=pythons)
def safety_tests(session):
    """Run safety tests."""
    session = base_install(session)
    session.run("safety", "check", "--full-report")


@nox.session(python=default_python_version)
def documentation_tests(session):
    """Run documentation tests."""
    return docs(session, batch_run=True)


@nox.session(python=default_python_version)
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
