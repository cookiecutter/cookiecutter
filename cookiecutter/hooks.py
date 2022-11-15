"""Functions for discovering and executing various cookiecutter hooks."""
import errno
import json
import locale
import logging
import os
import subprocess  # nosec
import sys
import tempfile
from json import JSONDecodeError

from cookiecutter import utils
from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import FailedHookException
from subprocess import PIPE, TimeoutExpired  # nosec

logger = logging.getLogger(__name__)

_HOOKS = [
    'pre_context',
    'pre_gen_project',
    'post_gen_project',
]
EXIT_SUCCESS = 0


def valid_hook(hook_file, hook_name):
    """Determine if a hook file is valid.

    :param hook_file: The hook file to consider for validity
    :param hook_name: The hook to find
    :return: The hook file validity
    """
    filename = os.path.basename(hook_file)
    basename = os.path.splitext(filename)[0]

    matching_hook = basename == hook_name
    supported_hook = basename in _HOOKS
    backup_file = filename.endswith('~')

    return matching_hook and supported_hook and not backup_file


def find_hook(hook_name, hooks_dir='hooks'):
    """Return a dict of all hook scripts provided.

    Must be called with the project template as the current working directory.
    Dict's key will be the hook/script's name, without extension, while values
    will be the absolute path to the script. Missing scripts will not be
    included in the returned dict.

    :param hook_name: The hook to find
    :param hooks_dir: The hook directory in the template
    :return: The absolute path to the hook script or None
    """
    logger.debug('hooks_dir is %s', os.path.abspath(hooks_dir))

    if not os.path.isdir(hooks_dir):
        logger.debug('No hooks/dir in template_dir')
        return None

    scripts = []
    for hook_file in os.listdir(hooks_dir):
        if valid_hook(hook_file, hook_name):
            scripts.append(os.path.abspath(os.path.join(hooks_dir, hook_file)))

    if len(scripts) == 0:
        return None
    return scripts


def run_script(script_path, cwd='.'):
    """Execute a script from a working directory.

    :param script_path: Absolute path to the script to run.
    :param cwd: The directory to run the script from.
    """
    run_thru_shell = sys.platform.startswith('win')
    if script_path.endswith('.py'):
        script_command = [sys.executable, script_path]
    else:
        script_command = [script_path]

    utils.make_executable(script_path)

    try:
        encoding = locale.getpreferredencoding()
        proc = subprocess.Popen(  # nosec
            script_command,
            shell=run_thru_shell,
            cwd=cwd,
            stdout=PIPE,
            stderr=PIPE,
            encoding=encoding,
        )
        try:
            outs, errs = proc.communicate()
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
            logger.error(f'Hook script killed after timeout: {errs}')
            raise FailedHookException(f'Hook script killed after timeout: {errs}')

        if proc.returncode != EXIT_SUCCESS:
            logger.error(f'Hook script failed with error message: {errs}')
            raise FailedHookException(
                f'Hook script failed (exit status: {proc.returncode})'
            )
        if errs:
            logger.warning(
                f'Hook script did not fail, but produced some error message: {errs}'
            )

        try:
            return json.loads(outs)
        except JSONDecodeError as err:
            logger.info(f'Hook script output is not well-formed JSON: {err.msg}')
            return outs

    except OSError as err:
        if err.errno == errno.ENOEXEC:
            raise FailedHookException(
                'Hook script failed, might be an empty file or missing a shebang'
            ) from err
        raise FailedHookException(f'Hook script failed (error: {err})') from err


def run_script_with_context(script_path, cwd, context):
    """Execute a script after rendering it with Jinja.

    :param script_path: Absolute path to the script to run.
    :param cwd: The directory to run the script from.
    :param context: Cookiecutter project template context.
    """
    _, extension = os.path.splitext(script_path)

    with open(script_path, encoding='utf-8') as file:
        contents = file.read()

    with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix=extension) as temp:
        env = StrictEnvironment(context=context, keep_trailing_newline=True)
        template = env.from_string(contents)
        output = template.render(**context)
        temp.write(output.encode('utf-8'))

    return run_script(temp.name, cwd)


def run_hook(hook_name, project_dir, context):
    """
    Try to find and execute a hook from the specified project directory.

    :param hook_name: The hook to execute.
    :param project_dir: The directory to execute the script from.
    :param context: Cookiecutter project context.
    """
    scripts = find_hook(hook_name)
    if not scripts:
        logger.debug('No %s hook found', hook_name)
        return context
    logger.debug('Running hook %s', hook_name)
    for script in scripts:
        payload = run_script_with_context(script, project_dir, context)
        if 'pre_context' == hook_name:
            if not isinstance(payload, dict):
                raise FailedHookException(
                    f'Pre-Context Hook script failed to provide JSON, got: {payload}'
                )
            for key, value in payload.items():
                if key in context['cookiecutter']:
                    old = context["cookiecutter"][key]
                    logger.info(
                        f'Replacing context[cookiecutter][{key}] = {old} with {value}'
                    )
                context['cookiecutter'][key] = value

    return context
