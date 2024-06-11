"""
tests_output_folder.

Test formerly known from a unittest residing in test_generate.py named
TestOutputFolder.test_output_folder
"""

from pathlib import Path

import pytest

from cookiecutter import exceptions, generate, utils


@pytest.fixture(scope='function')
def remove_output_folder():
    """Remove the output folder after test."""
    yield
    output_folder = Path('output_folder')
    if output_folder.exists():
        utils.rmtree(output_folder)


@pytest.mark.usefixtures('clean_system', 'remove_output_folder')
def test_output_folder() -> None:
    """Tests should correctly create content, as output_folder does not yet exist."""
    context = generate.generate_context(
        context_file='tests/test-output-folder/cookiecutter.json'
    )
    generate.generate_files(context=context, repo_dir='tests/test-output-folder')

    something = """Hi!
My name is Audrey Greenfeld.
It is 2014.
"""
    something2 = Path('output_folder/something.txt').read_text()
    assert something == something2

    in_folder = "The color is green and the letter is D.\n"
    in_folder2 = Path('output_folder/folder/in_folder.txt').read_text()
    assert in_folder == in_folder2

    dir = Path('output_folder/im_a.dir')
    assert dir.is_dir()
    assert (dir / 'im_a.file.py').is_file()


@pytest.mark.usefixtures('clean_system', 'remove_output_folder')
def test_exception_when_output_folder_exists() -> None:
    """Tests should raise error as output folder created before `generate_files`."""
    context = generate.generate_context(
        context_file='tests/test-output-folder/cookiecutter.json'
    )
    output_folder = Path(context['cookiecutter']['test_name'])

    if not output_folder.exists():
        output_folder.mkdir()
    with pytest.raises(exceptions.OutputDirExistsException):
        generate.generate_files(context=context, repo_dir='tests/test-output-folder')
