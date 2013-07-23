#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.generate
---------------------

Functions for generating a project from a project template.
"""

import json
import os

from jinja2 import FileSystemLoader, Template
from jinja2.environment import Environment

from .exceptions import NonTemplatedInputDirException
from .utils import make_sure_path_exists, unicode_open


def generate_context(json_dir='json/'):
    """
    Generates the context for a Cookiecutter project template.
    :param json_dir: Directory containing .json file(s).
    :paramtype json_dir: directory

    Description:

        Iterates through the contents of json_dir and finds all JSON
        files. Loads the JSON file as a Python object with the key being the
        JSON file name..

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


def generate_files(input_dir, context=None):
    """
    Renders the templates and saves them to files.
    :param input_dir: Project template input directory.
    :paramtype input_dir: directory
    """

    context = context or {}
    env = Environment()
    env.loader = FileSystemLoader('.')

    # Render dirname before writing
    name_tmpl = Template(input_dir)
    output_dir = name_tmpl.render(**context)
    if output_dir == input_dir:
        raise NonTemplatedInputDirException
        
    make_sure_path_exists(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for d in dirs:
            indir = os.path.join(root, d)
            outdir = indir.replace(input_dir, output_dir, 1)

            # Render dirname before writing
            name_tmpl = Template(outdir)
            rendered_dirname = name_tmpl.render(**context)

            make_sure_path_exists(rendered_dirname)

        for f in files:
            # Render the file
            infile = os.path.join(root, f)
            tmpl = env.get_template(infile)
            rendered_file = tmpl.render(**context)

            # Write it to the corresponding place in output_dir
            outfile = infile.replace(input_dir, output_dir, 1)

            # Render the output filename before writing
            name_tmpl = Template(outfile)
            rendered_name = name_tmpl.render(**context)
            print("Writing {0}".format(rendered_name))

            with unicode_open(rendered_name, 'w') as fh:
                fh.write(rendered_file)
