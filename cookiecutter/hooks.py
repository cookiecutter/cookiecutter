#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.hooks
------------------

Functions for discovering and executing various cookiecutter hooks.
"""

import io
import logging
import os
import subprocess
import sys
import tempfile
import errno

from jinja2 import Template

from pydoc import locate
from cookiecutter import utils
from .exceptions import FailedHookException, BadSerializedStringFormat
from .serialization import SerializationFacade, make_persistent
from .config import get_from_context


_HOOKS = [
    'pre_gen_project',
    'post_gen_project',
    # TODO: other hooks should be listed here
]
EXIT_SUCCESS = 0


def find_hooks():
    """
    Must be called with the project template as the current working directory.
    Returns a dict of all hook scripts provided.
    Dict's key will be the hook/script's name, without extension, while
    values will be the absolute path to the script.
    Missing scripts will not be included in the returned dict.
    """
    hooks_dir = 'hooks'
    r = {}
    logging.debug('hooks_dir is {0}'.format(hooks_dir))
    if not os.path.isdir(hooks_dir):
        logging.debug('No hooks/ dir in template_dir')
        return r
    for f in os.listdir(hooks_dir):
        basename = os.path.splitext(os.path.basename(f))[0]
        if basename in _HOOKS:
            r[basename] = os.path.abspath(os.path.join(hooks_dir, f))
    return r


def run_script_with_context(script_path, cwd, context):
    """
    Executes a script either after rendering with it Jinja or in place without
    template rendering.

    :param script_path: Absolute path to the script to run.
    :param cwd: The directory to run the script from.
    :param context: Cookiecutter project template context.
    """
    lazy_load_from_extra_dir(os.path.dirname(os.path.dirname(script_path)))

    script = __new_script(context, script_path)

    try:
        serializer = __new_serialization_facade(context)
        make_persistent(serializer)

        result = __do_run_script(
            script, cwd, serializer.serialize(context).encode())

        return serializer.deserialize(result[0].decode())

    except BadSerializedStringFormat:
        return context


def run_hook(hook_name, project_dir, context):
    """
    Try to find and execute a hook from the specified project directory.

    :param hook_name: The hook to execute.
    :param project_dir: The directory to execute the script from.
    :param context: Cookiecutter project context.
    """
    script = find_hooks().get(hook_name)
    if script is None:
        logging.debug('No hooks found')
        return context

    return run_script_with_context(script, project_dir, context)


def lazy_load_from_extra_dir(template_dir):
    """
    permit lazy load from the 'extra' directory
    :param template_dir: the project template directory
    """
    extra_dir = os.path.abspath(os.path.join(template_dir, 'extra'))
    if os.path.exists(extra_dir) and extra_dir not in sys.path:
        sys.path.insert(1, extra_dir)


def __create_renderable_hook(script_path, context):
    """
    Create a renderable hook by copying the real hook and applying the template

    :param script_path: Absolute path to the base hook.
    :param context: Cookiecutter project template context.
    """
    _, extension = os.path.splitext(script_path)
    contents = io.open(script_path, 'r', encoding='utf-8').read()
    with tempfile.NamedTemporaryFile(
        delete=False,
        mode='wb',
        suffix=extension
    ) as temp:
        output = Template(contents).render(**context)
        temp.write(output.encode('utf-8'))

    return temp.name


def __get_script_command(script_path):
    """
    Get the executable command of a given script

    :param script_path: Absolute path to the script to run.
    """
    if script_path.endswith('.py'):
        script_command = [sys.executable, script_path]
    else:
        script_command = [script_path]

    utils.make_executable(script_path)

    return script_command


def __do_run_script(script_path, cwd, serialized_context):
    """
    Executes a script wrinting the given serialized context to its standard
    input stream.

    :param script_path: Absolute path to the script to run.
    :param cwd: The directory to run the script from.
    :param serialized_context: Serialized Cookiecutter project template
                               context.
    """
    result = (serialized_context, b'')
    run_thru_shell = sys.platform.startswith('win')

    os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)

    proc = subprocess.Popen(
        __get_script_command(script_path),
        shell=run_thru_shell,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        result = proc.communicate(serialized_context)
    except OSError as e:
        if e.errno == errno.EINVAL and run_thru_shell:
            logging.warn(
                'Popen.communicate failed certainly ' +
                'because of the issue #19612'
            )
            pass
        else:
            raise e

    exit_status = proc.wait()
    if exit_status != EXIT_SUCCESS:
        raise FailedHookException(
            "Hook script failed (exit status: %d): \n%s" %
            (exit_status, result[1]))

    return result


def __get_from_context(context, key, default=None):
    """
    config.get_from_context wrapper

    :param context: context to search in
    :param key: key to look for
    :param default: default value to get back if key does not exist
    """
    result = get_from_context(context, key)

    return result if result is not None else get_from_context(
        context, 'cookiecutter.' + key, default)


def __new_serialization_facade(context):
    """
    serialization facade factory function

    :param context: current context
    """
    serializers = {}
    usetype = __get_from_context(context, '_serializers.use', 'json')
    classes = __get_from_context(context, '_serializers.classes', [])
    for type in classes:
        serializers[type] = locate(classes[type], 1)

    return SerializationFacade(serializers).use(usetype)


def __new_script(context, script_path):
    """
    script factory function

    :param context: current context
    :param script_path: absolute path to the script to run
    """
    return script_path if __get_from_context(
        context, '_run_hook_in_place', False) else __create_renderable_hook(
            script_path, context)
