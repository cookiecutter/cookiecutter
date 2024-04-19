"""Test main cookiecutter invocation with user input enabled (mocked)."""

from pathlib import Path

import pytest

from cookiecutter import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs():
    """Remove special directories which are created during the tests."""
    yield
    for p in {'fake-project', 'fake-project-input-extra'}:
        if Path(p).is_dir():
            utils.rmtree(p)


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_local_with_input(monkeypatch) -> None:
    """Verify simple cookiecutter run results, without extra_context provided."""
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda _var, default, _prompts, _prefix: default,
    )
    main.cookiecutter('tests/fake-repo-pre/', no_input=False)
    assert Path('tests/fake-repo-pre/{{cookiecutter.repo_name}}').is_dir()
    assert not Path('tests/fake-repo-pre/fake-project').is_dir()
    assert Path('fake-project').is_dir()
    assert Path('fake-project/README.rst').is_file()
    assert not Path('fake-project/json/').exists()


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_input_extra_context(monkeypatch) -> None:
    """Verify simple cookiecutter run results, with extra_context provided."""
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda _var, default, _prompts, _prefix: default,
    )
    main.cookiecutter(
        'tests/fake-repo-pre',
        no_input=False,
        extra_context={'repo_name': 'fake-project-input-extra'},
    )
    assert Path('fake-project-input-extra').is_dir()
