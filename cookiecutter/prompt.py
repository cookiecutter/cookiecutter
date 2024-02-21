"""Functions for prompting the user for project info."""

import json
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path

from jinja2.exceptions import UndefinedError
from rich.prompt import Confirm, InvalidResponse, Prompt, PromptBase

from cookiecutter.exceptions import UndefinedVariableInTemplate
from cookiecutter.utils import create_env_with_context, rmtree


def read_user_variable(var_name, default_value, prompts=None, prefix=""):
    """Prompt user for variable and return the entered value or given default.

    :param str var_name: Variable of the context to query the user
    :param default_value: Value that will be returned if no input happens
    """
    question = (
        prompts[var_name]
        if prompts and var_name in prompts.keys() and prompts[var_name]
        else var_name
    )

    while True:
        variable = Prompt.ask(f"{prefix}{question}", default=default_value)
        if variable is not None:
            break

    return variable


class YesNoPrompt(Confirm):
    """A prompt that returns a boolean for yes/no questions."""

    yes_choices = ["1", "true", "t", "yes", "y", "on"]
    no_choices = ["0", "false", "f", "no", "n", "off"]

    def process_response(self, value: str) -> bool:
        """Convert choices to a bool."""
        value = value.strip().lower()
        if value in self.yes_choices:
            return True
        elif value in self.no_choices:
            return False
        else:
            raise InvalidResponse(self.validate_error_message)


def read_user_yes_no(var_name, default_value, prompts=None, prefix=""):
    """Prompt the user to reply with 'yes' or 'no' (or equivalent values).

    - These input values will be converted to ``True``:
      "1", "true", "t", "yes", "y", "on"
    - These input values will be converted to ``False``:
      "0", "false", "f", "no", "n", "off"

    Actual parsing done by :func:`prompt`; Check this function codebase change in
    case of unexpected behaviour.

    :param str question: Question to the user
    :param default_value: Value that will be returned if no input happens
    """
    question = (
        prompts[var_name]
        if prompts and var_name in prompts.keys() and prompts[var_name]
        else var_name
    )
    return YesNoPrompt.ask(f"{prefix}{question}", default=default_value)


def read_repo_password(question):
    """Prompt the user to enter a password.

    :param str question: Question to the user
    """
    return Prompt.ask(question, password=True)


def read_user_choice(var_name, options, prompts=None, prefix=""):
    """Prompt the user to choose from several options for the given variable.

    The first item will be returned if no input happens.

    :param str var_name: Variable as specified in the context
    :param list options: Sequence of options that are available to select from
    :return: Exactly one item of ``options`` that has been chosen by the user
    """
    if not isinstance(options, list):
        raise TypeError

    if not options:
        raise ValueError

    choice_map = OrderedDict((f'{i}', value) for i, value in enumerate(options, 1))
    choices = choice_map.keys()

    question = f"Select {var_name}"
    choice_lines = [
        '    [bold magenta]{}[/] - [bold]{}[/]'.format(*c) for c in choice_map.items()
    ]

    # Handle if human-readable prompt is provided
    if prompts and var_name in prompts.keys():
        if isinstance(prompts[var_name], str):
            question = prompts[var_name]
        else:
            if "__prompt__" in prompts[var_name]:
                question = prompts[var_name]["__prompt__"]
            choice_lines = [
                (
                    f"    [bold magenta]{i}[/] - [bold]{prompts[var_name][p]}[/]"
                    if p in prompts[var_name]
                    else f"    [bold magenta]{i}[/] - [bold]{p}[/]"
                )
                for i, p in choice_map.items()
            ]

    prompt = '\n'.join(
        (
            f"{prefix}{question}",
            "\n".join(choice_lines),
            "    Choose from",
        )
    )

    user_choice = Prompt.ask(prompt, choices=list(choices), default=list(choices)[0])
    return choice_map[user_choice]


DEFAULT_DISPLAY = 'default'


def process_json(user_value, default_value=None):
    """Load user-supplied value as a JSON dict.

    :param str user_value: User-supplied value to load as a JSON dict
    """
    try:
        user_dict = json.loads(user_value, object_pairs_hook=OrderedDict)
    except Exception as error:
        # Leave it up to click to ask the user again
        raise InvalidResponse('Unable to decode to JSON.') from error

    if not isinstance(user_dict, dict):
        # Leave it up to click to ask the user again
        raise InvalidResponse('Requires JSON dict.')

    return user_dict


class JsonPrompt(PromptBase[dict]):
    """A prompt that returns a dict from JSON string."""

    default = None
    response_type = dict
    validate_error_message = "[prompt.invalid]  Please enter a valid JSON string"

    def process_response(self, value: str) -> dict:
        """Convert choices to a dict."""
        return process_json(value, self.default)


def read_user_dict(var_name, default_value, prompts=None, prefix=""):
    """Prompt the user to provide a dictionary of data.

    :param str var_name: Variable as specified in the context
    :param default_value: Value that will be returned if no input is provided
    :return: A Python dictionary to use in the context.
    """
    if not isinstance(default_value, dict):
        raise TypeError

    question = (
        prompts[var_name]
        if prompts and var_name in prompts.keys() and prompts[var_name]
        else var_name
    )
    user_value = JsonPrompt.ask(
        f"{prefix}{question} [cyan bold]({DEFAULT_DISPLAY})[/]",
        default=default_value,
        show_default=False,
    )
    return user_value


def render_variable(env, raw, cookiecutter_dict):
    """Render the next variable to be displayed in the user prompt.

    Inside the prompting taken from the cookiecutter.json file, this renders
    the next variable. For example, if a project_name is "Peanut Butter
    Cookie", the repo_name could be be rendered with:

        `{{ cookiecutter.project_name.replace(" ", "_") }}`.

    This is then presented to the user as the default.

    :param Environment env: A Jinja2 Environment object.
    :param raw: The next value to be prompted for by the user.
    :param dict cookiecutter_dict: The current context as it's gradually
        being populated with variables.
    :return: The rendered value for the default variable.
    """
    if raw is None or isinstance(raw, bool):
        return raw
    elif isinstance(raw, dict):
        return {
            render_variable(env, k, cookiecutter_dict): render_variable(
                env, v, cookiecutter_dict
            )
            for k, v in raw.items()
        }
    elif isinstance(raw, list):
        return [render_variable(env, v, cookiecutter_dict) for v in raw]
    elif not isinstance(raw, str):
        raw = str(raw)

    template = env.from_string(raw)

    return template.render(cookiecutter=cookiecutter_dict)


def _prompts_from_options(options: dict) -> dict:
    """Process template options and return friendly prompt information."""
    prompts = {"__prompt__": "Select a template"}
    for option_key, option_value in options.items():
        title = str(option_value.get("title", option_key))
        description = option_value.get("description", option_key)
        label = title if title == description else f"{title} ({description})"
        prompts[option_key] = label
    return prompts


def prompt_choice_for_template(key, options, no_input):
    """Prompt user with a set of options to choose from.

    :param no_input: Do not prompt for user input and return the first available option.
    """
    opts = list(options.keys())
    prompts = {"templates": _prompts_from_options(options)}
    return opts[0] if no_input else read_user_choice(key, opts, prompts, "")


def prompt_choice_for_config(
    cookiecutter_dict, env, key, options, no_input, prompts=None, prefix=""
):
    """Prompt user with a set of options to choose from.

    :param no_input: Do not prompt for user input and return the first available option.
    """
    rendered_options = [render_variable(env, raw, cookiecutter_dict) for raw in options]
    if no_input:
        return rendered_options[0]
    return read_user_choice(key, rendered_options, prompts, prefix)


def prompt_for_config(context, no_input=False):
    """Prompt user to enter a new config.

    :param dict context: Source for field names and sample values.
    :param no_input: Do not prompt for user input and use only values from context.
    """
    cookiecutter_dict = OrderedDict([])
    env = create_env_with_context(context)
    prompts = context['cookiecutter'].pop('__prompts__', {})

    # First pass: Handle simple and raw variables, plus choices.
    # These must be done first because the dictionaries keys and
    # values might refer to them.
    count = 0
    all_prompts = context['cookiecutter'].items()
    visible_prompts = [k for k, _ in all_prompts if not k.startswith("_")]
    size = len(visible_prompts)
    for key, raw in all_prompts:
        if key.startswith('_') and not key.startswith('__'):
            cookiecutter_dict[key] = raw
            continue
        elif key.startswith('__'):
            cookiecutter_dict[key] = render_variable(env, raw, cookiecutter_dict)
            continue

        if not isinstance(raw, dict):
            count += 1
            prefix = f"  [dim][{count}/{size}][/] "

        try:
            if isinstance(raw, list):
                # We are dealing with a choice variable
                val = prompt_choice_for_config(
                    cookiecutter_dict, env, key, raw, no_input, prompts, prefix
                )
                cookiecutter_dict[key] = val
            elif isinstance(raw, bool):
                # We are dealing with a boolean variable
                if no_input:
                    cookiecutter_dict[key] = render_variable(
                        env, raw, cookiecutter_dict
                    )
                else:
                    cookiecutter_dict[key] = read_user_yes_no(key, raw, prompts, prefix)
            elif not isinstance(raw, dict):
                # We are dealing with a regular variable
                val = render_variable(env, raw, cookiecutter_dict)

                if not no_input:
                    val = read_user_variable(key, val, prompts, prefix)

                cookiecutter_dict[key] = val
        except UndefinedError as err:
            msg = f"Unable to render variable '{key}'"
            raise UndefinedVariableInTemplate(msg, err, context) from err

    # Second pass; handle the dictionaries.
    for key, raw in context['cookiecutter'].items():
        # Skip private type dicts not to be rendered.
        if key.startswith('_') and not key.startswith('__'):
            continue

        try:
            if isinstance(raw, dict):
                # We are dealing with a dict variable
                count += 1
                prefix = f"  [dim][{count}/{size}][/] "
                val = render_variable(env, raw, cookiecutter_dict)

                if not no_input and not key.startswith('__'):
                    val = read_user_dict(key, val, prompts, prefix)

                cookiecutter_dict[key] = val
        except UndefinedError as err:
            msg = f"Unable to render variable '{key}'"
            raise UndefinedVariableInTemplate(msg, err, context) from err

    return cookiecutter_dict


def choose_nested_template(context: dict, repo_dir: str, no_input: bool = False) -> str:
    """Prompt user to select the nested template to use.

    :param context: Source for field names and sample values.
    :param repo_dir: Repository directory.
    :param no_input: Do not prompt for user input and use only values from context.
    :returns: Path to the selected template.
    """
    cookiecutter_dict = OrderedDict([])
    env = create_env_with_context(context)
    prefix = ""
    prompts = context['cookiecutter'].pop('__prompts__', {})
    key = "templates"
    config = context['cookiecutter'].get(key, {})
    if config:
        # Pass
        val = prompt_choice_for_template(key, config, no_input)
        template = config[val]["path"]
    else:
        # Old style
        key = "template"
        config = context['cookiecutter'].get(key, [])
        val = prompt_choice_for_config(
            cookiecutter_dict, env, key, config, no_input, prompts, prefix
        )
        template = re.search(r'\((.+)\)', val).group(1)

    template = Path(template) if template else None
    if not (template and not template.is_absolute()):
        raise ValueError("Illegal template path")

    repo_dir = Path(repo_dir).resolve()
    template_path = (repo_dir / template).resolve()
    # Return path as string
    return f"{template_path}"


def prompt_and_delete(path, no_input=False):
    """
    Ask user if it's okay to delete the previously-downloaded file/directory.

    If yes, delete it. If no, checks to see if the old version should be
    reused. If yes, it's reused; otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    :return: True if the content was deleted
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            f"You've downloaded {path} before. Is it okay to delete and re-download it?"
        )

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
        return True
    else:
        ok_to_reuse = read_user_yes_no(
            "Do you want to re-use the existing version?", 'yes'
        )

        if ok_to_reuse:
            return False

        sys.exit()
