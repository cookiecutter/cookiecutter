# -*- coding: utf-8 -*-

import codecs
import collections
import json
import pprint

import click
from jinja2 import Environment

DEFAULT_PROMPT = 'Please enter a value for "{variable.name}"'

VALID_TYPES = [
    'boolean',
    'yes_no',
    'int',
    'json',
    'string',
]


def prompt_string(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        type=click.STRING,
    )


def prompt_boolean(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        type=click.BOOL,
    )


def prompt_int(variable, default):
    return click.prompt(
        variable.prompt,
        default=default,
        type=click.INT,
    )


def prompt_json(variable, default):
    # The JSON object from cookiecutter.json might be very large
    # We only show 'default'
    DEFAULT_JSON = 'default'

    def process_json(user_value):
        if user_value == DEFAULT_JSON:
            # Return the given default w/o any processing
            return default

        try:
            hook = collections.OrderedDict
            return json.loads(user_value, object_pairs_hook=hook)
        except json.decoder.JSONDecodeError:
            # Leave it up to click to ask the user again
            raise click.UsageError('Unable to decode to JSON.')

    return click.prompt(
        variable.prompt,
        default=DEFAULT_JSON,
        type=click.STRING,
        value_proc=process_json,
    )


def prompt_yes_no(variable, default):
    if default is True:
        default_display = 'y'
    else:
        default_display = 'n'

    return click.prompt(
        variable.prompt,
        default=default_display,
        type=click.BOOL,
    )


def prompt_choice(variable, default):
    """Returns prompt, default and callback for a choice variable"""
    choice_map = collections.OrderedDict(
        (u'{}'.format(i), value)
        for i, value in enumerate(variable.choices, 1)
    )
    choices = choice_map.keys()

    prompt = u'\n'.join((
        variable.prompt,
        u'\n'.join([u'{} - {}'.format(*c) for c in choice_map.items()]),
        u'Choose from {}'.format(u', '.join(choices)),
    ))
    default = str(variable.choices.index(default) + 1)

    user_choice = click.prompt(
        prompt,
        type=click.Choice(choices),
        default=default,
    )
    return choice_map[user_choice]

PROMPTS = {
    'string': prompt_string,
    'boolean': prompt_boolean,
    'int': prompt_int,
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


def deserialize_json(value):
    return value


DESERIALIZERS = {
    'string': deserialize_string,
    'boolean': deserialize_boolean,
    'int': deserialize_int,
    'json': deserialize_json,
    'yes_no': deserialize_yes_no,
}


class Variable(object):
    def __init__(self, name, default, **info):

        # mandatory fields
        self.name = name
        self.default = default

        # optional fields
        self.description = info.get('description', None)
        self.prompt = info.get('prompt', DEFAULT_PROMPT.format(variable=self))

        self.var_type = info.get('type', 'string')
        if self.var_type not in VALID_TYPES:
            msg = 'Invalid type {var_type} for variable'
            raise ValueError(msg.format(var_type=self.var_type))

        self.skip_if = info.get('skip_if', '')
        if not isinstance(self.skip_if, str):
            # skip_if was specified in cookiecutter.json
            msg = 'Field skip_if is required to be a str, got {value}'
            raise ValueError(msg.format(value=self.skip_if))

        self.prompt_user = info.get('prompt_user', True)
        if not isinstance(self.prompt_user, bool):
            # prompt_user was specified in cookiecutter.json
            msg = 'Field prompt_user is required to be a bool, got {value}'
            raise ValueError(msg.format(value=self.prompt_user))

        # choices are somewhat special as they can of every type
        self.choices = info.get('choices', [])
        if self.choices and default not in self.choices:
            msg = 'Invalid default value {default} for choice variable'
            raise ValueError(msg.format(default=self.default))

    def __repr__(self):
        return "<{class_name} {variable_name}>".format(
            class_name=self.__class__.__name__,
            variable_name=self.name,
        )


class CookiecutterTemplate(object):
    def __init__(self, name, description, variables, **info):
        # mandatory fields
        self.name = name
        self.description = description
        self.variables = [Variable(**v) for v in variables]

        # optional fields
        self.authors = info.get('authors', [])
        self.cookiecutter_version = info.get('cookiecutter_version', None)
        self.keywords = info.get('keywords', [])
        self.license = info.get('license', None)
        self.version = info.get('version', None)
        self.url = info.get('url', None)

    def __repr__(self):
        return "<{class_name} {template_name}>".format(
            class_name=self.__class__.__name__,
            template_name=self.name,
        )

    def __iter__(self):
        for v in self.variables:
            yield v


def load_context(json_object, verbose):
    env = Environment(extensions=['jinja2_time.TimeExtension'])
    context = collections.OrderedDict({})

    for variable in CookiecutterTemplate(**json_object):
        if variable.skip_if:
            skip_template = env.from_string(variable.skip_if)
            if skip_template.render(cookiecutter=context) == 'True':
                continue

        default = variable.default

        if isinstance(default, str):
            template = env.from_string(default)
            default = template.render(cookiecutter=context)

        deserialize = DESERIALIZERS[variable.var_type]

        if not variable.prompt_user:
            context[variable.name] = deserialize(default)
            continue

        if variable.choices:
            prompt = prompt_choice
        else:
            prompt = PROMPTS[variable.var_type]

        if verbose and variable.description:
            click.echo(variable.description)

        value = prompt(variable, default)

        if verbose:
            width, _ = click.get_terminal_size()
            click.echo('-' * width)

        context[variable.name] = deserialize(value)

    return context


def main(file_path):
    """Load the json object and prompt the user for input"""

    with codecs.open(file_path, 'r', encoding='utf8') as f:
        json_object = json.load(f, object_pairs_hook=collections.OrderedDict)

    pprint.pprint(load_context(json_object, True))

if __name__ == '__main__':
    main('tests/new-context/cookiecutter.json')
