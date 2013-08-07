#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.prompt
---------------------

Functions for prompting the user for project info.
"""

import sys

PY3 = sys.version > '3'
if PY3:
    pass
else:
    input = raw_input

def prompt_for_config(context):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.
    """
    cookiecutter_dict = {}
    
    for key, val in context['cookiecutter'].iteritems():
        prompt = "{0} (e.g. \"{1}\")? ".format(key, val)
        new_val = input(prompt)
        new_val = new_val.strip()

        while new_val == '':
            prompt = "Please enter a value for {0}: ".format(key)
            new_val = input(prompt)
            new_val = new_val.strip()
        
        cookiecutter_dict[key] = new_val
    
    return cookiecutter_dict
