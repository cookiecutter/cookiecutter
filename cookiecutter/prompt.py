"""Functions for prompting the user for project info."""
import json
from collections import OrderedDict

import click
from jinja2.exceptions import UndefinedError

from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import UndefinedVariableInTemplate


def read_user_variable(var_name, default_value):
    """Prompt user for variable and return the entered value or given default.

    :param str var_name: Variable of the context to query the user
    :param default_value: Value that will be returned if no input happens
    """
    # Please see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    return click.prompt(var_name, default=default_value)


def read_user_yes_no(question, default_value):
    """Prompt the user to reply with 'yes' or 'no' (or equivalent values).

    Note:
      Possible choices are 'true', '1', 'yes', 'y' or 'false', '0', 'no', 'n'

    :param str question: Question to the user
    :param default_value: Value that will be returned if no input happens
    """
    # Please see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    return click.prompt(question, default=default_value, type=click.BOOL)


def read_repo_password(question):
    """Prompt the user to enter a password.

    :param str question: Question to the user
    """
    # Please see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    return click.prompt(question, hide_input=True)


def read_user_choice(var_name, options):
    """Prompt the user to choose from several options for the given variable.

    The first item will be returned if no input happens.

    :param str var_name: Variable as specified in the context
    :param list options: Sequence of options that are available to select from
    :return: Exactly one item of ``options`` that has been chosen by the user
    """
    # Please see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    if not isinstance(options, list):
        raise TypeError

    if not options:
        raise ValueError

    choice_map = OrderedDict(
        ('{}'.format(i), value) for i, value in enumerate(options, 1)
    )
    choices = choice_map.keys()
    default = '1'

    choice_lines = ['{} - {}'.format(*c) for c in choice_map.items()]
    prompt = '\n'.join(
        (
            'Select {}:'.format(var_name),
            '\n'.join(choice_lines),
            'Choose from {}'.format(', '.join(choices)),
        )
    )

    user_choice = click.prompt(
        prompt, type=click.Choice(choices), default=default, show_choices=False
    )
    return choice_map[user_choice]


def process_json(user_value):
    """Load user-supplied value as a JSON dict.

    :param str user_value: User-supplied value to load as a JSON dict
    """
    try:
        user_dict = json.loads(user_value, object_pairs_hook=OrderedDict)
    except Exception:
        # Leave it up to click to ask the user again
        raise click.UsageError('Unable to decode to JSON.')

    if not isinstance(user_dict, dict):
        # Leave it up to click to ask the user again
        raise click.UsageError('Requires JSON dict.')

    return user_dict


def read_user_dict(var_name, default_value):
    """Prompt the user to provide a dictionary of data.

    :param str var_name: Variable as specified in the context
    :param default_value: Value that will be returned if no input is provided
    :return: A Python dictionary to use in the context.
    """
    # Please see https://click.palletsprojects.com/en/7.x/api/#click.prompt
    if not isinstance(default_value, dict):
        raise TypeError

    default_display = 'default'

    user_value = click.prompt(
        var_name, default=default_display, type=click.STRING, value_proc=process_json
    )

    if user_value == default_display:
        # Return the given default w/o any processing
        return default_value
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
    if raw is None:
        return None
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

    rendered_template = template.render(cookiecutter=cookiecutter_dict)
    return rendered_template


def prompt_choice_for_config(cookiecutter_dict, env, key, options, no_input):
    """Prompt user with a set of options to choose from.

    Each of the possible choices is rendered beforehand.
    """
    rendered_options = [render_variable(env, raw, cookiecutter_dict) for raw in options]

    if no_input:
        return rendered_options[0]
    return read_user_choice(key, rendered_options)


def prompt_for_config(context, no_input=False):
    """Prompt user to enter a new config.

    :param dict context: Source for field names and sample values.
    :param no_input: Prompt the user at command line for manual configuration?
    """
    cookiecutter_dict = OrderedDict([])
    env = StrictEnvironment(context=context)

    # First pass: Handle simple and raw variables, plus choices.
    # These must be done first because the dictionaries keys and
    # values might refer to them.
    for key, raw in context['cookiecutter'].items():
        if key.startswith('_') and not key.startswith('__'):
            cookiecutter_dict[key] = raw
            continue
        elif key.startswith('__'):
            cookiecutter_dict[key] = render_variable(env, raw, cookiecutter_dict)
            continue

        try:
            if isinstance(raw, list):
                # We are dealing with a choice variable
                val = prompt_choice_for_config(
                    cookiecutter_dict, env, key, raw, no_input
                )
                cookiecutter_dict[key] = val
            elif not isinstance(raw, dict):
                # We are dealing with a regular variable
                val = render_variable(env, raw, cookiecutter_dict)

                if not no_input:
                    val = read_user_variable(key, val)

                cookiecutter_dict[key] = val
        except UndefinedError as err:
            msg = "Unable to render variable '{}'".format(key)
            raise UndefinedVariableInTemplate(msg, err, context)

    # Second pass; handle the dictionaries.
    for key, raw in context['cookiecutter'].items():
        # Skip private type dicts not ot be rendered.
        if key.startswith('_') and not key.startswith('__'):
            continue

        try:
            if isinstance(raw, dict):
                # We are dealing with a dict variable
                val = render_variable(env, raw, cookiecutter_dict)

                if not no_input and not key.startswith('__'):
                    val = read_user_dict(key, val)

                cookiecutter_dict[key] = val
        except UndefinedError as err:
            msg = "Unable to render variable '{}'".format(key)
            raise UndefinedVariableInTemplate(msg, err, context)

    return cookiecutter_dict
