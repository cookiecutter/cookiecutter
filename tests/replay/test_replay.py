# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""

import os
import pytest

from cookiecutter import replay, main, exceptions


def test_get_replay_file_name():
    """Make sure that replay.get_file_name generates a valid json file path."""
    exp_replay_file_name = os.path.join('foo', 'bar.json')
    assert replay.get_file_name('foo', 'bar') == exp_replay_file_name


@pytest.fixture(params=[
    {'no_input': True},
    {'extra_context': {}},
    {'no_input': True, 'extra_context': {}},
])
def invalid_kwargs(request):
    return request.param


def test_raise_on_invalid_mode(invalid_kwargs):
    with pytest.raises(exceptions.InvalidModeException):
        main.cookiecutter('foo', replay=True, **invalid_kwargs)


def test_main_does_not_invoke_dump_but_load(mocker):
    mock_prompt = mocker.patch('cookiecutter.main.prompt_for_config')
    mock_gen_context = mocker.patch('cookiecutter.main.generate_context')
    mock_gen_files = mocker.patch('cookiecutter.main.generate_files')
    mock_replay_dump = mocker.patch('cookiecutter.main.dump')
    mock_replay_load = mocker.patch('cookiecutter.main.load')

    main.cookiecutter('foobar', replay=True)

    assert not mock_prompt.called
    assert not mock_gen_context.called
    assert not mock_replay_dump.called
    assert mock_replay_load.called
    assert mock_gen_files.called


def test_main_does_not_invoke_load_but_dump(mocker):
    mock_prompt = mocker.patch('cookiecutter.main.prompt_for_config')
    mock_gen_context = mocker.patch('cookiecutter.main.generate_context')
    mock_gen_files = mocker.patch('cookiecutter.main.generate_files')
    mock_replay_dump = mocker.patch('cookiecutter.main.dump')
    mock_replay_load = mocker.patch('cookiecutter.main.load')

    main.cookiecutter('foobar', replay=False)

    assert mock_prompt.called
    assert mock_gen_context.called
    assert mock_replay_dump.called
    assert not mock_replay_load.called
    assert mock_gen_files.called
