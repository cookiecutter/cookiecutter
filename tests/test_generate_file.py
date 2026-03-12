"""Tests for `generate_file` function, part of `generate_files` function workflow."""

import json
import os
import re
from pathlib import Path
from unittest import mock

import pytest
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter.environment import StrictEnvironment


@pytest.fixture(scope='function', autouse=True)
def tear_down():
    """
    Fixture. Remove the test text file which is created by the tests.

    Used for all tests in this file.
    """
    yield
    if os.path.exists('tests/files/cheese.txt'):
        os.remove('tests/files/cheese.txt')
    if os.path.exists('tests/files/cheese_lf_newlines.txt'):
        os.remove('tests/files/cheese_lf_newlines.txt')
    if os.path.exists('tests/files/cheese_crlf_newlines.txt'):
        os.remove('tests/files/cheese_crlf_newlines.txt')
    if os.path.exists('tests/files/cheese_mixed_newlines.txt'):
        os.remove('tests/files/cheese_mixed_newlines.txt')
    if os.path.exists('tests/files/{{cookiecutter.generate_file}}_mixed_newlines.txt'):
        os.remove('tests/files/{{cookiecutter.generate_file}}_mixed_newlines.txt')


@pytest.fixture
def env():
    """Fixture. Set Jinja2 environment settings for other tests."""
    environment = StrictEnvironment()
    environment.loader = FileSystemLoader('.')
    return environment


def test_generate_file(env) -> None:
    """Verify simple file is generated with rendered context data."""
    infile = 'tests/files/{{cookiecutter.generate_file}}.txt'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'cookiecutter': {'generate_file': 'cheese'}},
        env=env,
    )
    assert os.path.isfile('tests/files/cheese.txt')
    generated_text = Path('tests/files/cheese.txt').read_text()
    assert generated_text == 'Testing cheese'


def test_generate_file_jsonify_filter(env) -> None:
    """Verify jsonify filter works during files generation process."""
    infile = 'tests/files/{{cookiecutter.jsonify_file}}.txt'
    data = {'jsonify_file': 'cheese', 'type': 'roquefort'}
    generate.generate_file(
        project_dir=".", infile=infile, context={'cookiecutter': data}, env=env
    )
    assert os.path.isfile('tests/files/cheese.txt')
    generated_text = Path('tests/files/cheese.txt').read_text()
    assert json.loads(generated_text) == data


@pytest.mark.parametrize("length", (10, 40))
@pytest.mark.parametrize("punctuation", (True, False))
def test_generate_file_random_ascii_string(env, length, punctuation) -> None:
    """Verify correct work of random_ascii_string extension on file generation."""
    infile = 'tests/files/{{cookiecutter.random_string_file}}.txt'
    data = {'random_string_file': 'cheese'}
    context = {"cookiecutter": data, "length": length, "punctuation": punctuation}
    generate.generate_file(project_dir=".", infile=infile, context=context, env=env)
    assert os.path.isfile('tests/files/cheese.txt')
    generated_text = Path('tests/files/cheese.txt').read_text()
    assert len(generated_text) == length


def test_generate_file_with_true_condition(env) -> None:
    """Verify correct work of boolean condition in file name on file generation.

    This test has positive answer, so file should be rendered.
    """
    infile = (
        'tests/files/{% if cookiecutter.generate_file == \'y\' %}cheese.txt{% endif %}'
    )
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'cookiecutter': {'generate_file': 'y'}},
        env=env,
    )
    assert os.path.isfile('tests/files/cheese.txt')
    generated_text = Path('tests/files/cheese.txt').read_text()
    assert generated_text == 'Testing that generate_file was y'


def test_generate_file_with_false_condition(env) -> None:
    """Verify correct work of boolean condition in file name on file generation.

    This test has negative answer, so file should not be rendered.
    """
    infile = (
        'tests/files/{% if cookiecutter.generate_file == \'y\' %}cheese.txt{% endif %}'
    )
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'cookiecutter': {'generate_file': 'n'}},
        env=env,
    )
    assert not os.path.isfile('tests/files/cheese.txt')


@pytest.fixture
def expected_msg_regex():
    """Fixture. Used to ensure that exception generated text contain full data."""
    return re.compile(
        'Missing end of comment tag\n'
        ' {2}File "(.[/\\\\])*tests[/\\\\]files[/\\\\]syntax_error.txt", line 1\n'
        ' {4}I eat {{ syntax_error }} {# this comment is not closed}'
    )


def test_generate_file_verbose_template_syntax_error(env, expected_msg_regex) -> None:
    """Verify correct exception raised on syntax error in file before generation."""
    with pytest.raises(TemplateSyntaxError) as exception:
        generate.generate_file(
            project_dir=".",
            infile='tests/files/syntax_error.txt',
            context={'syntax_error': 'syntax_error'},
            env=env,
        )
    assert expected_msg_regex.match(str(exception.value))


def test_generate_file_does_not_translate_lf_newlines_to_crlf(env) -> None:
    """Verify that file generation use same line ending, as in source file."""
    infile = 'tests/files/{{cookiecutter.generate_file}}_lf_newlines.txt'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'cookiecutter': {'generate_file': 'cheese'}},
        env=env,
    )

    # this generated file should have a LF line ending
    gf = 'tests/files/cheese_lf_newlines.txt'
    with Path(gf).open(encoding='utf-8', newline='') as f:
        simple_text = f.readline()
    assert simple_text == 'newline is LF\n'
    assert f.newlines == '\n'


def test_generate_file_does_not_translate_crlf_newlines_to_lf(env) -> None:
    """Verify that file generation use same line ending, as in source file."""
    infile = 'tests/files/{{cookiecutter.generate_file}}_crlf_newlines.txt'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'cookiecutter': {'generate_file': 'cheese'}},
        env=env,
    )

    # this generated file should have a CRLF line ending
    gf = 'tests/files/cheese_crlf_newlines.txt'
    with Path(gf).open(encoding='utf-8', newline='') as f:
        simple_text = f.readline()
    assert simple_text == 'newline is CRLF\r\n'
    assert f.newlines == '\r\n'


def test_generate_file_handles_mixed_line_endings(env) -> None:
    """Verify that file generation gracefully handles mixed line endings."""
    infile = 'tests/files/{{cookiecutter.generate_file}}_mixed_newlines.txt'
    with open(infile, mode='w', encoding='utf-8', newline='') as f:
        f.write('newline is CRLF\r\n')
        f.write('newline is LF\n')
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'cookiecutter': {'generate_file': 'cheese'}},
        env=env,
    )

    # this generated file should have either CRLF or LF line ending
    gf = 'tests/files/cheese_mixed_newlines.txt'
    with Path(gf).open(encoding='utf-8', newline='') as f:
        simple_text = f.readline()
    assert simple_text in ('newline is CRLF\r\n', 'newline is CRLF\n')
    assert f.newlines in ('\r\n', '\n')


@pytest.mark.parametrize(
    "exception",
    [
        NameError("name 'unicode' is not defined"),
        TypeError("decode() argument 'encoding' must be str, not None"),
    ],
    ids=["NameError", "TypeError"],
)
def test_generate_file_treats_file_as_binary_when_detection_fails(
    monkeypatch, env, tmp_path, exception
) -> None:
    """Regression test for https://github.com/cookiecutter/cookiecutter/issues/2197.

    When ``binaryornot`` raises ``NameError`` or ``TypeError`` (e.g. due to
    chardet 7.x returning ``None`` for the encoding), the file should be
    treated as binary and copied without rendering.
    """
    # generate_file uses relative infile paths joined with project_dir.
    # Simulate the real workflow: chdir to the template dir, use a relative
    # infile, and point project_dir at a separate output directory.
    infile = "somefile.ttf"
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    (template_dir / infile).write_bytes(b"\x00\x01\x02binary-content")

    out_dir = tmp_path / "output"
    out_dir.mkdir()

    monkeypatch.chdir(template_dir)

    with mock.patch("cookiecutter.generate.is_binary", side_effect=exception):
        generate.generate_file(
            project_dir=str(out_dir),
            infile=infile,
            context={'cookiecutter': {}},
            env=env,
        )

    outfile = out_dir / infile
    assert outfile.exists()
    assert outfile.read_bytes() == b"\x00\x01\x02binary-content"
