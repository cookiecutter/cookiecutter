"""Tests for `generate_files` function and related errors raising.

Use the global clean_system fixture and run additional teardown code to remove
some special folders.
"""

from pathlib import Path

import pytest
from binaryornot.check import is_binary
from jinja2 import Environment

from cookiecutter import exceptions, generate


def test_generate_files_nontemplated_exception(tmp_path) -> None:
    """
    Verify `generate_files` raises when no directories to render exist.

    Note: Check `tests/test-generate-files-nontemplated` location to understand.
    """
    with pytest.raises(exceptions.NonTemplatedInputDirException):
        generate.generate_files(
            context={'cookiecutter': {'food': 'pizza'}},
            repo_dir='tests/test-generate-files-nontemplated',
            output_dir=tmp_path,
        )


def test_generate_files(tmp_path) -> None:
    """Verify directory name correctly rendered with unicode containing context."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
        output_dir=tmp_path,
    )

    simple_file = Path(tmp_path, 'inputpizzä/simple.txt')
    assert simple_file.exists()
    assert simple_file.is_file()

    simple_text = Path(simple_file).read_text(encoding='utf-8')
    assert simple_text == 'I eat pizzä\n'


def test_generate_files_with_linux_newline(tmp_path) -> None:
    """Verify new line not removed by templating engine after folder generation."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
        output_dir=tmp_path,
    )

    newline_file = Path(tmp_path, 'inputpizzä/simple-with-newline.txt')
    assert newline_file.is_file()
    assert newline_file.exists()

    with Path(newline_file).open(encoding='utf-8', newline='') as f:
        simple_text = f.readline()
    assert simple_text == 'newline is LF\n'
    assert f.newlines == '\n'


def test_generate_files_with_jinja2_environment(tmp_path) -> None:
    """Extend StrictEnvironment with _jinja2_env_vars cookiecutter template option."""
    generate.generate_files(
        context={
            'cookiecutter': {
                'food': 'pizzä',
                '_jinja2_env_vars': {'lstrip_blocks': True, 'trim_blocks': True},
            }
        },
        repo_dir='tests/test-generate-files',
        output_dir=tmp_path,
    )

    conditions_file = tmp_path.joinpath('inputpizzä/simple-with-conditions.txt')
    assert conditions_file.is_file()
    assert conditions_file.exists()

    simple_text = conditions_file.read_text(encoding='utf-8')
    assert simple_text == 'I eat pizzä\n'


def test_generate_files_with_trailing_newline_forced_to_linux_by_context(
    tmp_path,
) -> None:
    """Verify new line not removed by templating engine after folder generation."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä', '_new_lines': '\r\n'}},
        repo_dir='tests/test-generate-files',
        output_dir=tmp_path,
    )

    # assert 'Overwritting endline character with %s' in caplog.messages
    newline_file = Path(tmp_path, 'inputpizzä/simple-with-newline.txt')
    assert newline_file.is_file()
    assert newline_file.exists()

    with Path(newline_file).open(encoding='utf-8', newline='') as f:
        simple_text = f.readline()
    assert simple_text == 'newline is LF\r\n'
    assert f.newlines == '\r\n'


def test_generate_files_with_windows_newline(tmp_path) -> None:
    """Verify windows source line end not changed during files generation."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
        output_dir=tmp_path,
    )

    newline_file = Path(tmp_path, 'inputpizzä/simple-with-newline-crlf.txt')
    assert newline_file.is_file()
    assert newline_file.exists()

    with Path(newline_file).open(encoding='utf-8', newline='') as f:
        simple_text = f.readline()
    assert simple_text == 'newline is CRLF\r\n'
    assert f.newlines == '\r\n'


def test_generate_files_with_windows_newline_forced_to_linux_by_context(
    tmp_path,
) -> None:
    """Verify windows line end changed to linux during files generation."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä', '_new_lines': '\n'}},
        repo_dir='tests/test-generate-files',
        output_dir=tmp_path,
    )

    newline_file = Path(tmp_path, 'inputpizzä/simple-with-newline-crlf.txt')
    assert newline_file.is_file()
    assert newline_file.exists()

    with Path(newline_file).open(encoding='utf-8', newline='') as f:
        simple_text = f.readline()

    assert simple_text == 'newline is CRLF\n'
    assert f.newlines == '\n'


def test_generate_files_binaries(tmp_path) -> None:
    """Verify binary files created during directory generation."""
    generate.generate_files(
        context={'cookiecutter': {'binary_test': 'binary_files'}},
        repo_dir='tests/test-generate-binaries',
        output_dir=tmp_path,
    )

    dst_dir = Path(tmp_path, 'inputbinary_files')

    assert is_binary(str(Path(dst_dir, 'logo.png')))
    assert is_binary(str(Path(dst_dir, '.DS_Store')))
    assert not is_binary(str(Path(dst_dir, 'readme.txt')))
    assert is_binary(str(Path(dst_dir, 'some_font.otf')))
    assert is_binary(str(Path(dst_dir, 'binary_files/logo.png')))
    assert is_binary(str(Path(dst_dir, 'binary_files/.DS_Store')))
    assert not is_binary(str(Path(dst_dir, 'binary_files/readme.txt')))
    assert is_binary(str(Path(dst_dir, 'binary_files/some_font.otf')))
    assert is_binary(str(Path(dst_dir, 'binary_files/binary_files/logo.png')))


def test_generate_files_absolute_path(tmp_path) -> None:
    """Verify usage of absolute path does not change files generation behaviour."""
    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir=Path('tests/test-generate-files').absolute(),
        output_dir=tmp_path,
    )
    assert Path(tmp_path, 'inputpizzä/simple.txt').is_file()


def test_generate_files_output_dir(tmp_path) -> None:
    """Verify `output_dir` option for `generate_files` changing location correctly."""
    output_dir = Path(tmp_path, 'custom_output_dir')
    output_dir.mkdir()

    project_dir = generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir=Path('tests/test-generate-files').absolute(),
        output_dir=output_dir,
    )

    assert Path(output_dir, 'inputpizzä/simple.txt').exists()
    assert Path(output_dir, 'inputpizzä/simple.txt').is_file()
    assert Path(project_dir) == Path(tmp_path, 'custom_output_dir/inputpizzä')


def test_generate_files_permissions(tmp_path) -> None:
    """Verify generates files respect source files permissions.

    simple.txt and script.sh should retain their respective 0o644 and 0o755
    permissions.
    """
    generate.generate_files(
        context={'cookiecutter': {'permissions': 'permissions'}},
        repo_dir='tests/test-generate-files-permissions',
        output_dir=tmp_path,
    )

    assert Path(tmp_path, 'inputpermissions/simple.txt').is_file()

    # Verify source simple.txt should still be 0o644
    tests_simple_file = Path(
        'tests',
        'test-generate-files-permissions',
        'input{{cookiecutter.permissions}}',
        'simple.txt',
    )
    tests_simple_file_mode = tests_simple_file.stat().st_mode

    input_simple_file = Path(tmp_path, 'inputpermissions', 'simple.txt')
    input_simple_file_mode = input_simple_file.stat().st_mode
    assert tests_simple_file_mode == input_simple_file_mode

    assert Path(tmp_path, 'inputpermissions/script.sh').exists()
    assert Path(tmp_path, 'inputpermissions/script.sh').is_file()

    # Verify source script.sh should still be 0o755
    tests_script_file = Path(
        'tests',
        'test-generate-files-permissions',
        'input{{cookiecutter.permissions}}',
        'script.sh',
    )
    tests_script_file_mode = tests_script_file.stat().st_mode

    input_script_file = Path(tmp_path, 'inputpermissions', 'script.sh')
    input_script_file_mode = input_script_file.stat().st_mode
    assert tests_script_file_mode == input_script_file_mode


def test_generate_files_with_overwrite_if_exists_with_skip_if_file_exists(
    tmp_path,
) -> None:
    """Verify `skip_if_file_exist` has priority over `overwrite_if_exists`."""
    simple_file = Path(tmp_path, 'inputpizzä/simple.txt')
    simple_with_new_line_file = Path(tmp_path, 'inputpizzä/simple-with-newline.txt')

    Path(tmp_path, 'inputpizzä').mkdir(parents=True)
    with Path(simple_file).open('w') as f:
        f.write('temp')

    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
        overwrite_if_exists=True,
        skip_if_file_exists=True,
        output_dir=tmp_path,
    )

    assert Path(simple_file).is_file()
    assert Path(simple_file).exists()
    assert Path(simple_with_new_line_file).is_file()
    assert Path(simple_with_new_line_file).exists()

    simple_text = Path(simple_file).read_text(encoding='utf-8')
    assert simple_text == 'temp'


def test_generate_files_with_skip_if_file_exists(tmp_path) -> None:
    """Verify existed files not removed if error raised with `skip_if_file_exists`."""
    simple_file = Path(tmp_path, 'inputpizzä/simple.txt')
    simple_with_new_line_file = Path(tmp_path, 'inputpizzä/simple-with-newline.txt')

    Path(tmp_path, 'inputpizzä').mkdir(parents=True)
    Path(simple_file).write_text('temp')

    with pytest.raises(exceptions.OutputDirExistsException):
        generate.generate_files(
            context={'cookiecutter': {'food': 'pizzä'}},
            repo_dir='tests/test-generate-files',
            skip_if_file_exists=True,
            output_dir=tmp_path,
        )

    assert Path(simple_file).is_file()
    assert not Path(simple_with_new_line_file).is_file()
    assert not Path(simple_with_new_line_file).exists()

    simple_text = Path(simple_file).read_text(encoding='utf-8')
    assert simple_text == 'temp'


def test_generate_files_with_overwrite_if_exists(tmp_path) -> None:
    """Verify overwrite_if_exists overwrites old files."""
    simple_file = Path(tmp_path, 'inputpizzä/simple.txt')
    simple_with_new_line_file = Path(tmp_path, 'inputpizzä/simple-with-newline.txt')

    Path(tmp_path, 'inputpizzä').mkdir(parents=True)
    Path(simple_file).write_text('temp')

    generate.generate_files(
        context={'cookiecutter': {'food': 'pizzä'}},
        repo_dir='tests/test-generate-files',
        overwrite_if_exists=True,
        output_dir=tmp_path,
    )

    assert Path(simple_file).is_file()
    assert Path(simple_file).exists()
    assert Path(simple_with_new_line_file).is_file()
    assert Path(simple_with_new_line_file).exists()

    simple_text = Path(simple_file).read_text(encoding='utf-8')
    assert simple_text == 'I eat pizzä\n'


@pytest.fixture
def undefined_context():
    """Fixture. Populate context variable for future tests."""
    return {
        'cookiecutter': {'project_slug': 'testproject', 'github_username': 'hackebrot'}
    }


def test_raise_undefined_variable_file_name(output_dir, undefined_context) -> None:
    """Verify correct error raised when file name cannot be rendered."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/file-name/',
            output_dir=output_dir,
            context=undefined_context,
        )
    error = err.value
    assert error.message == "Unable to create file '{{cookiecutter.foobar}}'"
    assert error.context == undefined_context

    assert not Path(output_dir).joinpath('testproject').exists()


def test_raise_undefined_variable_file_name_existing_project(
    output_dir, undefined_context
) -> None:
    """Verify correct error raised when file name cannot be rendered."""
    testproj_path = Path(output_dir, 'testproject')
    testproj_path.mkdir()

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/file-name/',
            output_dir=output_dir,
            context=undefined_context,
            overwrite_if_exists=True,
        )
    error = err.value
    assert error.message == "Unable to create file '{{cookiecutter.foobar}}'"
    assert error.context == undefined_context

    assert testproj_path.exists()


def test_raise_undefined_variable_file_content(output_dir, undefined_context) -> None:
    """Verify correct error raised when file content cannot be rendered."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/file-content/',
            output_dir=output_dir,
            context=undefined_context,
        )
    error = err.value
    assert error.message == "Unable to create file 'README.rst'"
    assert error.context == undefined_context

    assert not Path(output_dir).joinpath('testproject').exists()


def test_raise_undefined_variable_dir_name(output_dir, undefined_context) -> None:
    """Verify correct error raised when directory name cannot be rendered."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/dir-name/',
            output_dir=output_dir,
            context=undefined_context,
        )
    error = err.value

    directory = Path('testproject', '{{cookiecutter.foobar}}')
    msg = f"Unable to create directory '{directory}'"
    assert msg == error.message

    assert error.context == undefined_context

    assert not Path(output_dir).joinpath('testproject').exists()


def test_keep_project_dir_on_failure(output_dir, undefined_context) -> None:
    """Verify correct error raised when directory name cannot be rendered."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate):
        generate.generate_files(
            repo_dir='tests/undefined-variable/dir-name/',
            output_dir=output_dir,
            context=undefined_context,
            keep_project_on_failure=True,
        )
    assert Path(output_dir).joinpath('testproject').exists()


def test_raise_undefined_variable_dir_name_existing_project(
    output_dir, undefined_context
) -> None:
    """Verify correct error raised when directory name cannot be rendered."""
    testproj_path = Path(output_dir, 'testproject')
    testproj_path.mkdir()

    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/dir-name/',
            output_dir=output_dir,
            context=undefined_context,
            overwrite_if_exists=True,
        )
    error = err.value

    directory = Path('testproject', '{{cookiecutter.foobar}}')
    msg = f"Unable to create directory '{directory}'"
    assert msg == error.message

    assert error.context == undefined_context

    assert testproj_path.exists()


def test_raise_undefined_variable_project_dir(tmp_path) -> None:
    """Verify correct error raised when directory name cannot be rendered."""
    with pytest.raises(exceptions.UndefinedVariableInTemplate) as err:
        generate.generate_files(
            repo_dir='tests/undefined-variable/dir-name/',
            output_dir=tmp_path,
            context={},
        )
    error = err.value
    msg = "Unable to create project directory '{{cookiecutter.project_slug}}'"
    assert msg == error.message
    assert error.context == {}

    assert not Path(tmp_path, 'testproject').exists()


def test_raise_empty_dir_name(output_dir, undefined_context):
    """Verify correct error raised when directory name is empty."""
    with pytest.raises(exceptions.EmptyDirNameException):
        generate.render_and_create_dir(
            dirname='',
            output_dir=output_dir,
            context=undefined_context,
            environment=Environment(autoescape=True),
        )
    assert not Path(output_dir).joinpath('testproject').exists()
