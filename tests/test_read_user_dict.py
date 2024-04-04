"""Test `process_json`, `read_user_dict` functions in `cookiecutter.prompt`."""

import click
import pytest
from rich.prompt import InvalidResponse

from cookiecutter.prompt import JsonPrompt, process_json, read_user_dict


def test_process_json_invalid_json() -> None:
    """Test `process_json` for correct error on malformed input."""
    with pytest.raises(InvalidResponse) as exc_info:
        process_json('nope]')

    assert str(exc_info.value) == 'Unable to decode to JSON.'


def test_process_json_non_dict() -> None:
    """Test `process_json` for correct error on non-JSON input."""
    with pytest.raises(InvalidResponse) as exc_info:
        process_json('[1, 2]')

    assert str(exc_info.value) == 'Requires JSON dict.'


def test_process_json_valid_json() -> None:
    """Test `process_json` for correct output on JSON input.

    Test for simple dict with list.
    """
    user_value = '{"name": "foobar", "bla": ["a", 1, "b", false]}'

    assert process_json(user_value) == {
        'name': 'foobar',
        'bla': ['a', 1, 'b', False],
    }


def test_process_json_deep_dict() -> None:
    """Test `process_json` for correct output on JSON input.

    Test for dict in dict case.
    """
    user_value = """{
        "key": "value",
        "integer_key": 37,
        "dict_key": {
            "deep_key": "deep_value",
            "deep_integer": 42,
            "deep_list": [
                "deep value 1",
                "deep value 2",
                "deep value 3"
            ]
        },
        "list_key": [
            "value 1",
            "value 2",
            "value 3"
        ]
    }"""

    assert process_json(user_value) == {
        "key": "value",
        "integer_key": 37,
        "dict_key": {
            "deep_key": "deep_value",
            "deep_integer": 42,
            "deep_list": ["deep value 1", "deep value 2", "deep value 3"],
        },
        "list_key": ["value 1", "value 2", "value 3"],
    }


def test_should_raise_type_error(mocker) -> None:
    """Test `default_value` arg verification in `read_user_dict` function."""
    prompt = mocker.patch('cookiecutter.prompt.JsonPrompt.ask')

    with pytest.raises(TypeError):
        read_user_dict('name', 'russell')
    assert not prompt.called


def test_should_call_prompt_with_process_json(mocker) -> None:
    """Test to make sure that `process_json` is actually being used.

    Verifies generation of a processor for the user input.
    """
    mock_prompt = mocker.patch('cookiecutter.prompt.JsonPrompt.ask', autospec=True)

    read_user_dict('name', {'project_slug': 'pytest-plugin'})
    print(mock_prompt.call_args)
    args, kwargs = mock_prompt.call_args

    assert args == ('name [cyan bold](default)[/]',)
    assert kwargs['default'] == {'project_slug': 'pytest-plugin'}


def test_should_not_load_json_from_sentinel(mocker) -> None:
    """Make sure that `json.loads` is not called when using default value."""
    mock_json_loads = mocker.patch(
        'cookiecutter.prompt.json.loads', autospec=True, return_value={}
    )

    runner = click.testing.CliRunner()
    with runner.isolation(input="\n"):
        read_user_dict('name', {'project_slug': 'pytest-plugin'})

    mock_json_loads.assert_not_called()


@pytest.mark.parametrize("input", ["\n", "\ndefault\n"])
def test_read_user_dict_default_value(input) -> None:
    """Make sure that `read_user_dict` returns the default value.

    Verify return of a dict variable rather than the display value.
    """
    runner = click.testing.CliRunner()
    with runner.isolation(input=input):
        val = read_user_dict('name', {'project_slug': 'pytest-plugin'})

    assert val == {'project_slug': 'pytest-plugin'}


def test_json_prompt_process_response() -> None:
    """Test `JsonPrompt` process_response to convert str to json."""
    jp = JsonPrompt()
    assert jp.process_response('{"project_slug": "something"}') == {
        'project_slug': 'something'
    }
