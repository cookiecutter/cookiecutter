#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.prompt
---------------------

Functions for prompting the user for project info.
"""

from __future__ import unicode_literals
import os
import sys

PY3 = sys.version > '3'
if PY3:
    iteritems = lambda d: iter(d.items())
else:
    input = raw_input
    iteritems = lambda d: d.iteritems()

def get_input(p=''):
    return input(p)

def _parse_bool(value):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False, '0': False}
    return valid.get(value.lower(), bool(value))

def merge(dest, dictionary):
    try:
        return dest.format(**dictionary)
    except KeyError:
        return dest


def prompt_for_config(context):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.
    """
    cookiecutter_dict = {}

    for key, val in iteritems(context['cookiecutter']):
        default = val
        prompt = key
        if isinstance(val, dict):
            if PY3:
                default = val.get('default', key)
            else:
                default = val.get('default', key).decode('utf-8')
            prompt = val.get('prompt', key)

        default = merge(default, cookiecutter_dict)
        default = merge(default, dict(('$%s' % k, v) for k, v in os.environ.items()))

        prompt = merge("{0} (default is \"{1}\")? ".format(prompt, default), cookiecutter_dict)
        prompt = merge(prompt, dict(('$%s' % k, v) for k, v in os.environ.items()))

        if PY3:
            new_val = input(prompt)
        else:
            new_val = get_input(prompt.encode('utf-8')).decode('utf-8')

        new_val = new_val.strip()
        if new_val == '':
            new_val = default

        if isinstance(val, dict) and 'type' in val:
            new_val = {"int": int, "bool": _parse_bool}.get(val["type"])(new_val)

        cookiecutter_dict[key] = new_val

    return cookiecutter_dict


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via `raw_input()` and return their answer.

    :param question: A string that is presented to the user.
    :param default: The presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    Adapted from
    http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    http://code.activestate.com/recipes/577058/

    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
