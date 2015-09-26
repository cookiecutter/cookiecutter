from cookiecutter.main import is_repo_url, expand_abbreviations


def test_is_repo_url():
    """Verify is_repo_url works."""
    assert is_repo_url('gitolite@server:team/repo') is True
    assert is_repo_url('git@github.com:audreyr/cookiecutter.git') is True
    assert is_repo_url('https://github.com/audreyr/cookiecutter.git') is True
    assert is_repo_url('https://bitbucket.org/pokoli/cookiecutter.hg') is True

    assert is_repo_url('/audreyr/cookiecutter.git') is False
    assert is_repo_url('/home/audreyr/cookiecutter') is False

    appveyor_temp_dir = (
        'c:\\users\\appveyor\\appdata\\local\\temp\\1\\pytest-0\\'
        'test_default_output_dir0\\template'
    )
    assert is_repo_url(appveyor_temp_dir) is False


def test_expand_abbreviations():
    template = 'gh:audreyr/cookiecutter-pypackage'

    # This is not a valid repo url just yet!
    # First `main.expand_abbreviations` needs to translate it
    assert is_repo_url(template) is False

    expanded_template = expand_abbreviations(template, {})
    assert is_repo_url(expanded_template) is True
