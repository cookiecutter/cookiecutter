#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import json
import os

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def generate_context(json_dir='json/'):
    """
    Generates the context for all complexity pages.

    Description:

        Iterates through the contents of the input_dir and finds all JSON
        files.
        Loads the JSON file as a Python object with the key being the JSON
        filename.

    Example:

        Assume the following files exist:

            json/names.json
            json/numbers.json

        Depending on their content, might generate a context as follows:

        contexts = {"names":
                        ['Audrey', 'Danny']
                    "numbers":
                        [1, 2, 3, 4]
                    }
    """
    context = {}

    for file_name in os.listdir(json_dir):
        file_to_open = "{0}/{1}".format(json_dir, file_name)
        file_handle = open(file_to_open)
        obj = json.load(file_handle)

        # Add the Python object to the context dictionary
        context[file_name[:-5]] = obj

    return context


def generate_files(context=None, input_dir='input/', output_dir='output/'):
    """ Renders the templates and saves them to files. """

    context = context or {}
    env = Environment()
    env.loader = FileSystemLoader(input_dir)

    make_sure_path_exists(output_dir)

    for f in os.listdir(input_dir):
        # If f is a directory, create it
        print f
        full_path = '{0}/{1}'.format(input_dir, f)
        print full_path
        if os.path.isdir(full_path):
            print "Found dir" + full_path
            make_sure_path_exists(full_path)
        elif os.path.isfile(full_path):   # If f is a file, render it
            tmpl = env.get_template(f)
            rendered_file = tmpl.render(**context)

            with open('{0}/{1}'.format(output_dir, f), 'w') as fh:
                fh.write(rendered_file)


def command_line_runner():
    """ Entry point for the package, as defined in setup.py. """

    context = generate_context()
    generate_files(context=context, input_dir='package')


if __name__ == '__main__':
    command_line_runner()
