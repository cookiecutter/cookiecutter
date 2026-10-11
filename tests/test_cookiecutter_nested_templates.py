"""Test cookiecutter invocation with nested configuration structure."""

import json
from pathlib import Path

import pytest

from cookiecutter import main


@pytest.mark.parametrize(
    "template_dir,output_dir",
    [
        ["fake-nested-templates", "fake-project"],
        ["fake-nested-templates-old-style", "fake-package"],
    ],
)
def test_cookiecutter_nested_templates(
    mocker, template_dir: str, output_dir: str
) -> None:
    """Verify cookiecutter nested configuration files mechanism."""
    mock_generate_files = mocker.patch("cookiecutter.main.generate_files")
    main_dir = (Path("tests") / template_dir).resolve()
    main.cookiecutter(f"{main_dir}", no_input=True)
    expected = (Path(main_dir) / output_dir).resolve()
    assert mock_generate_files.call_args[1]["repo_dir"] == f"{expected}"


@pytest.mark.parametrize("old_style", [False, True])
@pytest.mark.parametrize("directory", [None, "templates", "group/templates"])
@pytest.mark.parametrize("levels", [1, 2])
def test_nested_templates_with_directory(
    tmp_path: Path, output_dir: str, old_style: bool, directory: str | None, levels: int
) -> None:
    """Apply the repository subdirectory only before choosing nested templates."""
    repo_dir = tmp_path / "repo"
    template_dir = repo_dir / directory if directory else repo_dir
    for _ in range(levels):
        template_dir.mkdir(parents=True, exist_ok=True)
        choices = (
            {"template": ["Project (child)"]}
            if old_style
            else {"templates": {"project": {"path": "child"}}}
        )
        (template_dir / "cookiecutter.json").write_text(
            json.dumps(choices), encoding="utf-8"
        )
        template_dir /= "child"

    project_dir = template_dir / "{{cookiecutter.project_slug}}"
    project_dir.mkdir(parents=True)
    (template_dir / "cookiecutter.json").write_text(
        json.dumps({"project_slug": "generated-project"}), encoding="utf-8"
    )
    (project_dir / "README.txt").write_text(
        "Project: {{cookiecutter.project_slug}}\n", encoding="utf-8"
    )

    result = main.cookiecutter(
        str(repo_dir), directory=directory, no_input=True, output_dir=output_dir
    )

    assert Path(result) == Path(output_dir) / "generated-project"
    assert (Path(result) / "README.txt").read_text(encoding="utf-8") == (
        "Project: generated-project\n"
    )
