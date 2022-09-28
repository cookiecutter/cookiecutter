"""Tests for _dump_input function."""
import pytest

from cookiecutter.generate import _dump_input


def test_dump_input_OS_failure(mocker):
    """Fail due to OSError."""
    mocker.patch('builtins.open', side_effect=OSError)
    rmtree = mocker.patch('cookiecutter.generate.rmtree')
    with pytest.raises(OSError):
        _dump_input({}, "", True)
    rmtree.assert_called()


def test_dump_input_JSON_failure(tmp_path, mocker):
    """Fail due to invalid json."""
    rmtree = mocker.patch('cookiecutter.generate.rmtree')
    with pytest.raises(TypeError):
        _dump_input({'cookiecutter': {1, 2}}, tmp_path, False)
    rmtree.assert_not_called()
