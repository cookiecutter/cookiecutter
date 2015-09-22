from collections import OrderedDict

import click

from .compat import text_type
from .exceptions import InvalidConfiguration, ValidationException
from .prompt import render_variable


class OptionRegistry(dict):
    def register(self, cls):
        self[cls.type_name] = cls
        return cls


option_types = OptionRegistry()


def option_from_context(key, value):
    if isinstance(value, dict):
        option_type_name = value.pop('type', 'string')
        try:
            OptionType = option_types[option_type_name]
        except KeyError:
            raise InvalidConfiguration('{0}: Unknown option type {1!r}'.format(
                key, option_type_name))
        return OptionType(key=key, **value)

    elif isinstance(value, list):
        return ChoicesOption(key=key, prompt=key, choices=value)

    elif isinstance(value, text_type):
        return Option(key=key, prompt=key, default=value)

    else:
        raise InvalidConfiguration('{0}: Invalid option value'.format(key))


class Option(object):

    def __init__(self, key, prompt=None, default=None):
        self.key = key
        self.prompt = prompt or key
        self.default = default

    def clean(self, value):
        return value

    def prompt_for_value(self, cookiecutter_dict, env, no_input):
        while True:
            out = self.show_prompt(cookiecutter_dict, env, no_input)
            try:
                return self.clean(out)
            except ValidationException as e:
                click.echo(e)
                pass

    def show_prompt(self, cookiecutter_dict, env, no_input):
        default = render_variable(env, self.default, cookiecutter_dict)
        if no_input:
            return default
        else:
            return click.prompt(self.prompt, default=default)

    def __str__(self):
        raise RuntimeError("Nope, shouldnt call this")


@option_types.register
class StringOption(Option):
    type_name = 'string'


@option_types.register
class ChoicesOption(Option):
    type_name = 'choice'

    def __init__(self, key, prompt=None, choices=[], **kwargs):
        if prompt is None:
            prompt = 'Select {}'.format(key)

        super(ChoicesOption, self).__init__(key, prompt, **kwargs)

        self.choice_map = OrderedDict(
            (text_type(i), value) for i, value in enumerate(choices, 1)
        )
        if not self.choice_map:
            raise InvalidConfiguration("{0}: Choices can not be empty".format(
                self.key))

        if self.default is None:
            self.default = '1'

    def clean(self, value):
        return self.choice_map[super(ChoicesOption, self).clean(value)]

    def show_prompt(self, cookiecutter_dict, env, no_input):
        # Please see http://click.pocoo.org/4/api/#click.prompt
        choices = self.choice_map.keys()
        default = self.default

        choice_lines = ['{} - {}'.format(*c) for c in self.choice_map.items()]
        prompt = '\n'.join((
            '{}:'.format(self.prompt),
            '\n'.join(choice_lines),
            'Choose from {}'.format(', '.join(choices))
        ))

        return click.prompt(
            prompt, type=click.Choice(choices), default=default
        )
