import pytest

from tests.utils import dir_tests


@pytest.fixture
def context():
    """Fixture to return a valid context as known from a cookiecutter.json."""
    return {
        u'cookiecutter': {
            u'email': u'raphael@hackebrot.de',
            u'full_name': u'Raphael Pierzina',
            u'github_username': u'hackebrot',
            u'version': u'0.1.0',
        }
    }


@pytest.fixture
def replay_test_dir():
    return dir_tests('test-replay/')


@pytest.fixture
def mock_user_config(mocker):
    return mocker.patch('cookiecutter.main.get_user_config')
