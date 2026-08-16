import pytest

from cookiecutter import generate


@pytest.mark.parametrize(
    "error",
    [
        TypeError("decode() argument 'encoding' must be str, not None"),
        NameError("name 'unicode' is not defined"),
    ],
)
def test_binary_detection_failure_falls_back_to_binary(monkeypatch, error):
    def fail_detection(_path):
        raise error

    monkeypatch.setattr(generate, "is_binary", fail_detection)

    assert generate._is_binary_file("font.ttf") is True
