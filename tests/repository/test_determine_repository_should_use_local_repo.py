# -*- coding: utf-8 -*-
from cookiecutter.repository import determine_repo_dir


def test_determine_repository_should_use_local_repo():
    project_dir = determine_repo_dir(
        'tests/fake-repo',
        abbreviations={},
        clone_to_dir=None,
        checkout=None,
        no_input=True
    )

    assert 'tests/fake-repo' == project_dir
