#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.prompt
---------------------

Functions for prompting the user for project info.
"""

from __future__ import unicode_literals
from collections import namedtuple
import sys

from .compat import iteritems, read_response
from jinja2.environment import Environment


ContextEntry = namedtuple('ContextEntry', 'key default prompt type_')


def get_context_entry(key, value):
    """Normalizes a context entry from different context versions to a
    consistent format.

    :param key: the context key
    :param value: either a string, or a dict represeting a context entry
    :returns: a :class:`ContextEntry`
    """
    if isinstance(value, dict):
        return ContextEntry(
            key,
            value.get('default', ''),
            value.get('prompt', key),
            value.get('type'))

    return ContextEntry(key, value, key, None)


def get_value(entry, value, default):
    """Return a context value for a context_entry. User submitted values
    are treated differently based on their type.
    """
    value = value if value != '' else default
    if entry.type_ == 'boolean':
        return value.lower() in ('y', 'yes', 'true', 'on', '1')

    return value


def prompt_for_config(context, no_input=False):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.

    :param no_input: Prompt the user at command line for manual configuration?
    """
    cookiecutter_dict = {}
    env = Environment()

    for key, raw in iteritems(context['cookiecutter']):
        context_entry = get_context_entry(key, raw)
        value = (env.from_string(context_entry.default)
                    .render(cookiecutter=cookiecutter_dict))

        if not no_input:
            prompt = '{entry.prompt} (default is "{default}")? '.format(
                entry=context_entry,
                default=value)

            value = get_value(
                context_entry,
                read_response(prompt).strip(),
                value)

        cookiecutter_dict[key] = value
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
