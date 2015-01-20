#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.prompt
---------------------

Functions for prompting the user for project info.
"""

from __future__ import unicode_literals
import sys

from .compat import iteritems, read_response, is_string
from jinja2.environment import Environment


def prompt_for_config(context, no_input=False):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.

    :param no_input: Prompt the user at command line for manual configuration?
    """
    cookiecutter_dict = {}
    env = Environment()

    for key, raw in iteritems(context['cookiecutter']):
        raw = raw if is_string(raw) else str(raw)
        val = env.from_string(raw).render(cookiecutter=cookiecutter_dict)

        if not no_input:
            prompt = '{0} (default is "{1}")? '.format(key, val)

            new_val = read_response(prompt).strip()

            if new_val != '':
                val = new_val

        cookiecutter_dict[key] = val
    return cookiecutter_dict


def query_yes_no(question, default='yes'):
    """
    Ask a yes/no question via `read_response()` and return their answer.

    :param question: A string that is presented to the user.
    :param default: The presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    Adapted from
    http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    http://code.activestate.com/recipes/577058/

    """
    valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError('Invalid default answer: "{0}"'.format(default))

    while True:
        sys.stdout.write(question + prompt)
        choice = read_response().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write('Please respond with "yes" or "no" '
                             '(or "y" or "n").\n')
