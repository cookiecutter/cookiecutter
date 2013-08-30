#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.generate
---------------------

Functions for generating a project from a project template.
"""
from __future__ import unicode_literals
import logging
import os
import shutil
import sys

from jinja2 import FileSystemLoader, Template
from jinja2.environment import Environment
from binaryornot.check import is_binary

from .exceptions import NonTemplatedInputDirException
from .utils import make_sure_path_exists, unicode_open, work_in


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
    obj = json.load(file_handle, encoding='utf-8', object_pairs_hook=OrderedDict)

    # Add the Python object to the context dictionary
    file_name = os.path.split(config_file)[1]
    file_stem = file_name.split('.')[0]
    context[file_stem] = obj

    logging.debug('Context generated is {0}'.format(context))
    return context


def generate_file(project_dir, infile, context, env):
    """
    1. Render the contents of infile.
    2. Render the filename of infile as the name of outfile.
    3. Write the rendered infile to outfile.
    :param infile: Input file to generate the file from.
    """
    logging.debug("Generating file {0}".format(infile))

    # Render the intermediary path to the output file (not including the root
    # project dir nor the filename itself)
    outdir_tmpl = Template(os.path.dirname(infile))
    outdir = outdir_tmpl.render(**context)

    # Write the file to the corresponding place
    fname = os.path.basename(infile)  # input/output filename
    outfile = os.path.join(project_dir, outdir, fname)
    logging.debug("outfile is {0}".format(outfile))

    # Just copy over binary files. Don't render.
    logging.debug("Check {0} to see if it's a binary".format(infile))
    if is_binary(infile):
        logging.debug("Copying binary {0} to {1} without rendering"
                      .format(infile, outfile))
        shutil.copyfile(infile, outfile)

    else:
        # Force fwd slashes on Windows for get_template
        # This is a by-design Jinja issue
        infile_fwd_slashes = infile.replace(os.path.sep, '/')

        # Render the file
        tmpl = env.get_template(infile_fwd_slashes)
        rendered_file = tmpl.render(**context)

        # Render the output filename before writing
        name_tmpl = Template(outfile)
        rendered_name = name_tmpl.render(**context)
        logging.debug("Writing {0}".format(rendered_name))

        with unicode_open(rendered_name, 'w') as fh:
            fh.write(rendered_file)

def generate_files(template_dir, context=None):
    """
    Renders the templates and saves them to files.
    :param input_dir: Project template input directory.
    :paramtype input_dir: directory
    """

    # Always use utf-8
    template_dir = template_dir

    logging.debug('Generating project from {0}...'.format(template_dir))

    context = context or {}

    # Render dirname before writing
    name_tmpl = Template(template_dir)
    project_dir = name_tmpl.render(**context)

    if project_dir == template_dir:
        raise NonTemplatedInputDirException

    # We want the Jinja path and the OS paths to match. Consequently, we'll:
    #   + CD to the template folder
    #   + Set Jinja's path to "."
    #
    #  In order to build our files to the correct folder(s), we'll use an
    # absolute path for the target folder (project)

    project_dir = os.path.abspath(project_dir)

    logging.debug("project_dir is {0}".format(project_dir))
    make_sure_path_exists(project_dir)

    with work_in(template_dir):
        env = Environment()
        env.loader = FileSystemLoader(".")

        for root, dirs, files in os.walk("."):

            for d in dirs:
                indir = os.path.join(root, d)
                name_tmpl = Template(indir)
                rendered_dirname = name_tmpl.render(**context)
                make_sure_path_exists(os.path.join(project_dir, rendered_dirname))

            for f in files:
                infile = os.path.join(root, f)
                logging.debug("f is {0}".format(f))
                generate_file(project_dir, infile, context, env)
