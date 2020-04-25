# -*- coding: utf-8 -*-

"""Collection of tests around log handling."""

import logging

import pytest

from cookiecutter.log import configure_logger


def create_log_records():
    """Test function, create log entries in expected stage of test."""
    cookiecutter_logger = logging.getLogger('cookiecutter')
    foo_logger = logging.getLogger('cookiecutter.foo')
    foobar_logger = logging.getLogger('cookiecutter.foo.bar')

    cookiecutter_logger.info('Welcome to Cookiecutter')
    cookiecutter_logger.debug('Generating project from pytest-plugin')
    foo_logger.info('Loading user config from home dir')
    foobar_logger.debug("I don't know.")
    foobar_logger.debug('I wanted to save the world.')
    foo_logger.error('Aw, snap! Something went wrong')
    cookiecutter_logger.debug('Successfully generated project')


@pytest.fixture
def info_messages():
    """Fixture. List of test info messages."""
    return [
        'INFO: Welcome to Cookiecutter',
        'INFO: Loading user config from home dir',
        'ERROR: Aw, snap! Something went wrong',
    ]


@pytest.fixture
def debug_messages():
    """Fixture. List of test debug messages."""
    return [
        'INFO cookiecutter: ' 'Welcome to Cookiecutter',
        'DEBUG cookiecutter: ' 'Generating project from pytest-plugin',
        'INFO cookiecutter.foo: ' 'Loading user config from home dir',
        "DEBUG cookiecutter.foo.bar: " "I don't know.",
        'DEBUG cookiecutter.foo.bar: ' 'I wanted to save the world.',
        'ERROR cookiecutter.foo: ' 'Aw, snap! Something went wrong',
        'DEBUG cookiecutter: ' 'Successfully generated project',
    ]


@pytest.fixture
def info_logger():
    """Fixture. Call cookiecutter logger setup with `info` debug level."""
    return configure_logger(stream_level='INFO')


@pytest.fixture
def debug_logger():
    """Fixture. Call cookiecutter logger setup with `debug` debug level."""
    return configure_logger(stream_level='DEBUG')


@pytest.fixture
def debug_file(tmpdir):
    """Fixture. Generate debug file location for tests."""
    return tmpdir / 'pytest-plugin.log'


@pytest.fixture
def info_logger_with_file(debug_file):
    """Fixture. Call cookiecutter logger setup with `info` debug level + `file`."""
    return configure_logger(stream_level='INFO', debug_file=str(debug_file))


def test_info_stdout_logging(caplog, info_logger, info_messages):
    """Test that stdout logs use info format and level."""
    [stream_handler] = info_logger.handlers
    assert isinstance(stream_handler, logging.StreamHandler)
    assert stream_handler.level == logging.INFO

    create_log_records()

    stream_messages = [
        stream_handler.format(r)
        for r in caplog.records
        if r.levelno >= stream_handler.level
    ]

    assert stream_messages == info_messages


def test_debug_stdout_logging(caplog, debug_logger, debug_messages):
    """Test that stdout logs use debug format and level."""
    [stream_handler] = debug_logger.handlers
    assert isinstance(stream_handler, logging.StreamHandler)
    assert stream_handler.level == logging.DEBUG

    create_log_records()

    stream_messages = [
        stream_handler.format(r)
        for r in caplog.records
        if r.levelno >= stream_handler.level
    ]

    assert stream_messages == debug_messages


def test_debug_file_logging(caplog, info_logger_with_file, debug_file, debug_messages):
    """Test that logging to stdout uses a different format and level than \
    the the file handler."""
    [file_handler, stream_handler] = info_logger_with_file.handlers
    assert isinstance(file_handler, logging.FileHandler)
    assert isinstance(stream_handler, logging.StreamHandler)
    assert stream_handler.level == logging.INFO
    assert file_handler.level == logging.DEBUG

    create_log_records()

    assert debug_file.exists()

    # Last line in the log file is an empty line
    assert debug_file.readlines(cr=False) == debug_messages + ['']
