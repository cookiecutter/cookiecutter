# -*- coding: utf-8 -*-

"""Tests for `generate_files` function and related errors raising.

Use the global clean_system fixture and run additional teardown code to remove
some special folders.

For a better understanding - order of fixture calls:
clean_system setup code
remove_additional_folders setup code
remove_additional_folders teardown code
clean_system teardown code
"""

from __future__ import unicode_literals

import io
import os

import pytest
from binaryornot.check import is_binary
from cookiecutter import exceptions, generate, utils


@pytest.mark.parametrize('invalid_dirname', ['', '{foo}', '{{foo', 'bar}}'])
def test_ensure_dir_is_templated_raises(invalid_dirname):
    """Verify `ensure_dir_is_templated` raises on wrong directories names input."""
    with pytest.raises(exceptions.NonTemplatedInputDirException):
        generate.ensure_dir_is_templated(invalid_dirname)


@pytest.fixture(scope='function')
def remove_additional_folders():
    """Remove some special folders which are created by the tests."""
    yield
    if os.path.exists('inputpizzä'):
        utils.rmtree('inputpizzä')
    if os.path.exists('inputgreen'):
        utils.rmtree('inputgreen')
    if os.path.exists('inputbinary_files'):
        utils.rmtree('inputbinary_files')
    if os.path.exists('tests/custom_output_dir'):
        utils.rmtree('tests/custom_output_dir')
    if os.path.exists('inputpermissions'):
        utils.rmtree('inputpermissions')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_nontemplated_exception():
    """
    Verify `generate_files` raises when no directories to render exist.

    Note: Check `tests/test-generate-files-nontemplated` location to understand.
    """
    with pytest.raises(exceptions.NonTemplatedInputDirException):
        generate.generate_files(
            context={'cookiecutter': {'food': 'pizza'}},
            repo_dir='tests/test-generate-files-nontemplated',
        )


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files():
    """Verify directory name correctly rendered with unicode containing context."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
    )

    simple_file = 'inputpizzä/simple.txt'
    assert os.path.isfile(simple_file)

    simple_text = io.open(simple_file, 'rt', encoding='utf-8').read()
    assert simple_text == u'I eat pizzä'


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_with_trailing_newline():
    """Verify new line not removed by templating engine after folder generation."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
    )

    newline_file = 'inputpizzä/simple-with-newline.txt'
    assert os.path.isfile(newline_file)

    with io.open(newline_file, 'r', encoding='utf-8') as f:
        simple_text = f.read()
    assert simple_text == u'I eat pizzä\n'


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_binaries():
    """Verify binary files created during directory generation."""
    generate.generate_files(
        context={'cookiecutter': {'binary_test': 'binary_files'}},
        repo_dir='tests/test-generate-binaries',
    )

    assert is_binary('inputbinary_files/logo.png')
    assert is_binary('inputbinary_files/.DS_Store')
    assert not is_binary('inputbinary_files/readme.txt')
    assert is_binary('inputbinary_files/some_font.otf')
    assert is_binary('inputbinary_files/binary_files/logo.png')
    assert is_binary('inputbinary_files/binary_files/.DS_Store')
    assert not is_binary('inputbinary_files/binary_files/readme.txt')
    assert is_binary('inputbinary_files/binary_files/some_font.otf')
    assert is_binary('inputbinary_files/binary_files/binary_files/logo.png')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_absolute_path():
    """Verify usage of `abspath` does not change files generation behaviour."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir=os.path.abspath('tests/test-generate-files'),
    )
    assert os.path.isfile('inputpizzä/simple.txt')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_output_dir():
    """Verify `output_dir` option for `generate_files` changing location correctly."""
    os.mkdir('tests/custom_output_dir')
    project_dir = generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir=os.path.abspath('tests/test-generate-files'),
        output_dir='tests/custom_output_dir',
    )
    assert os.path.isfile('tests/custom_output_dir/inputpizzä/simple.txt')
    assert project_dir == os.path.abspath('tests/custom_output_dir/inputpizzä')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_permissions():
    """Verify generates files respect source files permissions.

    simple.txt and script.sh should retain their respective 0o644 and 0o755
    permissions.
    """
    generate.generate_files(
        context={'cookiecutter': {'permissions': 'permissions'}},
        repo_dir='tests/test-generate-files-permissions',
    )

    assert os.path.isfile('inputpermissions/simple.txt')

    # simple.txt should still be 0o644
    tests_simple_file = os.path.join(
        'tests',
        'test-generate-files-permissions',
        'input{{cookiecutter.permissions}}',
        'simple.txt',
    )
    tests_simple_file_mode = os.stat(tests_simple_file).st_mode & 0o777

    input_simple_file = os.path.join('inputpermissions', 'simple.txt')
    input_simple_file_mode = os.stat(input_simple_file).st_mode & 0o777
    assert tests_simple_file_mode == input_simple_file_mode

    assert os.path.isfile('inputpermissions/script.sh')

    # script.sh should still be 0o755
    tests_script_file = os.path.join(
        'tests',
        'test-generate-files-permissions',
        'input{{cookiecutter.permissions}}',
        'script.sh',
    )
    tests_script_file_mode = os.stat(tests_script_file).st_mode & 0o777

    input_script_file = os.path.join('inputpermissions', 'script.sh')
    input_script_file_mode = os.stat(input_script_file).st_mode & 0o777
    assert tests_script_file_mode == input_script_file_mode


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_with_overwrite_if_exists_with_skip_if_file_exists():
    """Verify `skip_if_file_exist` has priority over `overwrite_if_exists`."""
    simple_file = 'inputpizzä/simple.txt'
    simple_with_new_line_file = 'inputpizzä/simple-with-newline.txt'

    os.makedirs('inputpizzä')
    with open(simple_file, 'w') as f:
        f.write('temp')

    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
        overwrite_if_exists=True,
        skip_if_file_exists=True,
    )

    assert os.path.isfile(simple_file)
    assert os.path.isfile(simple_with_new_line_file)

    simple_text = io.open(simple_file, 'rt', encoding='utf-8').read()
    assert simple_text == u'temp'


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_with_skip_if_file_exists():
    """Verify existed files not removed if error raised with `skip_if_file_exists`."""
    simple_file = 'inputpizzä/simple.txt'
    simple_with_new_line_file = 'inputpizzä/simple-with-newline.txt'

    os.makedirs('inputpizzä')
    with open(simple_file, 'w') as f:
        f.write('temp')

    with pytest.raises(exceptions.OutputDirExistsException):
        generate.generate_files(
            context={'cookiecutter': {'food': 'pizzä'}},
            repo_dir='tests/test-generate-files',
            skip_if_file_exists=True,
        )

    assert os.path.isfile(simple_file)
    assert not os.path.exists(simple_with_new_line_file)

    simple_text = io.open(simple_file, 'rt', encoding='utf-8').read()
    assert simple_text == u'temp'


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_generate_files_with_overwrite_if_exists():
    """Verify overwrite_if_exists overwrites old files."""
    simple_file = 'inputpizzä/simple.txt'
    simple_with_new_line_file = 'inputpizzä/simple-with-newline.txt'

    os.makedirs('inputpizzä')
    with open(simple_file, 'w') as f:
        f.write('temp')

    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
        overwrite_if_exists=True,
    )

    assert os.path.isfile(simple_file)
    assert os.path.isfile(simple_with_new_line_file)

    simple_text = io.open(simple_file, 'rt', encoding='utf-8').read()
    assert simple_text == u'I eat pizzä'


@pytest.fixture
def undefined_context():
    """Fixture. Populate context variable for future tests."""
    return {
        'cookiecutter': {'project_slug': 'testproject', 'github_username': 'hackebrot'}
    }


def test_raise_undefined_variable_file_name(tmpdir, undefined_context):
    """Verify correct error raised when file name cannot be rendered."""
    output_dir = tmpdir.mkdir('output')

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/file-name/',
            output_dir=str(output_dir),
            context=undefined_context,
        )
    error = err.value
    assert "Unable to create file '{{cookiecutter.foobar}}'" == error.message
    assert error.context == undefined_context

    assert not output_dir.join('testproject').exists()


def test_raise_undefined_variable_file_name_existing_project(tmpdir, undefined_context):
    """Verify correct error raised when file name cannot be rendered."""
    output_dir = tmpdir.mkdir('output')

    output_dir.join('testproject').mkdir()

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/file-name/',
            output_dir=str(output_dir),
            context=undefined_context,
            overwrite_if_exists=True,
        )
    error = err.value
    assert "Unable to create file '{{cookiecutter.foobar}}'" == error.message
    assert error.context == undefined_context

    assert output_dir.join('testproject').exists()


def test_raise_undefined_variable_file_content(tmpdir, undefined_context):
    """Verify correct error raised when file content cannot be rendered."""
    output_dir = tmpdir.mkdir('output')

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/file-content/',
            output_dir=str(output_dir),
            context=undefined_context,
        )
    error = err.value
    assert "Unable to create file 'README.rst'" == error.message
    assert error.context == undefined_context

    assert not output_dir.join('testproject').exists()


def test_raise_undefined_variable_dir_name(tmpdir, undefined_context):
    """Verify correct error raised when directory name cannot be rendered."""
    output_dir = tmpdir.mkdir('output')

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/dir-name/',
            output_dir=str(output_dir),
            context=undefined_context,
        )
    error = err.value

    directory = os.path.join('testproject', '{{cookiecutter.foobar}}')
    msg = "Unable to create directory '{}'".format(directory)
    assert msg == error.message

    assert error.context == undefined_context

    assert not output_dir.join('testproject').exists()


def test_raise_undefined_variable_dir_name_existing_project(tmpdir, undefined_context):
    """Verify correct error raised when directory name cannot be rendered."""
    output_dir = tmpdir.mkdir('output')

    output_dir.join('testproject').mkdir()

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/dir-name/',
            output_dir=str(output_dir),
            context=undefined_context,
            overwrite_if_exists=True,
        )
    error = err.value

    directory = os.path.join('testproject', '{{cookiecutter.foobar}}')
    msg = "Unable to create directory '{}'".format(directory)
    assert msg == error.message

    assert error.context == undefined_context

    assert output_dir.join('testproject').exists()


def test_raise_undefined_variable_project_dir(tmpdir):
    """Verify correct error raised when directory name cannot be rendered."""
    output_dir = tmpdir.mkdir('output')

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/dir-name/',
            output_dir=str(output_dir),
            context={},
        )
    error = err.value
    msg = "Unable to create project directory '{{cookiecutter.project_slug}}'"
    assert msg == error.message
    assert error.context == {}

    assert not output_dir.join('testproject').exists()
