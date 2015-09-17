#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.prompt
---------------------

Functions for prompting the user for project info.
"""

from __future__ import unicode_literals

import click

from .compat import iteritems, is_string
from jinja2.environment import Environment


def read_user_yes_no(question, default_value):
    """Prompt the user to reply with 'yes' or 'no' (or equivalent values).

    Note:
      Possible choices are 'true', '1', 'yes', 'y' or 'false', '0', 'no', 'n'

    :param str question: Question to the user
    :param default_value: Value that will be returned if no input happens
    """
    # Please see http://click.pocoo.org/4/api/#click.prompt
    return click.prompt(
        question,
        default=default_value,
        type=click.BOOL
    )


def render_variable(env, raw, cookiecutter_dict):
    if not is_string(raw):
        raw = str(raw)
    template = env.from_string(raw)
    rendered_template = template.render(cookiecutter=cookiecutter_dict)
    return rendered_template


def prompt_for_config(context, no_input=False):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.

    :param no_input: Prompt the user at command line for manual configuration?
    """
    cookiecutter_dict = {}
    env = Environment()

    for key, option in iteritems(context['cookiecutter']):
        if key.startswith('_'):
            cookiecutter_dict[key] = option.default
            continue

        cookiecutter_dict[key] = option.prompt_for_value(
            cookiecutter_dict, env, no_input)

    return cookiecutter_dict
