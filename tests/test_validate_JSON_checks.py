import json
from pathlib import Path

import pytest

from cookiecutter.main import validate_cookiecutter_json


def test_validate_cookiecutter_json_invalid_json(tmp_path):
    """Invalid JSON should raise a RuntimeError."""
    context_file = tmp_path / "cookiecutter.json"
    context_file.write_text("{ invalid json", encoding="utf-8")

    with pytest.raises(RuntimeError, match="Invalid cookiecutter.json"):
        validate_cookiecutter_json(context_file)


def test_validate_cookiecutter_json_missing_cookiecutter_key(tmp_path):
    """Missing top-level 'cookiecutter' key should raise a RuntimeError."""
    context_file = tmp_path / "cookiecutter.json"
    data = {"not_cookiecutter": {}}
    context_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(RuntimeError, match="missing 'cookiecutter' key"):
        validate_cookiecutter_json(context_file)


def test_validate_cookiecutter_json_cookiecutter_not_dict(tmp_path):
    """'cookiecutter' must be a JSON object (dict), not another type."""
    context_file = tmp_path / "cookiecutter.json"
    data = {"cookiecutter": ["not", "a", "dict"]}
    context_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(RuntimeError, match="'cookiecutter' value must be an object"):
        validate_cookiecutter_json(context_file)


def test_validate_cookiecutter_json_valid_structure(tmp_path):
    """A well-formed cookiecutter.json should pass without error."""
    context_file = tmp_path / "cookiecutter.json"
    data = {"cookiecutter": {"project_name": "Example"}}
    context_file.write_text(json.dumps(data), encoding="utf-8")

    # Should not raise
    validate_cookiecutter_json(context_file)
