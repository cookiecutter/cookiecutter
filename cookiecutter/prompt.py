#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.prompt
---------------------

Functions for prompting the user for project info.
"""

from collections import OrderedDict

import click
from past.builtins import basestring

from future.utils import iteritems
from jinja2.environment import Environment


def read_user_variable(var_name, default_value):
    """Prompt the user for the given variable and return the entered value
    or the given default.

    :param str var_name: Variable of the context to query the user
    :param default_value: Value that will be returned if no input happens
    """
    # Please see http://click.pocoo.org/4/api/#click.prompt
    return click.prompt(var_name, default=default_value)


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


def read_user_choice(var_name, options):
    """Prompt the user to choose from several options for the given variable.

    The first item will be returned if no input happens.

    :param str var_name: Variable as specified in the context
    :param list options: Sequence of options that are available to select from
    :return: Exactly one item of ``options`` that has been chosen by the user
    """
    # Please see http://click.pocoo.org/4/api/#click.prompt
    if not isinstance(options, list):
        raise TypeError

    if not options:
        raise ValueError

    choice_map = OrderedDict(
        (u'{}'.format(i), value) for i, value in enumerate(options, 1)
    )
    choices = choice_map.keys()
    default = u'1'

    choice_lines = [u'{} - {}'.format(*c) for c in choice_map.items()]
    prompt = u'\n'.join((
        u'Select {}:'.format(var_name),
        u'\n'.join(choice_lines),
        u'Choose from {}'.format(u', '.join(choices))
    ))

    user_choice = click.prompt(
        prompt, type=click.Choice(choices), default=default
    )
    return choice_map[user_choice]


def render_variable(env, raw, cookiecutter_dict):
    if not isinstance(raw, basestring):
        raw = str(raw)
    template = env.from_string(raw)
    rendered_template = template.render(cookiecutter=cookiecutter_dict)
    return rendered_template


def prompt_choice_for_config(cookiecutter_dict, env, key, options, no_input):
    """Prompt the user which option to choose from the given. Each of the
    possible choices is rendered beforehand.
    """
    rendered_options = [
        render_variable(env, raw, cookiecutter_dict) for raw in options
    ]

    if no_input:
        return rendered_options[0]
    return read_user_choice(key, rendered_options)


def prompt_for_config(context, no_input=False):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.

    :param no_input: Prompt the user at command line for manual configuration?
    """
    cookiecutter_dict = {}
    env = Environment()

    for key, raw in iteritems(context[u'cookiecutter']):
        if key.startswith(u'_'):
            cookiecutter_dict[key] = raw
            continue

        if isinstance(raw, list):
            # We are dealing with a choice variable
            val = prompt_choice_for_config(
                cookiecutter_dict, env, key, raw, no_input
            )
        else:
            # We are dealing with a regular variable
            val = render_variable(env, raw, cookiecutter_dict)

            if not no_input:
                val = read_user_variable(key, val)

        cookiecutter_dict[key] = val
    return cookiecutter_dict
