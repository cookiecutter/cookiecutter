# -*- coding: utf-8 -*-
# flake8: noqa
"""
test_context
------------

Tests for `cookiecutter.context` module that handles prompts for v2 context.
"""
from __future__ import unicode_literals

import sys
import os.path
import time
import json
import logging

import pytest

from collections import OrderedDict

from cookiecutter import context

from cookiecutter.exceptions import ContextDecodingException

import click

from uuid import UUID

logger = logging.getLogger(__name__)


def load_cookiecutter(cookiecutter_file):

    context = {}
    try:
        with open(cookiecutter_file) as file_handle:
            obj = json.load(file_handle, object_pairs_hook=OrderedDict)
    except ValueError as e:
        # JSON decoding error.  Let's throw a new exception that is more
        # friendly for the developer or user.
        full_fpath = os.path.abspath(cookiecutter_file)
        json_exc_message = str(e)
        our_exc_message = (
            'JSON decoding error while loading "{0}".  Decoding'
            ' error details: "{1}"'.format(full_fpath, json_exc_message)
        )
        raise ContextDecodingException(our_exc_message)

    # Add the Python object to the context dictionary
    file_name = os.path.split(cookiecutter_file)[1]
    file_stem = file_name.split('.')[0]
    context[file_stem] = obj

    return context


def context_data_check():
    context_all_reqs = (
        {
            'cookiecutter_context': OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    ("variables", []),
                ]
            )
        },
        True,
    )

    context_missing_name = (
        {
            'cookiecutter_context': OrderedDict(
                [("cookiecutter_version", "2.0.0"), ("variables", [])]
            )
        },
        False,
    )

    context_missing_cookiecutter_version = (
        {
            'cookiecutter_context': OrderedDict(
                [("name", "cookiecutter-pytest-plugin"), ("variables", [])]
            )
        },
        False,
    )

    context_missing_variables = (
        {
            'cookiecutter_context': OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                ]
            )
        },
        False,
    )

    yield context_all_reqs
    yield context_missing_name
    yield context_missing_cookiecutter_version
    yield context_missing_variables


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_result', context_data_check())
def test_context_check(input_params, expected_result):
    """
    Test that a context with the required fields will be detected as a
    v2 context.
    """
    assert context.context_is_version_2(**input_params) == expected_result


@pytest.mark.usefixtures('clean_system')
def test_load_context_defaults():

    cc = load_cookiecutter('tests/test-context/cookiecutter.json')

    cc_cfg = context.load_context(cc['cookiecutter'], no_input=True)

    assert cc_cfg['full_name'] == 'Raphael Pierzina'
    assert cc_cfg['email'] == 'raphael@hackebrot.de'
    assert cc_cfg['plugin_name'] == 'emoji'
    assert cc_cfg['module_name'] == 'emoji'
    assert cc_cfg['license'] == 'MIT'
    assert cc_cfg['docs'] is False
    assert 'docs_tool' not in cc_cfg.keys()  # skip_if worked
    assert cc_cfg['year'] == time.strftime('%Y')
    assert cc_cfg['incept_year'] == 2017
    assert cc_cfg['released'] is False
    assert cc_cfg['temperature'] == 77.3
    assert cc_cfg['Release-GUID'] == UUID('04f5eaa9ee7345469dccffc538b27194')
    assert cc_cfg['extensions'] == "['jinja2_time.TimeExtension']"
    assert (
        cc_cfg['copy_with_out_render']
        == "['*.html', '*not_rendered_dir', 'rendered_dir/not_rendered_file.ini']"
    )
    assert cc_cfg['fixtures'] == OrderedDict(
        [
            ('foo', OrderedDict([('scope', 'session'), ('autouse', True)])),
            ('bar', OrderedDict([('scope', 'function'), ('autouse', False)])),
        ]
    )


@pytest.mark.usefixtures('clean_system')
def test_load_context_defaults_skips_branch():
    """
    Test that if_no_skip_to and if_yes_skip_to actually do branch and
    skip variables
    """
    cc = load_cookiecutter('tests/test-context/cookiecutter_skips_1.json')

    cc_cfg = context.load_context(cc['cookiecutter_skips_1'], no_input=True)

    assert cc_cfg['project_configuration_enabled'] is False
    assert 'project_config_format' not in cc_cfg.keys()  # it was skipped

    assert cc_cfg['project_uses_existing_logging_facilities'] is True
    assert 'project_logging_enabled' not in cc_cfg.keys()  # it was skipped
    assert 'project_console_logging_enabled' not in cc_cfg.keys()  # it was skipped
    assert 'project_console_logging_level' not in cc_cfg.keys()  # it was skipped
    assert 'project_file_logging_enabled' not in cc_cfg.keys()  # it was skipped
    assert 'project_file_logging_level' not in cc_cfg.keys()  # it was skipped
    assert cc_cfg['github_username'] == 'eruber'


@pytest.mark.usefixtures('clean_system')
def test_load_context_defaults_skips_no_branch():
    """
    Test that if_no_skip_to and if_yes_skip_to do not branch and do not
    skip variables.
    """
    cc = load_cookiecutter('tests/test-context/cookiecutter_skips_2.json')

    cc_cfg = context.load_context(cc['cookiecutter_skips_2'], no_input=True)

    assert cc_cfg['project_configuration_enabled'] is True
    assert cc_cfg['project_config_format'] == 'toml'  # not skipped

    assert cc_cfg['project_uses_existing_logging_facilities'] is False
    assert cc_cfg['project_logging_enabled'] is True  # not skipped
    assert cc_cfg['project_console_logging_enabled'] is True  # not skipped
    assert cc_cfg['project_console_logging_level'] == 'WARN'  # not skipped
    assert cc_cfg['project_file_logging_enabled'] is True  # not skipped

    assert 'project_file_logging_level' not in cc_cfg.keys()  # do_if skipped

    assert cc_cfg['github_username'] == 'eruber'


@pytest.mark.usefixtures('clean_system')
def test_load_context_defaults_skips_unknown_variable_name_warning(caplog):
    """
    Test that a warning is issued if a variable.name specified in a skip_to
    directive is not in the variable list.
    """
    cc = load_cookiecutter('tests/test-context/cookiecutter_skips_3.json')

    cc_cfg = context.load_context(cc['cookiecutter_skips_3'], no_input=True)

    assert cc_cfg['project_uses_existing_logging_facilities'] is False
    assert 'project_logging_enabled' not in cc_cfg.keys()  # it was skipped
    assert 'project_console_logging_enabled' not in cc_cfg.keys()  # it was skipped
    assert 'project_console_logging_level' not in cc_cfg.keys()  # it was skipped
    assert 'project_file_logging_enabled' not in cc_cfg.keys()  # it was skipped
    assert 'project_file_logging_level' not in cc_cfg.keys()  # it was skipped
    assert 'github_username' not in cc_cfg.keys()  # it was skipped

    for record in caplog.records:
        assert record.levelname == 'WARNING'

    assert (
        "Processed all variables, but skip_to_variable_name 'this_variable_name_is_not_in_the_list' was never found."
        in caplog.text
    )


def test_prompt_string(mocker):

    EXPECTED_VALUE = 'Input String'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='name', default='', prompt='Enter Name', hide_input=False)

    r = context.prompt_string(v, default='Alpha')

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default='Alpha',
        hide_input=v.hide_input,
        type=click.STRING,
    )

    assert r == EXPECTED_VALUE


def test_prompt_bool(mocker):

    EXPECTED_VALUE = True

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='flag', default=False, prompt='Enter a Flag', hide_input=False
    )

    r = context.prompt_boolean(v, default=False)

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default=False,
        hide_input=v.hide_input,
        type=click.BOOL,
    )

    assert r  # EXPECTED_VALUE


def test_prompt_int(mocker):

    EXPECTED_VALUE = 777

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='port', default=1000, prompt='Enter Port', hide_input=False)

    r = context.prompt_int(v, default=1000)

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default=1000,
        hide_input=v.hide_input,
        type=click.INT,
    )

    assert r == EXPECTED_VALUE


def test_prompt_float(mocker):

    EXPECTED_VALUE = 3.14

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='PI', default=3.0, prompt='Enter PI', hide_input=False)

    r = context.prompt_float(v, default=3.0)

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default=3.0,
        hide_input=v.hide_input,
        type=click.FLOAT,
    )

    assert r == EXPECTED_VALUE


def test_prompt_uuid(mocker):

    EXPECTED_VALUE = '931ef56c3e7b45eea0427bac386f0a98'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='uuid', default=None, prompt='Enter a UUID', hide_input=False
    )

    r = context.prompt_uuid(v, default=None)

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default=None,
        hide_input=v.hide_input,
        type=click.UUID,
    )

    assert r == EXPECTED_VALUE


def test_prompt_json(monkeypatch, mocker):

    EXPECTED_VALUE = '{"port": 67888, "colors": ["red", "green", "blue"]}'

    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )
    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='json', default=None, prompt='Enter Config', hide_input=False
    )

    r = context.prompt_json(v, default=None)

    assert r == {"port": 67888, "colors": ["red", "green", "blue"]}


def test_prompt_json_bad_json_decode_click_asks_again(mocker, capsys):

    EXPECTED_BAD_VALUE = '{"port": 67888, "colors": ["red", "green", "blue"}'
    EXPECTED_GOOD_VALUE = '{"port": 67888, "colors": ["red", "green", "blue"]}'

    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[EXPECTED_BAD_VALUE, EXPECTED_GOOD_VALUE],
    )
    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='json', default=None, prompt='Enter Config', hide_input=False
    )

    r = context.prompt_json(v, default=None)

    out, err = capsys.readouterr()
    assert 'Error: Unable to decode to JSON.' in out
    assert r == {"port": 67888, "colors": ["red", "green", "blue"]}


def test_prompt_json_default(mocker):
    EXPECTED_VALUE = 'default'

    cfg = '{"port": 67888, "colors": ["red", "green", "blue"]}'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='json', default=None, prompt='Enter Config', hide_input=False
    )

    r = context.prompt_json(v, default=cfg)

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default='default',
        hide_input=v.hide_input,
        type=click.STRING,
        value_proc=mocker.ANY,
    )

    assert r == cfg


def test_prompt_yes_no_default_no(mocker):

    EXPECTED_VALUE = 'y'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='enable_docs', default='n', prompt='Enable docs', hide_input=False
    )

    r = context.prompt_yes_no(v, default=False)

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default='n',
        hide_input=v.hide_input,
        type=click.BOOL,
    )

    assert r  # EXPECTED_VALUE


def test_prompt_yes_no_default_yes(mocker):

    EXPECTED_VALUE = 'y'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='enable_docs', default='y', prompt='Enable docs', hide_input=False
    )

    r = context.prompt_yes_no(v, default=True)

    assert mock_prompt.call_args == mocker.call(
        v.prompt,
        default='y',
        hide_input=v.hide_input,
        type=click.BOOL,
    )

    assert r  # EXPECTED_VALUE


def test_prompt_choice(mocker):

    LICENSES = ['ISC', 'MIT', 'BSD3']

    DEFAULT_LICENSE = 'ISC'

    EXPECTED_VALUE = '2'
    EXPECTED_LICENSE = 'MIT'

    mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value=EXPECTED_VALUE,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='license',
        default=DEFAULT_LICENSE,
        choices=LICENSES,
        prompt='Pick a License',
        hide_input=False,
    )

    r = context.prompt_choice(v, default=DEFAULT_LICENSE)

    assert r == EXPECTED_LICENSE


def test_variable_invalid_type_exception():

    with pytest.raises(ValueError) as excinfo:
        context.Variable(name='badtype', default=None, type='color')

    assert 'Variable: badtype has an invalid type color' in str(excinfo.value)


def test_variable_invalid_default_choice():

    CHOICES = ['green', 'red', 'blue', 'yellow']

    with pytest.raises(ValueError) as excinfo:
        context.Variable(
            name='badchoice', default='purple', type='string', choices=CHOICES
        )

    assert 'Variable: badchoice has an invalid default value purple for choices: {choices}'.format(
        choices=CHOICES
    ) in str(
        excinfo.value
    )


def test_variable_invalid_validation_control_flag_is_logged_and_removed(caplog):

    with caplog.at_level(logging.INFO):
        v = context.Variable(
            'module_name',
            "{{cookiecutter.plugin_name|lower|replace('-','_')}}",
            prompt="Please enter a name for your base python module",
            type='string',
            validation='^[a-z_]+$',
            validation_flags=[
                'ignorecase',
                'forget',
            ],
            hide_input=True,
        )

        for record in caplog.records:
            assert record.levelname == 'WARNING'

        assert (
            "Variable: module_name - Ignoring unkown RegEx validation Control Flag named 'forget'"
            in caplog.text
        )

        assert v.validation_flag_names == ['ignorecase']


def test_variable_validation_compile_exception():

    VAR_NAME = 'module_name'
    BAD_REGEX_STRING = '^[a-z_+$'  # Missing a closing square-bracket (])

    with pytest.raises(ValueError) as excinfo:
        context.Variable(
            VAR_NAME,
            "{{cookiecutter.plugin_name|lower|replace('-','_')}}",
            prompt="Please enter a name for your base python module",
            type='string',
            validation=BAD_REGEX_STRING,
            validation_flags=['ignorecase'],
            hide_input=True,
        )

    assert "Variable: {var_name} - Validation Setup Error: Invalid RegEx '{value}' - does not compile - ".format(
        var_name=VAR_NAME, value=BAD_REGEX_STRING
    ) in str(
        excinfo.value
    )


def test_variable_forces_no_prompt_for_private_variable_names():
    v = context.Variable(
        '_private_variable_name',
        "{{cookiecutter.plugin_name|lower|replace('-','_')}}",
        prompt="Please enter a name for your base python module",
        prompt_user=True,
        type='string',
        validation='^[a-z_]+$',
        validation_flags=['ignorecase'],
        hide_input=True,
    )

    assert v.prompt_user is False


def test_variable_repr():

    v = context.Variable(
        'module_name',
        "{{cookiecutter.plugin_name|lower|replace('-','_')}}",
        prompt="Please enter a name for your base python module",
        type='string',
        validation='^[a-z_]+$',
        validation_flags=['ignorecase'],
        hide_input=True,
    )

    assert repr(v) == "<Variable module_name>"


def test_variable_str():

    v = context.Variable(
        'module_name',
        "{{cookiecutter.plugin_name|lower|replace('-','_')}}",
        prompt="Please enter a name for your base python module",
        type='string',
        validation='^[a-z_]+$',
        validation_flags=['ignorecase'],
        hide_input=True,
    )

    str_v = str(v)
    assert '<Variable module_name>:' in str_v
    assert "name='module_name'" in str_v
    assert "default='{{cookiecutter.plugin_name|lower|replace('-','_')}}'" in str_v
    assert "description='None'" in str_v
    assert "prompt='Please enter a name for your base python module'" in str_v
    assert "hide_input='True'" in str_v
    assert "var_type='string'" in str_v
    assert "skip_if=''" in str_v
    assert "prompt_user='True'" in str_v
    assert "choices='[]'" in str_v
    assert "validation='^[a-z_]+$'" in str_v
    assert "validation_flag_names='['ignorecase']'" in str_v
    assert (
        "validation_flags='2'" in str_v or "validation_flags='re.IGNORECASE'" in str_v
    )

    if sys.version_info >= (3, 4):
        assert "validate='re.compile('^[a-z_]+$', re.IGNORECASE)'" in str(v)
    else:
        assert "validate='<_sre.SRE_Pattern object at" in str(v)


def test_variable_option_raise_invalid_type_value_error():

    VAR_NAME = 'module_name'
    OPT_VALUE_OF_INCORRECT_TYPE = 12  # should be a string

    with pytest.raises(ValueError) as excinfo:
        context.Variable(
            VAR_NAME,
            "{{cookiecutter.plugin_name|lower|replace('-','_')}}",
            prompt="Please enter a name for your base python module",
            type='string',
            validation=OPT_VALUE_OF_INCORRECT_TYPE,
            validation_flags=['ignorecase'],
            hide_input=True,
        )

    msg = "Variable: '{var_name}' Option: 'validation' requires a value of type str, but has a value of: {value}"
    assert msg.format(var_name=VAR_NAME, value=OPT_VALUE_OF_INCORRECT_TYPE) in str(
        excinfo.value
    )


def test_cookiecutter_template_repr():
    #  name, cookiecutter_version, variables, **info

    cct = context.CookiecutterTemplate(
        'cookiecutter_template_repr_test', cookiecutter_version='2.0.0', variables=[]
    )

    assert repr(cct) == "<CookiecutterTemplate cookiecutter_template_repr_test>"


def test_load_context_with_input_choices(mocker):
    cc = load_cookiecutter('tests/test-context/cookiecutter_choices.json')

    INPUT_1 = 'E.R. Uber'
    INPUT_2 = 'eruber@gmail.com'
    INPUT_3 = '2'  # 'MIT'
    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[INPUT_1, INPUT_2, INPUT_3],
    )

    cc_cfg = context.load_context(cc['cookiecutter_choices'], no_input=False)

    assert cc_cfg['full_name'] == INPUT_1
    assert cc_cfg['email'] == INPUT_2
    assert cc_cfg['license'] == 'MIT'


def test_load_context_with_input_choices_no_verbose(mocker):
    cc = load_cookiecutter('tests/test-context/cookiecutter_choices.json')

    INPUT_1 = 'E.R. Uber'
    INPUT_2 = 'eruber@gmail.com'
    INPUT_3 = '2'  # 'MIT'
    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[INPUT_1, INPUT_2, INPUT_3],
    )

    cc_cfg = context.load_context(
        cc['cookiecutter_choices'], no_input=False, verbose=False
    )

    assert cc_cfg['full_name'] == INPUT_1
    assert cc_cfg['email'] == INPUT_2
    assert cc_cfg['license'] == 'MIT'


def test_load_context_with_input_with_validation_success(mocker):
    cc = load_cookiecutter('tests/test-context/cookiecutter_val_success.json')

    INPUT_1 = 'Image Module Maker'
    INPUT_2 = ''
    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[INPUT_1, INPUT_2],
    )

    logger.debug(cc)

    cc_cfg = context.load_context(cc['cookiecutter_val_success'], no_input=False)

    assert cc_cfg['project_name'] == INPUT_1
    assert cc_cfg['module_name'] == 'image_module_maker'


def test_load_context_with_input_with_validation_failure(mocker, capsys):
    cc = load_cookiecutter('tests/test-context/cookiecutter_val_failure.json')

    INPUT_1 = '6 Debug Shell'
    INPUT_2 = ''
    INPUT_3 = 'debug_shell'
    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[INPUT_1, INPUT_2, INPUT_3],
    )

    cc_cfg = context.load_context(cc['cookiecutter_val_failure'], no_input=False)

    out, err = capsys.readouterr()

    msg = "Input validation failure against regex: '^[a-z_]+$', try again!"
    assert msg in out

    assert cc_cfg['project_name'] == INPUT_1
    assert cc_cfg['module_name'] == INPUT_3


def test_load_context_with_input_with_validation_failure_msg(mocker, capsys):
    cc = load_cookiecutter('tests/test-context/cookiecutter_val_failure_msg.json')

    INPUT_1 = '6 Debug Shell'
    INPUT_2 = ''
    INPUT_3 = 'debug_shell'
    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[INPUT_1, INPUT_2, INPUT_3],
    )

    cc_cfg = context.load_context(cc['cookiecutter_val_failure_msg'], no_input=False)

    out, err = capsys.readouterr()

    msg = "Input validation failure against regex: '^[a-z_]+$', try again!"
    assert msg in out

    msg2 = "Really, you couldn't get this correct the first time?"
    assert msg2 in out

    assert cc_cfg['project_name'] == INPUT_1
    assert cc_cfg['module_name'] == INPUT_3


def test_specify_if_yes_skip_to_without_yes_no_type():
    """
    Test ValueError is raised when a variable specifies an if_yes_skip_to
    field and the variable type is not 'yes+no'
    """
    with pytest.raises(ValueError) as excinfo:
        context.Variable(
            name='author', default='JKR', type='string', if_yes_skip_to='roman'
        )

    assert (
        "Variable: 'author' specifies 'if_yes_skip_to' field, but variable not of type 'yes_no'"
        in str(excinfo.value)
    )


def test_specify_if_no_skip_to_without_yes_no_type():
    """
    Test ValueError is raised when a variable specifies an if_no_skip_to
    field and the variable type is not 'yes+no'
    """
    with pytest.raises(ValueError) as excinfo:
        context.Variable(
            name='author', default='JKR', type='string', if_no_skip_to='roman'
        )

    assert (
        "Variable: 'author' specifies 'if_no_skip_to' field, but variable not of type 'yes_no'"
        in str(excinfo.value)
    )
