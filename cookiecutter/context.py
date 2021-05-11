# -*- coding: utf-8 -*-
# flake8: noqa
"""
cookiecutter.context
--------------------

Process the version 2 cookiecutter context (previsously loaded via
cookiecutter.json) and handle any user input that might be associated with
initializing the settings defined in the 'variables' OrderedDict part of the
context.

This module produces a dictionary used later by the jinja2 template engine to
generate files.

Based on the source code written by @hackebrot see:
https://github.com/audreyr/cookiecutter/pull/848
https://github.com/hackebrot/cookiecutter/tree/new-context-format

"""

import logging
import collections
import json
import re

import click
from jinja2 import Environment

from cookiecutter.schema import validate

logger = logging.getLogger(__name__)

DEFAULT_PROMPT = 'Please enter a value for "{variable.name}"'

VALID_TYPES = [
    'boolean',
    'yes_no',
    'int',
    'float',
    'uuid',
    'json',
    'string',
]

SET_OF_REQUIRED_FIELDS = {
    'requires',
    'template',
    'version',
}

# TODO unify the version checkers (here and the schema one)

REGEX_COMPILE_FLAGS = {
    'ascii': re.ASCII,
    'debug': re.DEBUG,
    'ignorecase': re.IGNORECASE,
    'locale': re.LOCALE,
    'mulitline': re.MULTILINE,
    'dotall': re.DOTALL,
    'verbose': re.VERBOSE,
}


def prompt_string(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.STRING,
    )


def prompt_boolean(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.BOOL,
    )


def prompt_int(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.INT,
    )


def prompt_float(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.FLOAT,
    )


def prompt_uuid(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        hide_input=variable.hide_input,
        type=click.UUID,
    )


def prompt_json(variable, default):
    # The JSON object from cookiecutter.json might be very large
    # We only show 'default'

    DEFAULT_JSON = 'default'

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
        default=DEFAULT_JSON,
        hide_input=variable.hide_input,
        type=click.STRING,
        value_proc=process_json,
    )
    # working around the default process of click
    if dict_value == DEFAULT_JSON:
        # Return the given default w/o any processing
        return default
    return dict_value


def prompt_yes_no(variable, default):
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
    """Returns prompt, default and callback for a choice variable"""
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


PROMPTS = {
    'string': prompt_string,
    'boolean': prompt_boolean,
    'int': prompt_int,
    'float': prompt_float,
    'uuid': prompt_uuid,
    'json': prompt_json,
    'yes_no': prompt_yes_no,
}


def deserialize_string(value):
    return str(value)


def deserialize_boolean(value):
    return bool(value)


def deserialize_yes_no(value):
    return bool(value)


def deserialize_int(value):
    return int(value)


def deserialize_float(value):
    return float(value)


def deserialize_uuid(value):
    # standard UUID is not JSON Serializable
    return click.UUID(value).hex


def deserialize_json(value):
    return value


DESERIALIZERS = {
    'string': deserialize_string,
    'boolean': deserialize_boolean,
    'int': deserialize_int,
    'float': deserialize_float,
    'uuid': deserialize_uuid,
    'json': deserialize_json,
    'yes_no': deserialize_yes_no,
}


class Variable(object):
    """
    Embody attributes of variables while processing the variables field of
    a cookiecutter version 2 context.
    """

    def __init__(self, name, default, **info):
        """
        :param name: A string containing the variable's name in the jinja2
                     context.
        :param default: The variable's default value. Can any type defined
                        below.
        :param kwargs info: Keyword/Argument pairs recognized are shown below.

        Recognized Keyword/Arguments, but optional:

            - `description` -- A string description of the variable.
            - `prompt` -- A string to show user when prompted for input.
            - `prompt_user` -- A boolean, if True prompt user; else no prompt.
            - `hide_input` -- A boolean, if True hide user's input.
            - `type` -- Specifies the variable's data type see below,
                    defaults to string.
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
        self.default = default

        # optional fields
        self.info = info

        # -- DESCRIPTION -----------------------------------------------------
        self.description = info.get('description', None)
        # -- PROMPT ----------------------------------------------------------
        self.prompt = info.get('prompt', DEFAULT_PROMPT.format(variable=self))

        # -- HIDE_INPUT ------------------------------------------------------
        self.hide_input = info.get('hide_input', False)

        # -- TYPE ------------------------------------------------------------
        self.var_type = info.get('type', 'string')

        # -- SKIP_IF ---------------------------------------------------------
        self.skip_if = info.get('skip_if', '')

        # -- DO_IF ---------------------------------------------------------
        self.do_if = info.get('do_if', '')

        # -- IF_YES_SKIP_TO ---------------------------------------------------------
        self.if_yes_skip_to = info.get('if_yes_skip_to', None)

        # -- IF_NO_SKIP_TO ---------------------------------------------------------
        self.if_no_skip_to = info.get('if_no_skip_to', None)

        # -- PROMPT_USER -----------------------------------------------------
        self.prompt_user = info.get('prompt_user', True)
        # do not prompt for private variable names (beginning with _)
        if self.name.startswith('_'):
            self.prompt_user = False

        # -- CHOICES ---------------------------------------------------------
        # choices are somewhat special as they can be of every type
        self.choices = info.get('choices', [])
        if self.choices and default not in self.choices:
            msg = "Variable: {var_name} has an invalid default value {default} for choices: {choices}."
            raise ValueError(
                msg.format(
                    var_name=self.name, default=self.default, choices=self.choices
                )
            )

        # -- VALIDATION STARTS -----------------------------------------------
        self.validation = info.get('validation', None)

        self.validation_msg = info.get('validation_msg', None)

        self.validation_flag_names = info.get('validation_flags', [])
        self.validation_flags = 0

        for vflag in self.validation_flag_names:
            self.validation_flags |= REGEX_COMPILE_FLAGS[vflag]

        self.validate = None
        if self.validation:
            try:
                self.validate = re.compile(self.validation, self.validation_flags)
            except re.error as e:
                msg = "Variable: {var_name} - Validation Setup Error: Invalid RegEx '{value}' - does not compile - {err}"
                raise ValueError(
                    msg.format(var_name=self.name, value=self.validation, err=e)
                )
        # -- VALIDATION ENDS -------------------------------------------------

    def __repr__(self):
        return "<{class_name} {variable_name}>".format(
            class_name=self.__class__.__name__, variable_name=self.name,
        )

    def __str__(self):
        s = [
            "{key}='{value}'".format(key=key, value=self.__dict__[key])
            for key in self.__dict__
            if key != 'info'
        ]
        return self.__repr__() + ':\n' + ',\n'.join(s)


class CookiecutterTemplate(object):
    """
    Embodies all attributes of a version 2 Cookiecutter template.
    """

    def __init__(self, requires, template, **options):
        """
        Mandatorty Parameters

        :param name: A string, the cookiecutter template name
        :param cookiecutter_version: A string containing the version of the
            cookiecutter application that is compatible with this template.
        :param variables: A list of OrderedDict items that describe each
            variable in the template. These variables are essentially what
            is found in the version 1 cookiecutter.json file.

        Optional Parameters (via \**info)

        :param authors: An array of string - maintainers of the template.
        :param description: A string, human readable description of template.
        :param keywords: An array of string - similar to PyPI keywords.
        :param license: A string identifying the license of the template code.
        :param url: A string containing the URL for the template project.
        :param version: A string containing a version identifier, ideally
            following the semantic versioning spec.

        """

        # mandatory fields
        self.name = template["name"]
        self.cookiecutter_version = requires["cookiecutter"]
        self.variables = [Variable(**v) for v in template["variables"]]

        # optional fields
        self.authors = template.get('authors', [])
        self.description = template.get('description', None)
        self.keywords = template.get('keywords', [])
        self.license = template.get('license', None)
        self.url = template.get('url', None)
        self.version = template.get('version', None)

    def __repr__(self):
        return "<{class_name} {template_name}>".format(
            class_name=self.__class__.__name__, template_name=self.name,
        )

    def __iter__(self):
        for v in self.variables:
            yield v


def load_context(json_object, no_input=False, verbose=True):
    """
    Load a version 2 context & process the json_object for declared variables
    in the Cookiecutter template.

    :param json_object: A JSON file that has be loaded into a Python OrderedDict.
    :param no_input: Prompt the user at command line for manual configuration if False,
                     if True, no input prompts are made, all defaults are accepted.
    :param verbose: Emit maximum variable information.
    """
    env = Environment(extensions=['jinja2_time.TimeExtension'])
    context = collections.OrderedDict({})

    skip_to_variable_name = None

    validate(json_object)

    for variable in CookiecutterTemplate(**json_object):
        if skip_to_variable_name:
            if variable.name == skip_to_variable_name:
                skip_to_variable_name = None
            else:
                # Is executed, but not marked so in coverage report, due to
                # CPython's peephole optimizer's optimizations.
                # See https://bitbucket.org/ned/coveragepy/issues/198/continue-marked-as-not-covered
                # Issue #198 in coverage.py marked WONTFIX
                continue  # pragma: no cover

        if variable.skip_if:
            skip_template = env.from_string(variable.skip_if)
            if skip_template.render(cookiecutter=context) == 'True':
                continue

        if variable.do_if:
            do_template = env.from_string(variable.do_if)
            if do_template.render(cookiecutter=context) == 'False':
                continue

        default = variable.default

        if isinstance(default, str):
            template = env.from_string(default)
            default = template.render(cookiecutter=context)

        deserialize = DESERIALIZERS[variable.var_type]

        if no_input or (not variable.prompt_user):
            context[variable.name] = deserialize(default)
        else:
            if variable.choices:
                prompt = prompt_choice
            else:
                prompt = PROMPTS[variable.var_type]

            if verbose and variable.description:
                click.echo(variable.description)

            while True:
                value = prompt(variable, default)
                if variable.validate:
                    if variable.validate.match(value):
                        break
                    else:
                        msg = "Input validation failure against regex: '{val_string}', try again!".format(
                            val_string=variable.validation
                        )
                        click.echo(msg)
                        if variable.validation_msg:
                            click.echo(variable.validation_msg)
                else:
                    # no validation defined
                    break  # pragma: no cover
            if verbose:
                width, _ = click.get_terminal_size()
                click.echo('-' * width)

            context[variable.name] = deserialize(value)

        if variable.if_yes_skip_to and context[variable.name] is True:
            skip_to_variable_name = variable.if_yes_skip_to

        if variable.if_no_skip_to and context[variable.name] is False:
            skip_to_variable_name = variable.if_no_skip_to

    if skip_to_variable_name:
        logger.warning(
            "Processed all variables, but skip_to_variable_name '{}' was never found.".format(
                skip_to_variable_name
            )
        )

    if 'extensions' in json_object:
        context['extensions'] = json_object.get('extensions')

    return context
