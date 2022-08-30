"""Test cookiecutter invocation with nested configuration structure."""
from cookiecutter import main


def test_cookiecutter_nested_templates(mocker):
    """Verify cookiecutter nested configuration files mechanism."""
    mock_generate_files = mocker.patch("cookiecutter.generate.generate_files")
    main_dir = "tests/fake-nested-templates"
    main.cookiecutter(main_dir, no_input=True)
    assert mock_generate_files.call_args[1]["repo_dir"] == f"{main_dir}/fake-project"
