import jsonschema


schema_2_0 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "cookiecutter-schema-2.0",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "version": {"type": "string"},
        "description": {"type": "string"},
        "authors": {"type": "array", "items": {"type": "string"}},
        "cookiecutter_version": {"type": "string"},
        "python_requires": {"type": "string"},
        "license": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "url": {"type": "string"},
        "variables": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "default": {},
                    "prompt": {"type": "string"},
                    "description": {"type": "string"},
                    "type": {"type": "string"},
                    "validation": {"type": "string"},
                    "choices": {"type": "array", "items": {"type": "string"}},
                    "prompt_user": {"type": "boolean"},
                    "hide_input": {"type": "boolean"},
                    "do_if": {"type": "string"},
                    "skip_if": {"type": "string"},
                    "if_no_skip_to": {"type": "string"},
                    "if_yes_skip_to": {"type": "string"},
                    "validation_msg": {"type": "string"},
                },
                "required": ["name", "type"],
            },
        },
    },
    "required": ["name", "version", "cookiecutter_version", "variables"],
}


def validate(d):
    jsonschema.validate(instance=d, schema=schema_2_0)
