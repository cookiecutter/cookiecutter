from cookiecutter.main import is_repo_url


def test_is_repo_url():
    """Verify is_repo_url works."""
    assert is_repo_url('gitolite@server:team/repo') is True
    assert is_repo_url('git@github.com:audreyr/cookiecutter.git') is True
    assert is_repo_url('https://github.com/audreyr/cookiecutter.git') is True
    assert is_repo_url('gh:audreyr/cookiecutter-pypackage') is True
    assert is_repo_url('https://bitbucket.org/pokoli/cookiecutter.hg') is True

    assert is_repo_url('/audreyr/cookiecutter.git') is False
    assert is_repo_url('/home/audreyr/cookiecutter') is False
