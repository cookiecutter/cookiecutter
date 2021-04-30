from typing import Optional

import jsonschema
from jsonschema import ValidationError

schema_1_0 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "cookiecutter-schema-1.0",
    "type": "object",
    # schema 1.0 is trivial: mapping from any variable name to a string or list of strings
    "patternProperties": {
        "^.+$": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        }
    },
    "additionalProperties": False,
}

schema_2_0 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "cookiecutter-schema-2.0",
    "type": "object",
    "properties": {
        # cookiecutter schema version
        "version": {"type": "string", "enum": ["2.0", "2"]},
        # name of the template
        "name": {"type": "string"},
        # description of the template
        "description": {"type": "string"},
        # list of authors (may include email addresses or other contact information)
        "authors": {"type": "array", "items": {"type": "string"}},
        # version number of the cookiecutter template
        "template_version": {"type": "string"},
        # min version of cookiecutter that is required by the template
        "cookiecutter_version": {"type": "string"},
        # python version constraints of the template
        "python_requires": {"type": "string"},
        # license of the template
        "license": {"type": "string"},
        # keywords that describe the goals of the template
        "keywords": {"type": "array", "items": {"type": "string"}},
        # the canonical url from where the template can be retrieved
        "url": {"type": "string"},
        # definition of the template's variables
        "variables": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    # variable name (must be a valid python variable name)
                    "name": {"type": "string"},
                    # the default value for that variable
                    "default": {},
                    # text that will be displayed before the input field (keep it short!)
                    "prompt": {"type": "string"},
                    # more detailed description of this variable
                    "description": {"type": "string"},
                    # input data type (string, boolean, etc.)
                    "type": {
                        "type": "string",
                        "enum": [
                            "boolean",
                            "yes_no",
                            "int",
                            "float",
                            "uuid",
                            "json",
                            "string",
                        ],
                    },
                    # validate user input with this regex
                    "validation": {"type": "string"},
                    # display this message if validation failed
                    "validation_msg": {"type": "string"},
                    # a list of items to choose from
                    "choices": {"type": "array", "items": {"type": "string"}},
                    # don't prompt the user for this variable, if this is set to false
                    "prompt_user": {"type": "boolean"},
                    # hide user input while typing (e.g. if you're asking for a password)
                    "hide_input": {"type": "boolean"},
                    # only show this prompt, if the specified condition is true
                    "do_if": {"type": "string"},
                    # skip this prompt, if the specified condition is true
                    "skip_if": {"type": "string"},
                    # skip to this variable name, if the user selected "no" in a "yes_no" prompt
                    "if_no_skip_to": {"type": "string"},
                    # skip to this variable name, if the user selected "yes" in a "yes_no" prompt
                    "if_yes_skip_to": {"type": "string"},
                    "validation_flags": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "ascii",
                                "debug",
                                "ignorecase",
                                "locale",
                                "mulitline",
                                "dotall",
                                "verbose",
                            ],
                        },
                    },
                },
                "required": ["name", "type"],
            },
        },
    },
    "required": ["name", "version", "variables"],
}

# mapping from valid schema version names to their json schema instances
schema_versions = {
    '1.0': schema_1_0,
    '1': schema_1_0,
    '2.0': schema_2_0,
    '2': schema_2_0,
    'latest': schema_2_0,
}

# cookiecutter schema versions in chronological order
schema_chronology = ['1.0', '2.0']


def validate(d: dict, version=None) -> None:
    """
    Validate the a cookiecutter.json (as Python dict) against the specified cookiecutter schema
    version. If the version is undefined, the version that is declared in the cookiecutter.json
    is used. If no version declaration is found, schema version 1.0 is assumed.
    Raises a ValidationError if schema validation failed. Raises a ValueError, if the specified
    schema version is not supported.

    :param d: the cookiecutter.json as Python dict
    :param version: the schema version to validate against (optional)
    :return: None, if validation was successful, otherwise errors are raised
    :raises ValueError: if the schema version is not supported
    :raises ValidationError: if schema validation was not successful
    """
    if version:
        # a version number has been explicitly defined
        _validate(d, version)
    elif "version" in d:
        # at this point we can't be sure if this is a legacy cookiecutter which happens to contain
        # a "version" variable or a new cookiecutter with a version field
        try:
            # check the legacy path first
            _validate(d, '1.0')
        except ValidationError:
            # not a legacy cookiecutter - use the declared version number
            _validate(d, d['version'])
    else:
        # assuming schema 1.0.0, since no version has been defined explicitly or implicitly
        _validate(d, '1.0')


def _validate(d: dict, version: str):
    """
    Validate the specified cookiecutter.json (as Python dict) against the specified
    cookiecutter schema version. If the version number is undefined or not supported,
    a ValueError is raised.

    :param d: the cookiecutter.json as Python dict
    :param version: use this schema version to validate the cookiecutter.json
    :return: None, if validation was successful, otherwise errors are raised
    :raises ValueError: if the schema version is undefined or not supported
    :raises ValidationError: if schema validation was not successful
    """
    if version not in schema_versions:
        raise ValueError(f"Unsupported schema version {version}")
    jsonschema.validate(instance=d, schema=schema_versions[version])


def detect(d: dict) -> Optional[str]:
    """
    Detect the schema version of the specified cookiecutter.json (as Python dict).
    The schema will not be validated, this function will only try to return the schema version.
    If the schema version could not be detected, None is returned.

    :param d: the cookiecutter.json as Python dict
    :return: the schema version or None, if no version was detected
    """
    # try to validate against the declared version
    if "version" in d:
        try:
            _validate(d, d["version"])
            return d["version"]
        except (ValueError, ValidationError):
            pass
    # no version was declared or the declaration was invalid, fallback to schema 1.0
    try:
        _validate(d, '1.0')
        return '1.0'
    except ValidationError:
        # nope, this does not appear to be a valid cookiecutter.json
        return None
