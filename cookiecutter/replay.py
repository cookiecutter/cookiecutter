"""
cookiecutter.replay.

-------------------
"""
import json
import os

from cookiecutter.utils import make_sure_path_exists

import ruyaml

yaml = ruyaml.YAML(typ='safe')
# import yaml
# To swap, all we need to do is swap these lines above.


def get_file_name(replay_dir, template_name):
    """Get the name of file."""
    suffix = '.json' if not template_name.endswith('.json') else ''
    file_name = '{}{}'.format(template_name, suffix)
    return os.path.join(replay_dir, file_name)


def dump(replay_dir, template_name, context):
    """Write json data to file."""
    if not make_sure_path_exists(replay_dir):
        raise IOError('Unable to create replay dir at {}'.format(replay_dir))

    if not isinstance(template_name, str):
        raise TypeError('Template name is required to be of type str')

    if not isinstance(context, dict):
        raise TypeError('Context is required to be of type dict')

    if 'cookiecutter' not in context:
        raise ValueError('Context is required to contain a cookiecutter key')

    replay_file = get_file_name(replay_dir, template_name)

    with open(replay_file, 'w') as outfile:
        json.dump(context, outfile, indent=2)


def load_replay_file(replay_file):
    """Read cookiecutter's parameter values from replay file."""
    with open(replay_file, 'r') as infile:
        # Since a YAML parser will also parse JSON,
        # we could simply use the YAML parser always.
        if os.path.splitext(replay_file)[1] in ('.yml', '.yaml'):
            context = yaml.load(infile)
        else:
            context = json.load(infile)

    if 'cookiecutter' not in context:
        raise ValueError('Context is required to contain a cookiecutter key')

    return context


def load(replay_dir, template_name):
    """Read json data from file."""
    if not isinstance(template_name, str):
        raise TypeError('Template name is required to be of type str')

    replay_file = get_file_name(replay_dir, template_name)
    return load_replay_file(replay_file)
