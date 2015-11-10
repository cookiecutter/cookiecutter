# -*- coding: utf-8 -*-

import pytest

from cookiecutter import generate
from cookiecutter import exceptions


@pytest.mark.usefixtures('clean_system')
def test_pre_gen_hook(tmpdir):
    context = {
        'cookiecutter': {
            "repo_dir": "foobar",
            "abort_pre_gen": "yes",
            "abort_post_gen": "no"
        }
    }

    with pytest.raises(exceptions.FailedHookException):
        generate.generate_files(
            repo_dir='tests/hooks-abort-render',
            context=context,
            output_dir=str(tmpdir)
        )

    assert not tmpdir.join('foobar').isdir()


@pytest.mark.usefixtures('clean_system')
def test_post_gen_hook(tmpdir):
    context = {
        'cookiecutter': {
            "repo_dir": "foobar",
            "abort_pre_gen": "no",
            "abort_post_gen": "yes"
        }
    }

    with pytest.raises(exceptions.FailedHookException):
        generate.generate_files(
            repo_dir='tests/hooks-abort-render',
            context=context,
            output_dir=str(tmpdir)
        )

    assert not tmpdir.join('foobar').isdir()
