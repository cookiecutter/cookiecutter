#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_prompt
-----------

Tests for `cookiecutter.prompt` module.
TestPrompt.test_prompt_for_config_simple
TestPrompt.test_prompt_for_config_unicode
TestPrompt.test_unicode_prompt_for_config_unicode
TestPrompt.test_unicode_prompt_for_default_config_unicode
TestPrompt.test_unicode_prompt_for_templated_config

TestQueryAnswers.test_query_y
TestQueryAnswers.test_query_ye
TestQueryAnswers.test_query_yes
TestQueryAnswers.test_query_n

TestQueryDefaults.test_query_y_none_default
TestQueryDefaults.test_query_n_none_default
TestQueryDefaults.test_query_no_default
TestQueryDefaults.test_query_bad_default
"""

from collections import OrderedDict
import platform

import pytest

from cookiecutter import prompt


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    if 'windows' in platform.platform().lower():
        monkeypatch.setattr('sys.stdin.readline', lambda: '\n')


class TestPrompt(object):
    def test_prompt_for_config_simple(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'Audrey Roy'
        )
        context = {'cookiecutter': {'full_name': 'Your Name'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Audrey Roy'}

    def test_prompt_for_config_unicode(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'Pizzä ïs Gööd'
        )
        context = {'cookiecutter': {'full_name': 'Your Name'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Pizzä ïs Gööd'}

    def test_unicode_prompt_for_config_unicode(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'Pizzä ïs Gööd'
        )
        context = {'cookiecutter': {'full_name': u'Řekni či napiš své jméno'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Pizzä ïs Gööd'}

    def test_unicode_prompt_for_default_config_unicode(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'\n'
        )
        context = {'cookiecutter': {'full_name': u'Řekni či napiš své jméno'}}

        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'full_name': u'Řekni či napiš své jméno'}

    def test_unicode_prompt_for_templated_config(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'\n'
        )
        context = {'cookiecutter': OrderedDict([
            (
                'project_name',
                u'A New Project'
            ), (
                'pkg_name',
                u'{{ cookiecutter.project_name|lower|replace(" ", "") }}'
            )
        ])}

        exp_cookiecutter_dict = {
            'project_name': u'A New Project', 'pkg_name': u'anewproject'
        }
        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == exp_cookiecutter_dict

    def test_dont_prompt_for_private_context_var(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x: pytest.fail(
                'Should not try to read a response for private context var'
            )
        )
        context = {'cookiecutter': {'_copy_without_render': ['*.html']}}
        cookiecutter_dict = prompt.prompt_for_config(context)
        assert cookiecutter_dict == {'_copy_without_render': ['*.html']}


class TestQueryAnswers(object):
    @pytest.fixture(params=[u'y', u'ye', u'yes'])
    def patch_read_response(self, request, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': request.param
        )

    @pytest.mark.usefixtures('patch_read_response')
    def test_query(self):
        assert prompt.query_yes_no('Blah?')

    def test_query_n(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'n'
        )
        assert not prompt.query_yes_no('Blah?')


class TestQueryDefaults(object):
    def test_query_y_none_default(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'y'
        )
        assert prompt.query_yes_no('Blah?', default=None)

    def test_query_n_none_default(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'n'
        )
        assert not prompt.query_yes_no('Blah?', default=None)

    def test_query_no_default(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u''
        )
        assert not prompt.query_yes_no('Blah?', default='no')

    def test_query_bad_default(self, monkeypatch):
        monkeypatch.setattr(
            'cookiecutter.prompt.read_response',
            lambda x=u'': u'junk'
        )
        with pytest.raises(ValueError):
            prompt.query_yes_no('Blah?', default='yn')
