# -*- coding: utf-8 -*-

"""Testing invalid cookiecutter template repositories."""

import pytest

from cookiecutter import main, exceptions


def test_should_raise_error_if_repo_does_not_exist():
    with pytest.raises(exceptions.RepositoryNotFound):
        main.cookiecutter('definitely-not-a-valid-repo-dir')
