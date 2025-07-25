"""Test cookiecutter for work without any input.

Tests in this file execute `cookiecutter()` with `no_input=True` flag and
verify result with different settings in `cookiecutter.json`.
"""

import os
import textwrap
from pathlib import Path

import pytest

from cookiecutter import main, utils

@pytest.mark.parametrize('path', ['tests/fake-repo-pre/', 'tests/fake-repo-pre'])
@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_no_input_return_project_dir(path) -> None:
    """Verify `cookiecutter` create project dir on input with or without slash."""
    project_dir = main.cookiecutter(path, no_input=True)
    assert os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}')
    assert not os.path.isdir('tests/fake-repo-pre/fake-project')
    assert os.path.isdir(project_dir)
    assert os.path.isfile('fake-project/README.rst')
    assert not os.path.exists('fake-project/json/')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_no_input_extra_context() -> None:
    """Verify `cookiecutter` accept `extra_context` argument."""
    main.cookiecutter(
        'tests/fake-repo-pre',
        no_input=True,
        extra_context={'repo_name': 'fake-project-extra'},
    )
    assert os.path.isdir('fake-project-extra')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_templated_context() -> None:
    """Verify Jinja2 templating correctly works in `cookiecutter.json` file."""
    main.cookiecutter('tests/fake-repo-tmpl', no_input=True)
    assert os.path.isdir('fake-project-templated')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_no_input_return_rendered_file() -> None:
    """Verify Jinja2 templating correctly works in `cookiecutter.json` file."""
    project_dir = main.cookiecutter('tests/fake-repo-pre', no_input=True)
    assert project_dir == os.path.abspath('fake-project')
    content = Path(project_dir, 'README.rst').read_text()
    assert "Project name: **Fake Project**" in content


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_dict_values_in_context() -> None:
    """Verify configured dictionary from `cookiecutter.json` correctly unpacked."""
    project_dir = main.cookiecutter('tests/fake-repo-dict', no_input=True)
    assert project_dir == os.path.abspath('fake-project-dict')

    content = Path(project_dir, 'README.md').read_text()
    assert (
        content
        == textwrap.dedent(
            """
        # README


        <dl>
          <dt>Format name:</dt>
          <dd>Bitmap</dd>

          <dt>Extension:</dt>
          <dd>bmp</dd>

          <dt>Applications:</dt>
          <dd>
              <ul>
              <li>Paint</li>
              <li>GIMP</li>
              </ul>
          </dd>
        </dl>

        <dl>
          <dt>Format name:</dt>
          <dd>Portable Network Graphic</dd>

          <dt>Extension:</dt>
          <dd>png</dd>

          <dt>Applications:</dt>
          <dd>
              <ul>
              <li>GIMP</li>
              </ul>
          </dd>
        </dl>

    """
        ).lstrip()
    )


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_template_cleanup(mocker) -> None:
    """Verify temporary folder for zip unpacking dropped."""
    mocker.patch('tempfile.mkdtemp', return_value='fake-tmp', autospec=True)

    mocker.patch(
        'cookiecutter.prompt.prompt_and_delete', return_value=True, autospec=True
    )

    main.cookiecutter('tests/files/fake-repo-tmpl.zip', no_input=True)
    assert os.path.isdir('fake-project-templated')

    # The tmp directory will still exist, but the
    # extracted template directory *in* the temp directory will not.
    assert os.path.exists('fake-tmp')
    assert not os.path.exists('fake-tmp/fake-repo-tmpl')
