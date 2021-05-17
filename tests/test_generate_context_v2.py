# -*- coding: utf-8 -*-
# flake8: noqa
"""
test_generate_convext_v2
------------------------

Tests associated with processing v2 context syntax in the
`cookiecutter.generate` module.
"""

from __future__ import unicode_literals

from collections import OrderedDict
from copy import deepcopy

import pytest

from cookiecutter import generate

# writing explicitely the expected outcomes of different tests
expected_file1_v0 = OrderedDict(
    [
        ("version", "2.0"),
        ("requires", OrderedDict([("cookiecutter", ">1")])),
        (
            "template",
            OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "full_name"),
                                    ("default", "J. Paul Getty"),
                                    ("prompt", "What's your full name?"),
                                    (
                                        "description",
                                        "Please enter your full name. It will be displayed on "
                                        "the README file and used for the PyPI package definition.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "email"),
                                    ("default", "jpg@rich.de"),
                                    ("prompt", "What's your email?"),
                                    (
                                        "description",
                                        "Please enter an email address for "
                                        "the meta information in setup.py.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
        ),
    ]
)

expected_file1_v1 = deepcopy(expected_file1_v0)
expected_file1_v1['template']['variables'][0]['default'] = 'James Patrick Morgan'

expected_file1_v2 = deepcopy(expected_file1_v0)
expected_file1_v2['template']['variables'][1]['default'] = 'jpm@chase.bk'

expected_file1_v3 = deepcopy(expected_file1_v0)
expected_file1_v3['template']['variables'][0]['default'] = 'Alpha Gamma Five'
expected_file1_v3['template']['variables'][1]['default'] = 'agamma5@universe.open'

expected_file1_v4 = deepcopy(expected_file1_v0)
expected_file1_v4['template']['variables'][1]['name'] = 'email'
expected_file1_v4['template']['variables'][1]['default'] = 'miles.davis@jazz.gone'
expected_file1_v4['template']['variables'][1]['description'] = 'Enter jazzy email...'

expected_file2_v0 = OrderedDict(
    [
        ("version", "2.0"),
        (
            "template",
            OrderedDict(
                [
                    ("name", "cc-representative"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, "
                                        "we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.director_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
        ),
    ]
)

expected_file2_v1 = deepcopy(expected_file2_v0)
expected_file2_v1['template']['variables'][0]['name'] = 'producer_credit'
expected_file2_v1['template']['variables'][0][
    'prompt'
] = 'Is there a producer credit on this film?'
expected_file2_v1['template']['variables'][0][
    'description'
] = 'There are usually a lot of producers...'
del expected_file2_v1['template']['variables'][1]['skip_if']

expected_file2_v2 = deepcopy(expected_file2_v0)
expected_file2_v2['template']['variables'][0]['name'] = 'producer_credits'
expected_file2_v2['template']['variables'][0]['default'] = 2
expected_file2_v2['template']['variables'][0][
    'prompt'
] = 'How many producers does this film have?'
expected_file2_v2['template']['variables'][0][
    'description'
] = 'There are usually a lot of producers...'
expected_file2_v2['template']['variables'][0]['type'] = 'int'
expected_file2_v2['template']['variables'][1][
    'skip_if'
] = '{{cookiecutter.producer_credits == False}}'

expected_file2_v3 = deepcopy(expected_file2_v0)
expected_file2_v3['template']['variables'][1]['default'] = "Allan Smithe"
expected_file2_v3['template']['variables'][1]['choices'] = [
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
    'John Ford',
    'Billy Wilder',
]

expected_file2_v4 = deepcopy(expected_file2_v0)
expected_file2_v4['template']['variables'][1]['default'] = "John Ford"
expected_file2_v4['template']['variables'][1]['choices'] = [
    'John Ford',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
    'Billy Wilder',
]

expected_file2_v5 = deepcopy(expected_file2_v0)
expected_file2_v5['template']['variables'][1]['default'] = 'John Ford'
expected_file2_v5['template']['variables'][1]['choices'] = [
    'John Ford',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
]

expected_file2_v6 = deepcopy(expected_file2_v0)
expected_file2_v6['template']['variables'][1]['default'] = "Billy Wilder"
expected_file2_v6['template']['variables'][1]['choices'] = [
    'Billy Wilder',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
    'John Ford',
]

expected_file2_v7 = deepcopy(expected_file2_v0)
expected_file2_v7['template']['variables'][1]['default'] = "Peter Sellers"
expected_file2_v7['template']['variables'][1]['choices'] = [
    'Peter Sellers',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
]


def context_data_serializer():
    """
    Creates a generator of combination:
        ((input file, additional params), expected output)
    """
    context = (
        {'context_file': 'tests/test-generate-context-v2/test.json'},
        {"test": expected_file1_v0},
    )

    context_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {
                'full_name': 'James Patrick Morgan',
                'this_key_ignored': 'not_in_context',
            },
        },
        {"test": expected_file1_v1},
    )

    context_with_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'extra_context': {'email': 'jpm@chase.bk'},
        },
        {"test": expected_file1_v2},
    )

    context_choices_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': {'license': 'Apache2'},
        },
        {
            "test_choices": OrderedDict(
                [
                    ("version", "2.0"),
                    (
                        "template",
                        OrderedDict(
                            [
                                ("name", "cookiecutter-pytest-plugin"),
                                (
                                    "variables",
                                    [
                                        OrderedDict(
                                            [
                                                ("name", "license"),
                                                ("type", "string"),
                                                ("default", "Apache2"),
                                                (
                                                    "choices",
                                                    [
                                                        "Apache2",
                                                        "MIT",
                                                        "BSD3",
                                                        "GNU-GPL3",
                                                        "Mozilla2",
                                                    ],
                                                ),
                                            ]
                                        )
                                    ],
                                ),
                            ]
                        ),
                    ),
                ]
            )
        },
    )
    context_with_default_and_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'full_name': 'Alpha Gamma Five'},
            'extra_context': {'email': 'agamma5@universe.open'},
        },
        {"test": expected_file1_v3},
    )

    context_choices_with_default_not_in_choices = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'orientation': 'landscape'},
        },
        {"test": expected_file1_v0},
    )
    yield context
    yield context_with_default
    yield context_with_extra
    yield context_with_default_and_extra
    yield context_choices_with_default
    yield context_choices_with_default_not_in_choices


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data_serializer())
def test_generate_context(input_params, expected_context):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    assert generate.generate_context(**input_params) == expected_context


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_invalid():
    """
    Test error condition when extra context is not a dictionary or a list
    of dictionaries.
    """

    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context='should_be_a_list_or_a_dictionary',
        )

    msg = "Extra context must be a dictionary or a list of dictionaries!"
    assert msg in str(excinfo.value)


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_list_item_not_dict():
    """
    Test error condition when extra context is a list, but not a list that
    contains a dictionary.
    """
    xtra_context = ['a_string', 'here_too']
    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context=xtra_context,
        )

    msg = "Extra context list item 'a_string' is of type str, should be a dictionary."
    assert msg in str(excinfo.value)


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_list_item_dict_missing_name_field():
    """
    Test error condition when extra context is a list, but not a list that
    contains a dictionary.
    """
    xtra_context = [
        {
            "shouldbename": "author_name",
            "default": "Robert Lewis",
            "prompt": "What's the author's name?",
            "description": "Please enter the author's full name.",
            "type": "string",
        }
    ]
    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context=xtra_context,
        )

    msg = "is missing a 'name' key."
    assert msg in str(excinfo.value)


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_list_item_dict_no_name_field_match():
    """
    Test error condition when extra context is a list, but not a list that
    contains a dictionary.
    """
    xtra_context = [
        {
            "name": "author_name",
            "default": "Robert Lewis",
            "prompt": "What's the author's name?",
            "description": "Please enter the author's full name.",
            "type": "string",
        }
    ]
    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context=xtra_context,
        )

    msg = "No variable found in context whose name matches extra context name 'author_name'"
    assert msg in str(excinfo.value)


def gen_context_data_inputs_expected():
    """
    Creates a generator of combination:
        ((input file, additional params), expected output)
    """
    context_with_valid_extra_0 = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'extra_context': [
                {
                    'name': 'email',
                    'default': 'miles.davis@jazz.gone',
                    'description': 'Enter jazzy email...',
                    'extra_field': 'extra_field_value',
                }
            ],
        },
        {"test": expected_file1_v4},
    )
    # Empty extra context precipitates no ill effect
    context_with_valid_extra_1 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [],
        },
        {"representative": expected_file2_v0},
    )

    # Test the ability to change the variable's name field (since it is used
    # to identify the variable to be modifed) with extra context and to remove
    # a key from the context via the removal token: '<<REMOVE::FIELD>>'
    context_with_valid_extra_2 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credit',
                    'prompt': 'Is there a producer credit on this film?',
                    'description': 'There are usually a lot of producers...',
                },
                {'name': 'director_name', 'skip_if': '<<REMOVE::FIELD>>',},
            ],
        },
        {"representative": expected_file2_v1},
    )
    # Test the ability to change the variable's name field (since it is used
    # to identify the variable to be modifed) with extra context and to also
    context_with_valid_extra_2_B = (
        {
            'context_file': 'tests/test-generate-context-v2/representative_2B.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credit',
                    'prompt': 'Is there a producer credit on this film?',
                    'description': 'There are usually a lot of producers...',
                },
            ],
        },
        {
            "representative_2B": OrderedDict(
                [
                    ("version", "2.0"),
                    (
                        "requires",
                        OrderedDict([("cookiecutter", ">1"), ("python", ">=3.0")]),
                    ),
                    (
                        "template",
                        OrderedDict(
                            [
                                ("name", "cc-representative"),
                                (
                                    "variables",
                                    [
                                        OrderedDict(
                                            [
                                                ("name", "producer_credit"),
                                                ("default", True),
                                                (
                                                    "prompt",
                                                    "Is there a producer credit on this film?",
                                                ),
                                                (
                                                    "description",
                                                    "There are usually a lot of producers...",
                                                ),
                                                ("type", "boolean"),
                                            ]
                                        ),
                                        OrderedDict(
                                            [
                                                ("name", "director_name"),
                                                ("default", "Allan Smithe"),
                                                (
                                                    "prompt",
                                                    "What's the Director's full name?",
                                                ),
                                                ("prompt_user", True),
                                                (
                                                    "description",
                                                    "The default director is not proud "
                                                    "of their work, we hope you are.",
                                                ),
                                                ("hide_input", False),
                                                (
                                                    "choices",
                                                    [
                                                        "Allan Smithe",
                                                        "Ridley Scott",
                                                        "Victor Fleming",
                                                        "John Houston",
                                                        "{{cookiecutter.producer_credit}}",
                                                    ],
                                                ),
                                                ("validation", "^[a-z][A-Z]+$"),
                                                (
                                                    "validation_flags",
                                                    ["verbose", "ascii"],
                                                ),
                                                (
                                                    "skip_if",
                                                    "{{cookiecutter.producer_credit == False}}",
                                                ),
                                                ("type", "string"),
                                            ]
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ),
                ]
            )
        },
    )
    # test that any other references in other variables that might use the
    # original variable name get updated as well.

    # Test changing variable's name field value, default field, prompt field,
    # and changing the type
    context_with_valid_extra_3 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credits',
                    'default': 2,
                    'prompt': 'How many producers does this film have?',
                    'description': 'There are usually a lot of producers...',
                    'type': "int",
                }
            ],
        },
        {"representative": expected_file2_v2},
    )
    # Test changing choices field without changing the default, but default
    # does not change because the first position in choices matches default
    context_with_valid_extra_4 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'choices': [
                        'Allan Smithe',
                        'Ridley Scott',
                        'Victor Fleming',
                        'John Houston',
                        'John Ford',
                        'Billy Wilder',
                    ],
                }
            ],
        },
        {"representative": expected_file2_v3},
    )
    # Test changing choices field and changing the default
    context_with_valid_extra_5 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'default': 'John Ford',
                    'choices': [
                        'Allan Smithe',
                        'Ridley Scott',
                        'Victor Fleming',
                        'John Houston',
                        'John Ford',
                        'Billy Wilder',
                    ],
                }
            ],
        },
        {"representative": expected_file2_v4},
    )
    # Test changing the default, but not the choices field, yet seeing choices field re-ordered
    # to put default value in first location
    context_with_valid_extra_6 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [{'name': 'director_name', 'default': 'John Ford',}],
        },
        {"representative": expected_file2_v5},
    )
    # Test changing choices field without changing the default, but default
    # does get changee because the first position in choices field chagned
    context_with_valid_extra_7 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'choices': [
                        'Billy Wilder',
                        'Allan Smithe',
                        'Ridley Scott',
                        'Victor Fleming',
                        'John Houston',
                        'John Ford',
                    ],
                }
            ],
        },
        {"representative": expected_file2_v6},
    )
    # Test changing the default value with a value that is not in choices,
    # we should see the choice first position get updated.
    context_with_valid_extra_8 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [{'name': 'director_name', 'default': 'Peter Sellers',}],
        },
        {"representative": expected_file2_v7},
    )
    yield context_with_valid_extra_0
    yield context_with_valid_extra_1
    yield context_with_valid_extra_2
    yield context_with_valid_extra_2_B
    yield context_with_valid_extra_3
    yield context_with_valid_extra_4
    yield context_with_valid_extra_5
    yield context_with_valid_extra_6
    yield context_with_valid_extra_7
    yield context_with_valid_extra_8


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize(
    'input_params, expected_context', gen_context_data_inputs_expected()
)
def test_generate_context_with_extra_context_dictionary(
    input_params, expected_context, monkeypatch
):
    """
    Test the generated context with extra content overwrite to multiple fields,
    with creation of new fields NOT allowed.
    """
    assert OrderedDict(generate.generate_context(**input_params)) == OrderedDict(
        expected_context
    )


@pytest.mark.usefixtures('clean_system')
def test_raise_exception_when_attempting_to_remove_mandatory_field():
    """
    Test that ValueError is raised if attempt is made to remove a mandatory
    field -- the default field.
    The other mandatory field, name, cannot be removed because it has to be
    used to specify which variable to remove.
    """
    xtra_context = [
        {'name': 'director_name', 'default': '<<REMOVE::FIELD>>',},
    ]

    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/representative.json',
            default_context=None,
            extra_context=xtra_context,
        )

    assert "Cannot remove mandatory 'default' field" in str(excinfo.value)
