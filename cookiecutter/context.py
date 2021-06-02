"""
Parses a cookiecutter JSON content and prompts the users for input.

Process the version 2 cookiecutter context (previously loaded via
cookiecutter.json) and handle any user input that might be associated with
initializing the settings defined in the 'variables' OrderedDict part of the
context.

This module produces a dictionary used later by the jinja2 template engine to
generate files.

Based on the source code written by @hackebrot see:
https://github.com/audreyr/cookiecutter/pull/848
https://github.com/hackebrot/cookiecutter/tree/new-context-format

"""

import collections
import json
import logging
from operator import eq, ge, gt, le, lt, ne
from typing import Dict

import click
from jinja2 import Environment

from cookiecutter.exceptions import InvalidConfiguration
from cookiecutter.schema import validate

logger = logging.getLogger(__name__)

DEFAULT_PROMPT = 'Please enter a value for "{variable.name}"'

op_mapping = {'==': eq, '<=': le, '<': lt, '>=': ge, '>': gt, '!=': ne}


def prompt_string(variable, default):
    """Prompts the user for a text value."""
    return click.prompt(variable.prompt, default=default, type=click.STRING,)


def prompt_boolean(variable, default):
    """Prompts the user for a boolean."""
    return click.prompt(variable.prompt, default=default, type=click.BOOL,)


def prompt_int(variable, default):
    """Prompts the user for an int."""
    return click.prompt(variable.prompt, default=default, type=click.INT,)


def prompt_float(variable, default):
    """Prompts the user for float."""
    return click.prompt(variable.prompt, default=default, type=click.FLOAT,)


def prompt_uuid(variable, default):
    """Prompts the user for a uuid."""
    return click.prompt(variable.prompt, default=default, type=click.UUID,)


def prompt_json(variable, default):
    """Prompts the user for a JSON entry."""
    # The JSON object from cookiecutter.json might be very large
    # We only show 'default'

    default_json = 'default'

    def process_json(user_value):
        try:
            return json.loads(user_value, object_pairs_hook=collections.OrderedDict,)
        except ValueError:
            # json.decoder.JSONDecodeError raised in Python 3.5, 3.6
            # but it inherits from ValueError which is raised in Python 3.4
            # ---------------------------------------------------------------
            # Leave it up to click to ask the user again.
            # Local function procsse_json() is called by click within a
            # try block that catches click.UsageError exception's and asks
            # the user to try again.
            raise click.UsageError('Unable to decode to JSON.')

    dict_value = click.prompt(
        variable.prompt,
        default=default_json,
        type=click.STRING,
        value_proc=process_json,
    )
    # working around the default process of click
    if dict_value == default_json:
        # Return the given default w/o any processing
        return default
    return dict_value


def prompt_yes_no(variable, default):
    """Prompts the user for a yes or no option."""
    if default is True:
        default_display = 'y'
    else:
        default_display = 'n'

    # click.prompt() behavior:
    # When supplied with a string default, the string default is returned,
    # rather than the string converted to a click.BOOL.
    # If default is passed as a boolean then the default is displayed as
    # [True] or [False], rather than [y] or [n].
    # This prompt translates y, yes, Yes, YES, n, no, No, NO to their correct
    # boolean values, its just that it does not translate a string default
    # value of y, yes, Yes, YES, n, no, No, NO to a boolean...
    value = click.prompt(variable.prompt, default=default_display, type=click.BOOL,)

    # ...so if we get the displayed default value back (its a string),
    # change it to its associated boolean value
    if value == default_display:
        value = default

    return value


def prompt_choice(variable, default):
    """Return prompt, default and callback for a choice variable."""
    choice_map = collections.OrderedDict(
        (u'{}'.format(i), value) for i, value in enumerate(variable.choices, 1)
    )
    choices = choice_map.keys()

    prompt = u'\n'.join(
        (
            variable.prompt,
            u'\n'.join([u'{} - {}'.format(*c) for c in choice_map.items()]),
            u'Choose from {}'.format(u', '.join(choices)),
        )
    )
    default = str(variable.choices.index(default) + 1)

    user_choice = click.prompt(prompt, default=default, type=click.Choice(choices),)
    return choice_map[user_choice]


# each variable type need specific handling in prompting
PROMPTS = {
    'string': prompt_string,
    'boolean': prompt_boolean,
    'int': prompt_int,
    'float': prompt_float,
    'uuid': prompt_uuid,
    'json': prompt_json,
    'yes_no': prompt_yes_no,
}


def _deserialize_string(value) -> str:
    return str(value)


def _deserialize_boolean(value) -> bool:
    return bool(value)


def _deserialize_yes_no(value) -> bool:
    return bool(value)


def _deserialize_int(value) -> int:
    return int(value)


def _deserialize_float(value) -> float:
    return float(value)


def _deserialize_uuid(value) -> str:
    # standard UUID is not JSON Serializable
    return click.UUID(value).hex


def _deserialize_json(value) -> Dict:
    return value


# mapping of functions used to process every possible click input type
DESERIALIZERS = {
    'string': _deserialize_string,
    'boolean': _deserialize_boolean,
    'int': _deserialize_int,
    'float': _deserialize_float,
    'uuid': _deserialize_uuid,
    'json': _deserialize_json,
    'yes_no': _deserialize_yes_no,
}


class Variable(object):
    """Parse the attributes and functionalities of a version 2 variable."""

    def __init__(self, name: str, type: str, **info):
        """
        Mandatory parameters.

        :param name: A string containing the variable's name in the jinja2
                     context.
        :param type: The variable's type. Suported types are listed in the schema

        :param kwargs info: Keyword/Argument pairs recognized are shown below.

        Recognized Keyword/Arguments, but optional:

            - `prompt` -- A string to show user when prompted for input.
            - `prompt_user` -- A boolean, if True prompt user; else no prompt.
            - `default` -- Specify a fall back value if no input is provided
                        (highly recommended).

        Supported Types
            * string
            * boolean
            * int
            * float
            * uuid
            * json
            * yes_no

        """
        # mandatory fields
        self.name = name
        self.var_type = type
        # -- DEFAULT ------------------------------------------------------------
        self.default = info.get('default')

        # -- PROMPT ----------------------------------------------------------
        self.prompt = info.get('prompt', DEFAULT_PROMPT.format(variable=self))

        # -- PROMPT_USER -----------------------------------------------------
        self.prompt_user = info.get('prompt_user')
        # do not prompt for private variable names (beginning with _)
        if self.prompt_user is None:
            self.prompt_user = not self.name.startswith('_')

        # -- CHOICES ---------------------------------------------------------
        self.choices = info.get('choices', [])
        # making sure that the default value is present in the choices
        if self.choices and "default" in info and self.default not in self.choices:
            msg = (
                "Variable: {var_name} has an invalid default "
                "value {default} for choices: {choices}."
            )
            raise InvalidConfiguration(
                msg.format(
                    var_name=self.name, default=self.default, choices=self.choices
                )
            )

    def __repr__(self):
        """Provide a representation with variable name."""
        return "<{class_name} {variable_name}>".format(
            class_name=self.__class__.__name__, variable_name=self.name,
        )

    def __str__(self):
        """Provide a JSON representation of the variable content."""
        s = [
            "{key}='{value}'".format(key=key, value=self.__dict__[key])
            for key in self.__dict__
            if key != 'info'
        ]
        return self.__repr__() + ':\n' + ',\n'.join(s)


class CookiecutterTemplate:
    """Embodies all attributes of a version 2 Cookiecutter template."""

    def __init__(self, template, extensions=None, **kwargs):
        """
        Mandatory Parameters.

        :param template: A dictionary containing the template fields of
               schema 2.0, including:
                - name: the template name
                - variables: a list of context variables
                - additional template info (e.g. Authors, URL, etc.)
        :param requires: A list of env. requirement (python version and CC version)
        :param extensions: a list of jinja2 environment parameters
        :param kwargs: Other template info not used here
        """
        # mandatory fields
        self.name = template["name"]
        self.extensions = extensions

        self.variables = [Variable(**v) for v in template["variables"]]

    def __repr__(self):
        """Provide a classname with template name."""
        return "<{class_name} {template_name}>".format(
            class_name=self.__class__.__name__, template_name=self.name,
        )

    def __iter__(self):
        """Iterate through the templates variables."""
        for v in self.variables:
            yield v


def prompt_variable(variable: Variable, verbose: bool):
    """
    Prompt variable value from user in the terminal.

    :param variable: the variable object to be prompted
    :param verbose: option for more elaborate display
    :return: the value provided by user
    """
    if variable.choices:
        # which prompt depends of the variable type except if its a choice list
        prompt = prompt_choice
    else:
        prompt = PROMPTS[variable.var_type]

    return prompt(variable, variable.default)


def load_context(json_object: Dict, no_input=False, verbose=True) -> Dict:
    """
    Load a v2 cookiecutter.json and prompts/loads the variable inputs.

    :param json_object: A JSON file that has be loaded into a Python OrderedDict.
    :param no_input: Prompt the user at command line for manual configuration if False,
                     if True, no input prompts are made, all defaults are accepted.
    :param verbose: Emit maximum variable information.
    """
    # checking that the context shell is valid
    validate(json_object)

    # setting up jinja for rendering dynamical variables
    env = Environment(extensions=['jinja2_time.TimeExtension'])  # nosec
    context = collections.OrderedDict({})

    def jinja_render(string):
        template = env.from_string(string)
        return template.render(cookiecutter=context)

    for variable in CookiecutterTemplate(**json_object):

        # rendering dynamical default value
        if isinstance(variable.default, str):
            variable.default = jinja_render(variable.default)

        # actually getting the variable value
        if no_input or (not variable.prompt_user):
            value = variable.default
        else:
            value = prompt_variable(variable, verbose)

        deserialize = DESERIALIZERS[variable.var_type]
        context[variable.name] = deserialize(value)

        # for prompt esthetics
        if verbose:
            width, _ = click.get_terminal_size()
            click.echo('-' * width)

    # TODO: here we match the v2 context to the v1 conventions for Jinja env variables
    #  if this PR goes through, next step is to refactor the whole context
    #  structure and the namings
    context_parameters = json_object.get('jinja')
    if context_parameters:
        context['_extensions'] = context_parameters.get('extensions')
        context['_jinja2_env_vars'] = {
            param: context_parameters[param]
            for param in context_parameters.keys()
            if param != 'extensions'
        }

    return context
