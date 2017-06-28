# -*- coding: utf-8 -*-

"""Functions for generating a project from a project template."""
from __future__ import unicode_literals

import fnmatch
import io
import json
import logging
import os
import shutil
from collections import OrderedDict

from binaryornot.check import is_binary
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError, UndefinedError

from .environment import StrictEnvironment
from .exceptions import (
    NonTemplatedInputDirException,
    ContextDecodingException,
    FailedHookException,
    OutputDirExistsException,
    UndefinedVariableInTemplate
)
from .find import find_template
from .hooks import run_hook
from .utils import make_sure_path_exists, work_in, rmtree

logger = logging.getLogger(__name__)


def is_copy_only_path(path, context):
    """Check whether the given `path` should only be copied and not rendered.

    Returns True if `path` matches a pattern in the given `context` dict,
    otherwise False.

    :param path: A file-system path referring to a file or dir that
        should be rendered or just copied.
    :param context: cookiecutter context.
    """
    try:
        for dont_render in context['cookiecutter']['_copy_without_render']:
            if fnmatch.fnmatch(path, dont_render):
                return True
    except KeyError:
        return False

    return False


def apply_overwrites_to_context(context, overwrite_context):
    """Modify the given context in place based on the overwrite_context."""
    for variable, overwrite in overwrite_context.items():
        if variable not in context:
            # Do not include variables which are not used in the template
            continue

        context_value = context[variable]

        if isinstance(context_value, list):
            # We are dealing with a choice variable
            if overwrite in context_value:
                # This overwrite is actually valid for the given context
                # Let's set it as default (by definition first item in list)
                # see ``cookiecutter.prompt.prompt_choice_for_config``
                context_value.remove(overwrite)
                context_value.insert(0, overwrite)
        else:
            # Simply overwrite the value for this variable
            context[variable] = overwrite


def generate_context(context_file='cookiecutter.json', default_context=None,
                     extra_context=None):
    """Generate the context for a Cookiecutter project template.

    Loads the JSON file as a Python object, with key being the JSON filename.

    :param context_file: JSON file containing key/value pairs for populating
        the cookiecutter's variables.
    :param default_context: Dictionary containing config to take into account.
    :param extra_context: Dictionary containing configuration overrides
    """
    context = {}

    try:
        with open(context_file) as file_handle:
            obj = json.load(file_handle, object_pairs_hook=OrderedDict)
    except ValueError as e:
        # JSON decoding error.  Let's throw a new exception that is more
        # friendly for the developer or user.
        full_fpath = os.path.abspath(context_file)
        json_exc_message = str(e)
        our_exc_message = (
            'JSON decoding error while loading "{0}".  Decoding'
            ' error details: "{1}"'.format(full_fpath, json_exc_message))
        raise ContextDecodingException(our_exc_message)

    # Add the Python object to the context dictionary
    file_name = os.path.split(context_file)[1]
    file_stem = file_name.split('.')[0]
    context[file_stem] = obj

    # Overwrite context variable defaults with the default context from the
    # user's global config, if available
    if default_context:
        apply_overwrites_to_context(obj, default_context)
    if extra_context:
        apply_overwrites_to_context(obj, extra_context)

    logger.debug('Context generated is {}'.format(context))
    return context


def generate_file(project_dir, infile, context, env):
    """Render filename of infile as name of outfile, handle infile correctly.

    Dealing with infile appropriately:

        a. If infile is a binary file, copy it over without rendering.
        b. If infile is a text file, render its contents and write the
           rendered infile to outfile.

    Precondition:

        When calling `generate_file()`, the root template dir must be the
        current working directory. Using `utils.work_in()` is the recommended
        way to perform this directory change.

    :param project_dir: Absolute path to the resulting generated project.
    :param infile: Input file to generate the file from. Relative to the root
        template dir.
    :param context: Dict for populating the cookiecutter's variables.
    :param env: Jinja2 template execution environment.
    """
    logger.debug('Processing file {}'.format(infile))

    # Render the path to the output file (not including the root project dir)
    outfile_tmpl = env.from_string(infile)

    outfile = os.path.join(project_dir, outfile_tmpl.render(**context))
    file_name_is_empty = os.path.isdir(outfile)
    if file_name_is_empty:
        logger.debug('The resulting file name is empty: {0}'.format(outfile))
        return

    logger.debug('Created file at {0}'.format(outfile))

    # Just copy over binary files. Don't render.
    logger.debug("Check {} to see if it's a binary".format(infile))
    if is_binary(infile):
        logger.debug(
            'Copying binary {} to {} without rendering'
            ''.format(infile, outfile)
        )
        shutil.copyfile(infile, outfile)
    else:
        # Force fwd slashes on Windows for get_template
        # This is a by-design Jinja issue
        infile_fwd_slashes = infile.replace(os.path.sep, '/')

        # Render the file
        try:
            tmpl = env.get_template(infile_fwd_slashes)
        except TemplateSyntaxError as exception:
            # Disable translated so that printed exception contains verbose
            # information about syntax error location
            exception.translated = False
            raise
        rendered_file = tmpl.render(**context)

        logger.debug('Writing contents to file {}'.format(outfile))

        with io.open(outfile, 'w', encoding='utf-8') as fh:
            fh.write(rendered_file)

    # Apply file permissions to output file
    shutil.copymode(infile, outfile)


def render_and_create_dir(dirname, context, output_dir, environment,
                          overwrite_if_exists=False):
    """Render name of a directory, create the directory, return its path."""
    name_tmpl = environment.from_string(dirname)
    rendered_dirname = name_tmpl.render(**context)

    dir_to_create = os.path.normpath(
        os.path.join(output_dir, rendered_dirname)
    )

    logger.debug('Rendered dir {} must exist in output_dir {}'.format(
        dir_to_create,
        output_dir
    ))

    output_dir_exists = os.path.exists(dir_to_create)

    if output_dir_exists:
        if overwrite_if_exists:
            logger.debug(
                'Output directory {} already exists,'
                'overwriting it'.format(dir_to_create)
            )
        else:
            msg = 'Error: "{}" directory already exists'.format(dir_to_create)
            raise OutputDirExistsException(msg)
    else:
        make_sure_path_exists(dir_to_create)

    return dir_to_create, not output_dir_exists


def ensure_dir_is_templated(dirname):
    """Ensure that dirname is a templated directory name."""
    if '{{' in dirname and '}}' in dirname:
        return True
    else:
        raise NonTemplatedInputDirException


def _run_hook_from_repo_dir(repo_dir, hook_name, project_dir, context,
                            delete_project_on_failure):
    """Run hook from repo directory, clean project directory if hook fails.

    :param repo_dir: Project template input directory.
    :param hook_name: The hook to execute.
    :param project_dir: The directory to execute the script from.
    :param context: Cookiecutter project context.
    :param delete_project_on_failure: Delete the project directory on hook
        failure?
    """
    with work_in(repo_dir):
        try:
            run_hook(hook_name, project_dir, context)
        except FailedHookException:
            if delete_project_on_failure:
                rmtree(project_dir)
            logger.error(
                "Stopping generation because {} hook "
                "script didn't exit successfully".format(hook_name)
            )
            raise


def generate_files(repo_dir, context=None, output_dir='.',
                   overwrite_if_exists=False):
    """Render the templates and saves them to files.

    :param repo_dir: Project template input directory.
    :param context: Dict for populating the template's variables.
    :param output_dir: Where to output the generated project dir into.
    :param overwrite_if_exists: Overwrite the contents of the output directory
        if it exists.
    """
    template_dir = find_template(repo_dir)
    logger.debug('Generating project from {}...'.format(template_dir))
    context = context or {}

    unrendered_dir = os.path.split(template_dir)[1]
    ensure_dir_is_templated(unrendered_dir)
    env = StrictEnvironment(
        context=context,
        keep_trailing_newline=True,
    )
    try:
        project_dir, output_directory_created = render_and_create_dir(
            unrendered_dir,
            context,
            output_dir,
            env,
            overwrite_if_exists
        )
    except UndefinedError as err:
        msg = "Unable to create project directory '{}'".format(unrendered_dir)
        raise UndefinedVariableInTemplate(msg, err, context)

    # We want the Jinja path and the OS paths to match. Consequently, we'll:
    #   + CD to the template folder
    #   + Set Jinja's path to '.'
    #
    #  In order to build our files to the correct folder(s), we'll use an
    # absolute path for the target folder (project_dir)

    project_dir = os.path.abspath(project_dir)
    logger.debug('Project directory is {}'.format(project_dir))

    # if we created the output directory, then it's ok to remove it
    # if rendering fails
    delete_project_on_failure = output_directory_created

    _run_hook_from_repo_dir(
        repo_dir,
        'pre_gen_project',
        project_dir,
        context,
        delete_project_on_failure
    )

    with work_in(template_dir):
        env.loader = FileSystemLoader('.')

        for root, dirs, files in os.walk('.'):
            # We must separate the two types of dirs into different lists.
            # The reason is that we don't want ``os.walk`` to go through the
            # unrendered directories, since they will just be copied.
            copy_dirs = []
            render_dirs = []

            for d in dirs:
                d_ = os.path.normpath(os.path.join(root, d))
                # We check the full path, because that's how it can be
                # specified in the ``_copy_without_render`` setting, but
                # we store just the dir name
                if is_copy_only_path(d_, context):
                    copy_dirs.append(d)
                else:
                    render_dirs.append(d)

            for copy_dir in copy_dirs:
                indir = os.path.normpath(os.path.join(root, copy_dir))
                outdir = os.path.normpath(os.path.join(project_dir, indir))
                logger.debug(
                    'Copying dir {} to {} without rendering'
                    ''.format(indir, outdir)
                )
                shutil.copytree(indir, outdir)

            # We mutate ``dirs``, because we only want to go through these dirs
            # recursively
            dirs[:] = render_dirs
            for d in dirs:
                unrendered_dir = os.path.join(project_dir, root, d)
                try:
                    render_and_create_dir(
                        unrendered_dir,
                        context,
                        output_dir,
                        env,
                        overwrite_if_exists
                    )
                except UndefinedError as err:
                    if delete_project_on_failure:
                        rmtree(project_dir)
                    _dir = os.path.relpath(unrendered_dir, output_dir)
                    msg = "Unable to create directory '{}'".format(_dir)
                    raise UndefinedVariableInTemplate(msg, err, context)

            for f in files:
                infile = os.path.normpath(os.path.join(root, f))
                if is_copy_only_path(infile, context):
                    outfile_tmpl = env.from_string(infile)
                    outfile_rendered = outfile_tmpl.render(**context)
                    outfile = os.path.join(project_dir, outfile_rendered)
                    logger.debug(
                        'Copying file {} to {} without rendering'
                        ''.format(infile, outfile)
                    )
                    shutil.copyfile(infile, outfile)
                    shutil.copymode(infile, outfile)
                    continue
                try:
                    generate_file(project_dir, infile, context, env)
                except UndefinedError as err:
                    if delete_project_on_failure:
                        rmtree(project_dir)
                    msg = "Unable to create file '{}'".format(infile)
                    raise UndefinedVariableInTemplate(msg, err, context)

    _run_hook_from_repo_dir(
        repo_dir,
        'post_gen_project',
        project_dir,
        context,
        delete_project_on_failure
    )

    return project_dir
