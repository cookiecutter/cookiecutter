"""Tests around locally cached cookiecutter template repositories."""

from pathlib import Path

import pytest

from cookiecutter import exceptions, repository


@pytest.fixture
def template() -> str:
    """Fixture. Return simple string as template name."""
    return 'cookiecutter-pytest-plugin'


@pytest.fixture
def cloned_cookiecutter_path(user_config_data, template) -> Path:
    """Fixture. Prepare folder structure for tests in this file."""
    cookiecutters_dir = Path(user_config_data['cookiecutters_dir'])

    cloned_template_path = cookiecutters_dir / template
    if not cloned_template_path.exists():
        cloned_template_path.mkdir()  # might exist from other tests.

    subdir_template_path = cloned_template_path / 'my-dir'
    if not subdir_template_path.exists():
        subdir_template_path.mkdir()
    (subdir_template_path / 'cookiecutter.json').touch()  # creates file

    return subdir_template_path  # type: ignore[no-any-return]


def test_should_find_existing_cookiecutter(
    template, user_config_data, cloned_cookiecutter_path
) -> None:
    """Find `cookiecutter.json` in sub folder created by `cloned_cookiecutter_path`."""
    project_dir, cleanup = repository.determine_repo_dir(
        template=template,
        abbreviations={},
        clone_to_dir=user_config_data['cookiecutters_dir'],
        checkout=None,
        no_input=True,
        directory='my-dir',
    )

    assert str(cloned_cookiecutter_path) == project_dir
    assert not cleanup


def test_local_repo_typo(template, user_config_data, cloned_cookiecutter_path) -> None:
    """Wrong pointing to `cookiecutter.json` sub-directory should raise."""
    with pytest.raises(exceptions.RepositoryNotFound) as err:
        repository.determine_repo_dir(
            template=template,
            abbreviations={},
            clone_to_dir=user_config_data['cookiecutters_dir'],
            checkout=None,
            no_input=True,
            directory='wrong-dir',
        )

    wrong_full_cookiecutter_path = cloned_cookiecutter_path.parent / 'wrong-dir'
    assert str(err.value) == (
        f'A valid repository for "{template}" could not be found in the following '
        'locations:\n'
        f'{Path(template, "wrong-dir")}\n'
        f'{wrong_full_cookiecutter_path}'
    )
