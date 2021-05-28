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
import platform
import re
from operator import eq, ge, gt, le, lt, ne
from typing import Any, Callable, Dict, Tuple

import click
from jinja2 import Environment
from packaging import version

from cookiecutter import __version__
from cookiecutter.exceptions import IncompatibleVersion, InvalidConfiguration
from cookiecutter.schema import validate

logger = logging.getLogger(__name__)

DEFAULT_PROMPT = 'Please enter a value for "{variable.name}"'


REGEX_COMPILE_FLAGS = {
    'ascii': re.ASCII,
    'debug': re.DEBUG,
    'ignorecase': re.IGNORECASE,
    'locale': re.LOCALE,
    'mulitline': re.MULTILINE,
    'dotall': re.DOTALL,
    'verbose': re.VERBOSE,
}

op_mapping = {'==': eq, '<=': le, '<': lt, '>=': ge, '>': gt, '!=': ne}


def _split_version_op(
    version_op: str, default='=='
) -> Tuple[str, str, Callable[[Any, Any], bool]]:
    """
    Parse the version requirement string.

    Split a version string that may contain an operator and return just the version,
    the operator and the Python function that implements this operator.
    If no operator was detected, use the default operator instead.
    Supported operators are ==, <=, <, >=, >, !=.

    Example: ">= 1.5.0" becomes ("1.5.0", ">=", <built-in function ge>)

    :param version_op: a version string with an optional operator at the start
    :param default: the default operator to return, if no operator was found
    :return: a tuple of (version string, operator string, operator function)
    """
    version_op = version_op.strip()
    for code, op in op_mapping.items():
        if version_op.startswith(code):
            version_str = version_op[len(code) :].strip()  # noqa
            return version_str, code, op
    return version_op, default, op_mapping[default]


def validate_requirement(requires: str, actual: str, message=None):
    """
    Check if a version number fits a version requirement.

    Mostly adheres to PEP 440 with a few limitations:

    * no wildcard version matching, e.g. "!= 3.1.*"
    * no compatible release matching, e.g. "~= 1.4.5"

    :param requires: string with list of version requirements (e.g ">=3, <4")
    :param actual: the actual version to compare to
    :param message: error message to use when the version check fails
    :raises IncompatibleVersion: if a version check fails
    """
    # parse version numbers
    requires_ops = [_split_version_op(s) for s in requires.split(',')]
    version_actual = version.parse(actual)
    # check each version
    for version_str, op_str, op_fun in requires_ops:
        version_requires = version.parse(version_str)
        if not op_fun(version_actual, version_requires):
            error_text = f"{actual} {op_str} {version_str}"
            if message:
                error_text = f"{message}: {error_text}"
            raise IncompatibleVersion(error_text)


def prompt_string(variable, default):
    """Prompts the user for a text value."""
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.STRING,
    )


def prompt_boolean(variable, default):
    """Prompts the user for a boolean."""
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.BOOL,
    )


def prompt_int(variable, default):
    """Prompts the user for an int."""
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.INT,
    )


def prompt_float(variable, default):
    """Prompts the user for float."""
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.FLOAT,
    )


def prompt_uuid(variable, default):
    """Prompts the user for a uuid."""
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.UUID,
    )


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
        hide_input=variable.hide_input,
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
    value = click.prompt(
        variable.prompt,
        default=default_display,
        hide_input=variable.hide_input,
        type=click.BOOL,
    )

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

    user_choice = click.prompt(
        prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.Choice(choices),
    )
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

            - `description` -- A string description of the variable.
            - `prompt` -- A string to show user when prompted for input.
            - `prompt_user` -- A boolean, if True prompt user; else no prompt.
            - `hide_input` -- A boolean, if True hide user's input.
            - `default` -- Specify a fall back value if no input is provided
                        (highly recommended).
            - `skip_if` -- A string of a jinja2 renderable boolean expression,
                    the variable will be skipped if it renders True.
            - `do_if` -- A string of a jinja2 renderable boolean expression,
                    the variable will be processed if it renders True.
            - `choices` -- A list of choices, may be of mixed types.
            - `if_yes_skip_to` -- A string containing a variable name to skip
                    to if the yes_no value is True (yes). Only has meaning for
                    variables of type 'yes_no'.
            - `if_no_skip_to` -- A string containing a variable name to skip
                    to if the yes_no value is False (no). Only has meaning for
                    variables of type 'yes_no'.
            - `validation` -- A string defining a regex to use to validation
                    user input. Defaults to None.
            - `validation_msg` -- A string defining an additional message to
                    display if the validation check fails.
            - `validation_flags` -- A list of validation flag names that can be
                    specified to control the behaviour of the validation
                    check done using the above defined `validation` string.
                    Specifying a flag is equivalent to setting it to True,
                    not specifying a flag is equivalent to setting it to False.
                    The default value of this variable has no effect on the
                    validation check.

                    The flags supported are:

                        * ascii - enabling re.ASCII
                        * debug - enabling re.DEBUG
                        * ignorecase - enabling re.IGNORECASE
                        * locale - enabling re.LOCALE
                        * mulitline - enabling re.MULTILINE
                        * dotall - enabling re.DOTALL
                        * verbose - enabling re.VERBOSE

                    See: https://docs.python.org/3/library/re.html#re.compile

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

        # optional fields
        self.info = info

        # -- DESCRIPTION -----------------------------------------------------
        self.description = info.get('description')
        # -- PROMPT ----------------------------------------------------------
        self.prompt = info.get('prompt', DEFAULT_PROMPT.format(variable=self))

        # -- HIDE_INPUT ------------------------------------------------------
        self.hide_input = info.get('hide_input', False)

        # -- DEFAULT ------------------------------------------------------------
        self.default = info.get('default')

        # -- SKIP_IF ---------------------------------------------------------
        self.skip_if = info.get('skip_if')

        # -- DO_IF ---------------------------------------------------------
        self.do_if = info.get('do_if')

        # -- IF_YES_SKIP_TO ---------------------------------------------------------
        self.if_yes_skip_to = info.get('if_yes_skip_to')

        # -- IF_NO_SKIP_TO ---------------------------------------------------------
        self.if_no_skip_to = info.get('if_no_skip_to')

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

        # -- VALIDATION STARTS -----------------------------------------------
        self.validation = info.get('validation')
        self.validate = None
        if self.validation:

            self.validation_msg = info.get('validation_msg')
            self.validation_flag_names = info.get('validation_flags', [])

            self.validation_flags = 0
            for vflag in self.validation_flag_names:
                self.validation_flags |= REGEX_COMPILE_FLAGS[vflag]
            try:
                self.validate = re.compile(self.validation, self.validation_flags)
            except re.error as e:
                raise InvalidConfiguration(
                    f"Variable: {self.name} - Validation Setup Error:"
                    f" Invalid RegEx '{self.validation}' - does not compile - {e}"
                )

            # -- making a few sanity checks
            # checking fo key as default value could be 'False' or ''
            if self.var_type != "string":
                raise InvalidConfiguration(
                    "attempting regex validation on non-string input"
                )

        # -- VALIDATION ENDS -------------------------------------------------

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

    def __init__(self, template, requires=None, extensions=None, **kwargs):
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
        self.requirements = requires
        self.extensions = extensions

        if self.requirements:
            self.cookiecutter_version = self.requirements.get('cookiecutter')
            if self.cookiecutter_version:
                validate_requirement(
                    self.cookiecutter_version,
                    __version__,
                    "cookiecutter version check failed",
                )
            self.python_version = self.requirements.get('python')
            if self.python_version:
                validate_requirement(
                    self.python_version,
                    platform.python_version(),
                    "Python version check failed",
                )

        self.variables = [Variable(**v) for v in template["variables"]]

        # optional fields
        self.authors = template.get('authors', [])
        self.description = template.get('description')
        self.keywords = template.get('keywords', [])
        self.license = template.get('license')
        self.url = template.get('url')
        self.version = template.get('version', None)

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

    if verbose and variable.description:
        click.echo(variable.description)

    while True:
        value = prompt(variable, variable.default)
        # if a regex pattern has been used for validation, we repeat the prompting
        # until regex validation patter has been matched
        if variable.validate:
            if variable.validate.match(value):
                return value
            else:
                msg = (
                    f"Input validation failure against regex:"
                    f" '{variable.validation}', try again!"
                )

                click.echo(msg)
                if variable.validation_msg:
                    click.echo(variable.validation_msg)
        else:
            return value


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

    skip_to_variable_name = None
    for variable in CookiecutterTemplate(**json_object):

        # checking all scenarios for which this variable should be skipped
        if skip_to_variable_name and variable.name != skip_to_variable_name:
            continue
        skip_to_variable_name = None

        if variable.skip_if and jinja_render(variable.skip_if) == 'True':
            continue

        if variable.do_if and jinja_render(variable.do_if) == 'False':
            continue

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

        # updating the skipping variables for the continuation
        if variable.if_yes_skip_to and context[variable.name] is True:
            skip_to_variable_name = variable.if_yes_skip_to

        if variable.if_no_skip_to and context[variable.name] is False:
            skip_to_variable_name = variable.if_no_skip_to

    if skip_to_variable_name:
        logger.warning(
            f"Processed all variables, but skip_to_variable_name "
            f"'{skip_to_variable_name}' was never found."
        )

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
