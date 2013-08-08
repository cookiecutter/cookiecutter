#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.generate
---------------------

Functions for generating a project from a project template.
"""

import logging
import os
import sys

from jinja2 import FileSystemLoader, Template
from jinja2.environment import Environment

from .exceptions import NonTemplatedInputDirException
from .utils import make_sure_path_exists, unicode_open


if sys.version_info[:2] < (2, 7):
    import simplejson as json
    from ordereddict import OrderedDict
else:
    import json
    from collections import OrderedDict

def generate_context(config_file='cookiecutter.json'):
    """
    Generates the context for a Cookiecutter project template.
    Loads the JSON file as a Python object, with key being the JSON filename.

    :param config_file: JSON file containing project config values.
    :paramtype config_file: filename
    """

    context = {}

    file_handle = open(config_file)
    obj = json.load(file_handle, object_pairs_hook=OrderedDict)

    # Add the Python object to the context dictionary
    file_name = os.path.split(config_file)[1]
    file_stem = file_name.split('.')[0]
    context[file_stem] = obj

    logging.debug('Context generated is {0}'.format(context))
    return context


def generate_files(template_dir, context=None):
    """
    Renders the templates and saves them to files.
    :param input_dir: Project template input directory.
    :paramtype input_dir: directory
    """
    
    logging.debug('Generating project from {0}...'.format(template_dir))

    context = context or {}
    env = Environment()
    env.loader = FileSystemLoader('.')

    # Render dirname before writing
    name_tmpl = Template(template_dir)
    output_dir = name_tmpl.render(**context)
    if output_dir == template_dir:
        raise NonTemplatedInputDirException

    make_sure_path_exists(output_dir)

    for root, dirs, files in os.walk(template_dir):
        for d in dirs:
            indir = os.path.join(root, d)
            outdir = indir.replace(template_dir, output_dir, 1)

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
            outfile = infile.replace(template_dir, output_dir, 1)

            # Render the output filename before writing
            name_tmpl = Template(outfile)
            rendered_name = name_tmpl.render(**context)
            logging.debug("Writing {0}".format(rendered_name))

            with unicode_open(rendered_name, 'w') as fh:
                fh.write(rendered_file)
