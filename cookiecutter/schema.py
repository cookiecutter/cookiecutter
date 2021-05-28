"""JSON Schema definition for cookiecutter.json"""
from typing import Optional
from warnings import warn

import jsonschema

schema_1_0 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "cookiecutter-schema-1.0",
    "type": "object",
    # schema 1.0 is simply everything
    "properties": {},
}

schema_2_0 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "cookiecutter-schema-2.0",
    "type": "object",
    "properties": {
        # cookiecutter schema version
        "version": {"type": "string", "enum": ["2.0", "2"]},
        # list requirements for this template
        "requires": {
            "type": "object",
            "properties": {
                # min version of cookiecutter that is required by the template
                "cookiecutter": {"type": "string"},
                # python version constraints of the template
                "python": {"type": "string"},
            },
            "additionalProperties": False,
        },
        # additional parameters for Jinja2 environment
        # frequent use for the 'extension' parameter
        # see all parameter options at
        # https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment
        "jinja": {
            "type": "object",
            "additionalProperties": {
                "type": ["string", "boolean", "integer", "array"],
                "items": {"type": "string"},
            },
        },
        # the template definition
        "template": {
            "type": "object",
            "properties": {
                # name of the template
                "name": {"type": "string"},
                # version number of the cookiecutter template
                "version": {"type": "string"},
                # description of the template
                "description": {"type": "string"},
                # list of authors (may include email addresses or other contact information)
                "authors": {"type": "array", "items": {"type": "string"}},
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
                            # regex flags used with the validation string
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
                            # skip to this variable, if "no" was selected in a "yes_no" prompt
                            "if_no_skip_to": {"type": "string"},
                            # skip to this variable, if "yes" was selected in a "yes_no" prompt
                            "if_yes_skip_to": {"type": "string"},
                        },
                        "required": ["name", "type"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["name", "variables"],
            "additionalProperties": False,
        },
    },
    "required": ["version", "template"],
    "additionalProperties": False,
}

# mapping from valid schema version names to their json schema instances
schema_versions = {
    '1.0': schema_1_0,
    '2.0': schema_2_0,
}

# cookiecutter schema versions in chronological order
schema_chronology = ['1.0', '2.0']


def validate(d: dict, version=None) -> None:
    """
    Validate a cookiecutter.json (as Python dict) against the specified cookiecutter schema
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
    else:
        version = infer_schema_version(d)
        _validate(d, version)


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


def infer_schema_version(d: dict) -> Optional[str]:
    """
    Detect the schema version of the specified cookiecutter.json (as Python dict).
    The schema will not be validated, this function will only try to return the
    schema version. If the schema version could not be detected, None is returned.

    :param d: the cookiecutter.json as Python dict
    :return: the schema version, defaults to v1.0 with a warning
    """
    # here we make the minimal assumptions for the versions.
    # If a file contains a version=2.0 term but contains a 1.0
    # schema structure, it will be considered as a broken 2.0 file
    if "version" in d and d["version"] in schema_versions:
        return d["version"]

    if "version" in d:
        warn(
            " Schema version & detected."
            " \"version\" field is reserved in Cookiecutter 2 for indicating "
            "the Schema version. Please use another variable name for safe usage",
            UserWarning,
        )

    return '1.0'
