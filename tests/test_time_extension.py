"""Tests for the TimeExtension Jinja2 extension."""

import freezegun
import pytest
from jinja2 import Environment, exceptions


@pytest.fixture
def environment():
    """Fixture. Add tested extension to environment."""
    return Environment(extensions=['cookiecutter.extensions.TimeExtension'])  # noqa: S701


@pytest.fixture(autouse=True)
def freeze():
    """Fixture. Freeze time for all tests."""
    freezer = freezegun.freeze_time("2015-12-09 23:33:01")
    freezer.start()
    yield
    freezer.stop()


def test_tz_is_required(environment) -> None:
    """Verify template parsing fails without a timezone."""
    with pytest.raises(exceptions.TemplateSyntaxError):
        environment.from_string('{% now %}')


def test_utc_default_datetime_format(environment) -> None:
    """Verify default datetime format can be parsed."""
    template = environment.from_string("{% now 'utc' %}")

    assert template.render() == "2015-12-09"


@pytest.mark.parametrize("valid_tz", ['utc', 'local', 'Europe/Berlin'])
def test_accept_valid_timezones(environment, valid_tz) -> None:
    """Verify that valid timezones are accepted."""
    template = environment.from_string(f"{{% now '{valid_tz}', '%Y-%m' %}}")

    assert template.render() == '2015-12'


def test_environment_datetime_format(environment) -> None:
    """Verify datetime format can be parsed from environment."""
    environment.datetime_format = '%a, %d %b %Y %H:%M:%S'

    template = environment.from_string("{% now 'utc' %}")

    assert template.render() == "Wed, 09 Dec 2015 23:33:01"


def test_add_time(environment) -> None:
    """Verify that added time offset can be parsed."""
    environment.datetime_format = '%a, %d %b %Y %H:%M:%S'

    template = environment.from_string("{% now 'utc' + 'hours=2,seconds=30' %}")

    assert template.render() == "Thu, 10 Dec 2015 01:33:31"


def test_substract_time(environment) -> None:
    """Verify that substracted time offset can be parsed."""
    environment.datetime_format = '%a, %d %b %Y %H:%M:%S'

    template = environment.from_string("{% now 'utc' - 'minutes=11' %}")

    assert template.render() == "Wed, 09 Dec 2015 23:22:01"


def test_offset_with_format(environment) -> None:
    """Verify that offset works together with datetime format."""
    environment.datetime_format = '%d %b %Y %H:%M:%S'

    template = environment.from_string(
        "{% now 'utc' - 'days=2,minutes=33,seconds=1', '%d %b %Y %H:%M:%S' %}"
    )

    assert template.render() == "07 Dec 2015 23:00:00"
