import pytest

from cookiecutter import config


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
    return 'tests/test-replay/'


@pytest.fixture
def mock_user_config(mocker, replay_test_dir):
    user_config = config.DEFAULT_CONFIG
    user_config.update({'replay_dir': replay_test_dir})

    return mocker.patch(
        'cookiecutter.replay.get_user_config', return_value=user_config
    )
