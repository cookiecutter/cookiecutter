"""Tests for cookiecutter.env() Jinja extension (issue #2045).

The env() global is exposed by EnvExtension. It lets users reference
environment variables inside ``cookiecutter.json`` and template strings,
e.g.::

    {
        "author_name": "{{ env('USER', 'Default Name') }}",
        "author_email": "{{ env('EMAIL') }}"
    }

These are evaluated by the same render path that already handles things
like ``{{ cookiecutter.project_name.lower() }}`` in cookiecutter.json
— see ``cookiecutter.prompt.render_variable``.
"""

from pathlib import Path

import pytest

from cookiecutter import generate
from cookiecutter.prompt import render_variable
from cookiecutter.utils import create_env_with_context


@pytest.fixture
def template_dir(tmp_path):
    """Minimal template that uses cookiecutter's two-stage rendering.

    Stage 1: context values are rendered (e.g. {{ env('USER') }})
    Stage 2: template files reference context values
    """
    project = tmp_path / "{{cookiecutter.project_name}}"
    project.mkdir()
    (project / "README.rst").write_text(
        "{{ cookiecutter.project_name }} — "
        "{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>"
    )
    return tmp_path


def _build_context():
    """Render context values the way cookiecutter does after prompts.

    Cookiecutter's prompt flow goes through ``cookiecutter.prompt.render_variable``
    for every value coming out of cookiecutter.json, which renders each value
    in the Jinja environment. We simulate that here so the test exercises
    the same code path that real users hit.
    """
    raw = {
        "project_name": "Hello",
        "author_name": "{{ env('TEST_AUTHOR', 'Default Name') }}",
        "author_email": "{{ env('TEST_EMAIL') }}",
    }
    env = create_env_with_context({"cookiecutter": raw})
    return {k: render_variable(env, v, raw) for k, v in raw.items()}


def test_env_returns_value_when_set(template_dir, monkeypatch):
    monkeypatch.setenv("TEST_AUTHOR", "Rachel")
    monkeypatch.setenv("TEST_EMAIL", "rachel@example.com")
    out = template_dir / "out1"
    ctx = _build_context()
    project_dir = generate.generate_files(
        context={"cookiecutter": ctx},
        repo_dir=str(template_dir),
        output_dir=str(out),
        overwrite_if_exists=True,
    )
    readme = (Path(project_dir) / "README.rst").read_text()
    assert "Rachel" in readme
    assert "rachel@example.com" in readme


def test_env_returns_default_when_unset(template_dir, monkeypatch):
    monkeypatch.delenv("TEST_AUTHOR", raising=False)
    monkeypatch.delenv("TEST_EMAIL", raising=False)
    out = template_dir / "out2"
    ctx = _build_context()
    project_dir = generate.generate_files(
        context={"cookiecutter": ctx},
        repo_dir=str(template_dir),
        output_dir=str(out),
        overwrite_if_exists=True,
    )
    readme = (Path(project_dir) / "README.rst").read_text()
    assert "Default Name" in readme
    assert "<None>" in readme


def test_env_empty_string_is_returned_not_treated_as_unset(template_dir, monkeypatch):
    monkeypatch.setenv("TEST_AUTHOR", "")
    monkeypatch.delenv("TEST_EMAIL", raising=False)
    out = template_dir / "out3"
    ctx = _build_context()
    project_dir = generate.generate_files(
        context={"cookiecutter": ctx},
        repo_dir=str(template_dir),
        output_dir=str(out),
        overwrite_if_exists=True,
    )
    readme = (Path(project_dir) / "README.rst").read_text()
    # Empty string is returned, not None, not "Default Name"
    assert "—  <" in readme
    assert "Default Name" not in readme


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
