#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import codecs
import errno
import json
import os
import sys

from jinja2 import FileSystemLoader, Template
from jinja2.environment import Environment


PY3 = sys.version > '3'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


def unicode_open(filename, *args, **kwargs):

    if PY3:
        return open(filename, *args, **kwargs)
    kwargs['encoding'] = "utf-8"
    return codecs.open(filename, *args, **kwargs)
    

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


def generate_files(input_dir, output_dir, context=None):
    """ Renders the templates and saves them to files. """

    context = context or {}
    env = Environment()
    env.loader = FileSystemLoader('.')

    # Render dirname before writing
    name_tmpl = Template(output_dir)
    rendered_dirname = name_tmpl.render(**context)
    make_sure_path_exists(rendered_dirname)
    
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


def main():
    """ Entry point for the package, as defined in setup.py. """
    
    # Get command line input/output arguments
    parser = argparse.ArgumentParser(
        description='Create a project from a Cookiecutter project template.'
    )
    parser.add_argument(
        'input_dir', 
        help='Cookiecutter project template dir, e.g. {{project.repo_name}}/'
    )
    parser.add_argument(
        'output_dir',
        help='Name of desired output dir, e.g. alotofeffort/ or {{project.repo_name}}/. \
            (This can be templated.)'
    )
    args = parser.parse_args()

    context = generate_context()
    generate_files(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        context=context
    )


if __name__ == '__main__':
    main()
