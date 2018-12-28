# -*- coding: utf-8 -*-

"""
test_cookie_pick
----------------
"""

import os
import pytest

from git.exc import GitCommandError, NoSuchPathError
from jinja2 import FileSystemLoader

from cookiecutter.cookie_pick import (
    generate_cookie_pick,
    get_target_directory,
    show_commits
)
from cookiecutter.environment import StrictEnvironment


@pytest.fixture(params=['fake-repo-pre', 'fake-repo-pre2'])
def repo_dir(request):
    return os.path.join('tests', request.param)


@pytest.fixture
def output_dir(tmpdir):
    return str(tmpdir.mkdir('output'))


@pytest.fixture
def env():
    environment = StrictEnvironment()
    environment.loader = FileSystemLoader('.')
    return environment


@pytest.fixture
def context():
    return {'cookiecutter': {'repo_name': 'repo'}}


@pytest.fixture
def commits(mocker):
    commits = [
        mocker.Mock(hexsha=str(idx))
        for idx in range(3)
    ]
    for idx, commit in enumerate(commits):
        commit.parents = commits[idx + 1:]
    return commits


def test_show_commits(mocker, commits):
    """Show commits calls the repository and sends info to the logger"""
    repo_mock = mocker.patch('cookiecutter.cookie_pick.Repo')
    repo_mock.return_value.iter_commits.return_value = commits
    info_mock = mocker.patch('cookiecutter.cookie_pick.logger.info')

    repo = repo_mock()
    show_commits(repo)

    assert repo.iter_commits.called
    assert info_mock.call_count == len(commits) + 1


def test_get_target_directory(repo_dir, context, output_dir, env):
    target_dir = get_target_directory(
        repo_dir,
        context,
        output_dir,
        env
    )

    assert target_dir == os.path.join(output_dir, 'repo')


def test_cookie_pick_list(mocker, repo_dir, context, output_dir, commits):
    repo_mock = mocker.patch('cookiecutter.cookie_pick.Repo')
    repo_mock.return_value.iter_commits.return_value = commits
    info_mock = mocker.patch('cookiecutter.cookie_pick.logger.info')

    generate_cookie_pick(
        repo_dir,
        context=context,
        output_dir=output_dir,
        cookie_pick='list',
        cookie_pick_parent=None
    )

    assert info_mock.called
    assert info_mock.call_count == len(commits) + 1


def test_cookie_pick_single_diff(
        mocker, repo_dir, context, output_dir, commits):
    repo_mock = mocker.patch('cookiecutter.cookie_pick.Repo')
    repo_mock.return_value.iter_commits.return_value = commits
    repo_mock.return_value.commit.side_effect = commits
    repo_mock.return_value.git.diff.return_value = \
        '+Repository: {{ cookiecutter.repo_name }}'
    mocker.patch('cookiecutter.cookie_pick.logger.info')
    try:
        mocker.patch('cookiecutter.cookie_pick.open', mocker.mock_open())
    except AttributeError:
        mocker.patch('builtins.open', mocker.mock_open())
    remove_mock = mocker.patch('cookiecutter.cookie_pick.os.remove')

    generate_cookie_pick(
        repo_dir,
        context=context,
        output_dir=output_dir,
        cookie_pick='0',
        cookie_pick_parent=None
    )

    assert repo_mock.called
    repo_mock.assert_has_calls([
        mocker.call(repo_dir),
        mocker.call().commit('0'),
        mocker.call().git.diff(['1', '0', '--no-color', '-p']),
        mocker.call(os.path.join(output_dir, 'repo')),
        mocker.call().git.apply(
            ['-p2', '--reject', '--whitespace=fix', 'cookiecutter_0_1.patch'])
    ])
    remove_mock.assert_called_with(
        os.path.join(output_dir, 'repo', 'cookiecutter_0_1.patch'))


def test_cookie_pick_parent_diff(
        mocker, repo_dir, context, output_dir, commits):
    repo_mock = mocker.patch('cookiecutter.cookie_pick.Repo')
    repo_mock.return_value.iter_commits.return_value = commits
    repo_mock.return_value.commit.side_effect = [commits[0], commits[2]]
    repo_mock.return_value.git.diff.return_value = \
        '+Repository: {{ cookiecutter.repo_name }}'
    mocker.patch('cookiecutter.cookie_pick.logger.info')
    try:
        mocker.patch('cookiecutter.cookie_pick.open', mocker.mock_open())
    except AttributeError:
        mocker.patch('builtins.open', mocker.mock_open())
    remove_mock = mocker.patch('cookiecutter.cookie_pick.os.remove')

    generate_cookie_pick(
        repo_dir,
        context=context,
        output_dir=output_dir,
        cookie_pick='0',
        cookie_pick_parent='2'
    )

    assert repo_mock.called
    repo_mock.assert_has_calls([
        mocker.call(repo_dir),
        mocker.call().commit('0'),
        mocker.call().commit('2'),
        mocker.call().git.diff(['2', '0', '--no-color', '-p']),
        mocker.call(os.path.join(output_dir, 'repo')),
        mocker.call().git.apply(
            ['-p2', '--reject', '--whitespace=fix', 'cookiecutter_0_2.patch'])
    ])
    remove_mock.assert_called_with(
        os.path.join(output_dir, 'repo', 'cookiecutter_0_2.patch'))


def test_cookie_pick_apply_error(
        mocker, repo_dir, context, output_dir, commits):
    repo_mock = mocker.patch('cookiecutter.cookie_pick.Repo')
    repo_mock.return_value.iter_commits.return_value = commits
    repo_mock.return_value.commit.side_effect = [commits[0], commits[2]]
    repo_mock.return_value.git.diff.return_value = \
        '+Repository: {{ cookiecutter.repo_name }}'
    repo_mock.return_value.git.apply.side_effect = GitCommandError('apply', 1)

    mocker.patch('cookiecutter.cookie_pick.logger.info')
    try:
        mocker.patch('cookiecutter.cookie_pick.open', mocker.mock_open())
    except AttributeError:
        mocker.patch('builtins.open', mocker.mock_open())
    remove_mock = mocker.patch('cookiecutter.cookie_pick.os.remove')

    with pytest.raises(GitCommandError):
        generate_cookie_pick(
            repo_dir,
            context=context,
            output_dir=output_dir,
            cookie_pick='0',
            cookie_pick_parent='2'
        )

    assert repo_mock.called
    repo_mock.assert_has_calls([
        mocker.call(repo_dir),
        mocker.call().commit('0'),
        mocker.call().commit('2'),
        mocker.call().git.diff(['2', '0', '--no-color', '-p']),
        mocker.call(os.path.join(output_dir, 'repo')),
        mocker.call().git.apply(
            ['-p2', '--reject', '--whitespace=fix', 'cookiecutter_0_2.patch'])
    ])
    remove_mock.assert_called_with(
        os.path.join(output_dir, 'repo', 'cookiecutter_0_2.patch'))


def test_cookie_pick_target_dir_error(
        mocker, repo_dir, context, output_dir, commits):
    repo_mock = mocker.patch('cookiecutter.cookie_pick.Repo')
    source_repo_mock = mocker.MagicMock()
    source_repo_mock.iter_commits.return_value = commits
    source_repo_mock.commit.side_effect = commits
    source_repo_mock.git.diff.return_value = \
        '+Repository: {{ cookiecutter.repo_name }}'
    source_repo_mock.git.apply.side_effect = GitCommandError('apply', 1)
    repo_mock.side_effect = [source_repo_mock, NoSuchPathError]

    mocker.patch('cookiecutter.cookie_pick.logger.info')
    try:
        mocker.patch('cookiecutter.cookie_pick.open', mocker.mock_open())
    except AttributeError:
        mocker.patch('builtins.open', mocker.mock_open())
    remove_mock = mocker.patch('cookiecutter.cookie_pick.os.remove')

    with pytest.raises(NoSuchPathError):
        generate_cookie_pick(
            repo_dir,
            context=context,
            output_dir=output_dir,
            cookie_pick='0',
            cookie_pick_parent=None
        )

    assert repo_mock.called
    repo_mock.assert_has_calls([
        mocker.call(repo_dir),
        mocker.call(os.path.join(output_dir, 'repo'))
    ])
    assert not remove_mock.called
