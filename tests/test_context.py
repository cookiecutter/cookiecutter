# -*- coding: utf-8 -*-
# flake8: noqa
"""
test_context
------------

Tests for `cookiecutter.context` module that handles prompts for v2 context.
"""
from __future__ import unicode_literals

import json
import logging
import os.path
import sys
import time
from collections import OrderedDict
from uuid import UUID

import click
import pytest

from cookiecutter import context
from cookiecutter.exceptions import (
    ContextDecodingException,
    IncompatibleVersion,
    InvalidConfiguration,
)

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


@pytest.mark.usefixtures('clean_system')
def test_load_context_defaults():

    cc = load_cookiecutter('tests/test-context/cookiecutter.json')
    cc_cfg = context.load_context(cc['cookiecutter'], no_input=True)

    assert cc_cfg['full_name'] == 'Raphael Pierzina'
    assert cc_cfg['email'] == 'raphael@hackebrot.de'
    assert cc_cfg['plugin_name'] == 'emoji'
    assert cc_cfg['license'] == 'MIT'
    assert cc_cfg['docs'] is False
    assert cc_cfg['year'] == time.strftime('%Y')
    assert cc_cfg['incept_year'] == 2017
    assert cc_cfg['released'] is False
    assert cc_cfg['temperature'] == 77.3
    assert cc_cfg['Release-GUID'] == UUID('04f5eaa9ee7345469dccffc538b27194').hex
    assert cc_cfg['_extensions'] == [
        'cookiecutter.extensions.SlugifyExtension',
        'jinja2_time.TimeExtension',
    ]
    assert cc_cfg['_jinja2_env_vars'] == {"optimized": True}
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


def test_prompt_string(mocker):

    expected_value = 'Input String'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='name', type='string', default='', prompt='Enter Name')

    r = context.prompt_string(v, default='Alpha')

    assert mock_prompt.call_args == mocker.call(
        v.prompt, default='Alpha', type=click.STRING,
    )

    assert r == expected_value


def test_prompt_bool(mocker):

    expected_value = True

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='flag', type='bool', default=False, prompt='Enter a Flag',)

    r = context.prompt_boolean(v, default=False)

    assert mock_prompt.call_args == mocker.call(
        v.prompt, default=False, type=click.BOOL,
    )

    assert r  # expected_value


def test_prompt_int(mocker):

    expected_value = 777

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='port', type='int', default=1000, prompt='Enter Port')

    r = context.prompt_int(v, default=1000)

    assert mock_prompt.call_args == mocker.call(v.prompt, default=1000, type=click.INT,)

    assert r == expected_value


def test_prompt_float(mocker):

    expected_value = 3.14

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='PI', type='float', default=3.0, prompt='Enter PI')

    r = context.prompt_float(v, default=3.0)

    assert mock_prompt.call_args == mocker.call(
        v.prompt, default=3.0, type=click.FLOAT,
    )

    assert r == expected_value


def test_prompt_uuid(mocker):

    expected_value = '931ef56c3e7b45eea0427bac386f0a98'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='uuid', default=None, type='uuid', prompt='Enter a UUID')

    r = context.prompt_uuid(v, default=None)

    assert mock_prompt.call_args == mocker.call(
        v.prompt, default=None, type=click.UUID,
    )

    assert r == expected_value


def test_prompt_json(monkeypatch, mocker):

    expected_value = '{"port": 67888, "colors": ["red", "green", "blue"]}'

    mocker.patch(
        'click.termui.visible_prompt_func', autospec=True, return_value=expected_value,
    )
    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='json', type='json', default=None, prompt='Enter Config')

    r = context.prompt_json(v, default=None)

    assert r == {"port": 67888, "colors": ["red", "green", "blue"]}


def test_prompt_json_bad_json_decode_click_asks_again(mocker, capsys):

    expected_bad_value = '{"port": 67888, "colors": ["red", "green", "blue"}'
    expected_good_value = '{"port": 67888, "colors": ["red", "green", "blue"]}'

    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[expected_bad_value, expected_good_value],
    )
    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='json', type='json', default=None, prompt='Enter Config')

    r = context.prompt_json(v, default=None)

    out, err = capsys.readouterr()
    assert 'Error: Unable to decode to JSON.' in out
    assert r == {"port": 67888, "colors": ["red", "green", "blue"]}


def test_prompt_json_default(mocker):
    expected_value = 'default'

    cfg = '{"port": 67888, "colors": ["red", "green", "blue"]}'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(name='json', type='json', default=None, prompt='Enter Config')

    r = context.prompt_json(v, default=cfg)

    assert mock_prompt.call_args == mocker.call(
        v.prompt, default='default', type=click.STRING, value_proc=mocker.ANY,
    )

    assert r == cfg


def test_prompt_yes_no_default_no(mocker):

    expected_value = 'y'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='enable_docs',
        type='yes_no',
        default='n',
        prompt='Enable docs',
        hide_input=False,
    )

    r = context.prompt_yes_no(v, default=False)

    assert mock_prompt.call_args == mocker.call(v.prompt, default='n', type=click.BOOL,)

    assert r  # expected_value


def test_prompt_yes_no_default_yes(mocker):

    expected_value = 'y'

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='enable_docs',
        type='yes_no',
        default='y',
        prompt='Enable docs',
        hide_input=False,
    )

    r = context.prompt_yes_no(v, default=True)

    assert mock_prompt.call_args == mocker.call(v.prompt, default='y', type=click.BOOL,)

    assert r  # expected_value


def test_prompt_choice(mocker):

    licenses = ['ISC', 'MIT', 'BSD3']

    default_license = 'ISC'

    expected_value = '2'
    expected_license = 'MIT'

    mocker.patch(
        'cookiecutter.prompt.click.prompt', autospec=True, return_value=expected_value,
    )

    m = mocker.Mock()
    m.side_effect = context.Variable
    v = m.side_effect(
        name='license',
        type='string',
        default=default_license,
        choices=licenses,
        prompt='Pick a License',
        hide_input=False,
    )

    r = context.prompt_choice(v, default=default_license)

    assert r == expected_license


def test_variable_invalid_default_choice():
    choices = ['green', 'red', 'blue', 'yellow']
    with pytest.raises(InvalidConfiguration) as excinfo:
        context.Variable(
            name='badchoice', default='purple', type='string', choices=choices
        )
    assert (
        f'Variable: badchoice has an invalid default value purple for choices: {choices}'
        in str(excinfo.value)
    )


def test_variable_defaults_to_no_prompt_for_private_variable_names():
    v = context.Variable(
        '_private_variable_name',
        default="{{cookiecutter.plugin_name|lower|replace('-','_')}}",
        prompt="Please enter a name for your base python module",
        type='string',
        validation='^[a-z_]+$',
        validation_flags=['ignorecase'],
        hide_input=True,
    )

    assert v.prompt_user is False


def test_variable_repr():

    v = context.Variable(
        'module_name',
        default="{{cookiecutter.plugin_name|lower|replace('-','_')}}",
        prompt="Please enter a name for your base python module",
        type='string',
    )

    assert repr(v) == "<Variable module_name>"


def test_variable_str():
    v = context.Variable(
        'module_name',
        default="{{cookiecutter.plugin_name|lower|replace('-','_')}}",
        prompt="Please enter a name for your base python module",
        type='string',
    )

    v_str = str(v)
    assert '<Variable module_name>:' in v_str
    assert "name='module_name'" in v_str
    assert "default='{{cookiecutter.plugin_name|lower|replace('-','_')}}'" in v_str
    assert "prompt='Please enter a name for your base python module'" in v_str
    assert "var_type='string'" in v_str
    assert "prompt_user='True'" in v_str
    assert "choices='[]'" in v_str


def test_cookiecutter_template_repr():
    #  name, cookiecutter_version, variables, **info

    cct = context.CookiecutterTemplate(
        {'name': 'cookiecutter_template_repr_test', 'variables': []},
    )

    assert repr(cct) == "<CookiecutterTemplate cookiecutter_template_repr_test>"


def test_load_context_with_input_chioces(mocker):
    cc = load_cookiecutter('tests/test-context/cookiecutter_choices.json')

    input_1 = 'E.R. Uber'
    input_2 = 'eruber@gmail.com'
    input_3 = '2'  # 'MIT'
    mocker.patch(
        'click.termui.visible_prompt_func',
        autospec=True,
        side_effect=[input_1, input_2, input_3],
    )

    cc_cfg = context.load_context(cc['cookiecutter_choices'], no_input=False)

    assert cc_cfg['full_name'] == input_1
    assert cc_cfg['email'] == input_2
    assert cc_cfg['license'] == 'MIT'
