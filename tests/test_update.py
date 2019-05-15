# -*- coding: utf-8 -*-

"""
test_generate_update
---------------------------------
"""

from __future__ import unicode_literals
import logging
import os
import pytest
import git
import tempfile
import shutil

from cookiecutter.main import cookiecutter
from cookiecutter import generate, exceptions, utils
from cookiecutter.update import DEFAULT_CK_BRANCH


@pytest.fixture(scope='function')
def remove_test_dir(request):
    """
    Remove the folder that is created by the test.
    """
    def fin_remove_test_dir():
        if os.path.exists('test_update'):
            utils.rmtree('test_update')
    request.addfinalizer(fin_remove_test_dir)


@pytest.fixture(scope='function')
def create_test_dir(request):
    """
    Create an test directory updated
    """
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_update',
                'render_test': 'I have been rendered!',
                '_copy_without_render': [
                    '*not-rendered',
                    'rendered/not_rendered.yml',
                    '*.txt',
                ]}
        },
        repo_dir='tests/test-update')
    shutil.copyfile('tests/test-update/cookiecutter.json',
                    'test_update/.cookiecutter.json')

    git_repo = git.Repo.init('test_update')
    git_repo.git.add("-A")
    git_repo.git.commit("-m", "Initial Commit")
    git_repo.git.branch(DEFAULT_CK_BRANCH)


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_update_empty():
    repo_dir = 'tests/test-update/'

    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_update',
                'render_test': 'I have been rendered!',
                '_copy_without_render': [
                    '*not-rendered',
                    'rendered/not_rendered.yml',
                    '*.txt',
                ]}
        },
        repo_dir=repo_dir)
    shutil.copyfile('tests/test-update/cookiecutter.json',
                    'test_update/.cookiecutter.json')

    with pytest.raises(exceptions.InvalidGitRepository):
        cookiecutter(repo_dir, no_input=True, update_dir='test_update')

    git.Repo.init('test_update')

    with pytest.raises(exceptions.RepositoryNoCKBranch):
        cookiecutter(repo_dir, no_input=True, update_dir='test_update')


@pytest.mark.usefixtures('create_test_dir', 'clean_system', 'remove_test_dir')
def test_dirty_project():
    """
    If the project contains untracked files or staged/unstaged files, abort
    """
    repo_dir = 'tests/test-update/'

    open('test_update/foo', 'a').close()
    with pytest.raises(exceptions.RepositoryNotCleanError):
        cookiecutter(repo_dir, no_input=True, update_dir='test_update')


@pytest.mark.usefixtures('create_test_dir', 'clean_system', 'remove_test_dir')
def test_already_last_update():
    repo_dir = 'tests/test-update/'

    cookiecutter(repo_dir, no_input=True, update_dir='test_update')


@pytest.mark.usefixtures('create_test_dir', 'clean_system', 'remove_test_dir')
def test_new_added_files():
    repo_dir = 'tests/test-update/'

    # Create new file
    new_file = 'new_file.txt'
    with open(repo_dir + "{{cookiecutter.repo_name}}/" + new_file, 'w+') as f:
        f.write('This is a special line.\n')

    cookiecutter(repo_dir, no_input=True, update_dir='test_update')

    assert(os.path.isfile('test_update/' + new_file))
    with open('test_update/' + new_file) as f:
        assert 'This is a special line.\n' in f.read()

    os.remove(repo_dir + "{{cookiecutter.repo_name}}/" + new_file)


@pytest.mark.usefixtures('create_test_dir', 'clean_system', 'remove_test_dir')
def test_update_file_no_conflict():
    repo_dir = 'tests/test-update/'

    # Modify a file
    mod_file = 'README.txt'
    with open(repo_dir + "{{cookiecutter.repo_name}}/" + mod_file, 'a') as f:
        f.write('This is a special line.\n')

    cookiecutter(repo_dir, no_input=True, update_dir='test_update')

    assert(os.path.isfile('test_update/' + mod_file))
    with open('test_update/' + mod_file) as f:
        assert 'This is a special line.\n' in f.read()


@pytest.mark.usefixtures('create_test_dir', 'clean_system', 'remove_test_dir')
def test_update_conflicts(caplog):
    repo_dir = 'tests/test-update/'
    mod_file = 'README.txt'

    # Save file
    fd, fpath = tempfile.mkstemp()
    os.close(fd)
    shutil.copyfile(repo_dir + "{{cookiecutter.repo_name}}/" + mod_file, fpath)

    # Modify a file
    with open('test_update/' + mod_file, 'w+') as f:
        f.write('This is another special line.\n')

    # Modify the same file in the existing repo
    with open(repo_dir + "{{cookiecutter.repo_name}}/" + mod_file, 'w+') as f:
        for line in f.readlines():
            line.replace('Fake Project', 'Fake Updated Project')
    repo_git = git.Repo('test_update/')
    repo_git.git.add('README.txt')
    repo_git.git.commit('-m', 'README.txt: add a new line')

    with caplog.at_level(logging.WARNING,
                         logger='cookiecutter.update:update.py'):
        cookiecutter(repo_dir, no_input=True, update_dir='test_update')

    assert repo_git.active_branch.name == 'master'

    # Restore file
    shutil.copyfile(fpath, 'test_update/' + mod_file)
