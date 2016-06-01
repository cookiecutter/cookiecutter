#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_serialization
------------------

Tests for `cookiecutter.serialization` module.
"""

import pytest

from cookiecutter.serialization import SerializationFacade
from cookiecutter.exceptions import \
    NotRegisteredSerializer, MissingRequiredMethod, BadSerializedStringFormat


@pytest.fixture
def get_context():
    """
    helper method to get a bunch of context objects
    """
    return {
        'object': {
            "my_key": "my_val"
        },
        'json': 'json|{"my_key": "my_val"}'
    }


@pytest.fixture
def get_serializers():
    """
    helper method to get a bunch of serializers
    """
    class NoSerialize(object):
        def deserialize(self, string):
            return {}

    class NoDeserialize(object):
        def serialize(self, subject):
            return 'serialized'

    class DummySerializer(object):
        def serialize(self, subject):
            return 'serialized'

        def deserialize(self, string):
            return get_context()['object']

    return {
        'serialize': NoSerialize,
        'deserialize': NoDeserialize,
        'dummy': DummySerializer
    }


class TestSerialization(object):

    def test_default_serialize(self):
        """
        serialize a context object with the default available serializer
        """
        assert get_context()['json'] == SerializationFacade().serialize(
            get_context()['object'])

    def test_default_deserialize(self):
        """
        deserialize a context string with the default available serializer
        """

        assert get_context()['object'] == SerializationFacade().deserialize(
            get_context()['json'])

    def test_not_registered_serializer_during_serialization(self):
        """
        ensure a non registered serializer cannot be called during
        serialization
        """
        with pytest.raises(NotRegisteredSerializer) as excinfo:
            type = 'not_registered'
            SerializationFacade().serialize(
                get_context()['object'], type)

            assert type in excinfo.message

    def test_not_registered_serializer_during_deserialization(self):
        """
        ensure a non registered serializer cannot be called during
        deserialization
        """
        with pytest.raises(NotRegisteredSerializer) as excinfo:
            type = 'not_registered'
            SerializationFacade().deserialize(type + '|somestring')

            assert type in excinfo.message

    def test_register_serializer(self):
        """
        register a custom serializer class
        """
        type = 'dummy'
        serialized = type + '|serialized'
        facade = SerializationFacade()
        facade.register(type, get_serializers()[type])

        assert serialized == facade.serialize(
            get_context()['object'], type)
        assert get_context()['object'] == facade.deserialize(
            serialized)

    def test_register_serializer_accepts_object(self):
        """
        register a custom serializer instance
        """
        type = 'dummy'
        serialized = type + '|serialized'
        facade = SerializationFacade()
        facade.register(type, get_serializers()[type]())

        assert serialized == facade.serialize(
            get_context()['object'], type)

    def test_serializer_api_check(self):
        """
        enforce the given serializer to implement the serializer API
        """
        types = ['serialize', 'deserialize']
        for type in types:
            with pytest.raises(MissingRequiredMethod) as excinfo:
                SerializationFacade().register(
                    type, get_serializers()[type]
                )

            assert type in excinfo.value.message

    def test_get_serialization_type(self):
        """
        get the type of the current serializer
        """
        type = 'dummy'
        facade = SerializationFacade()
        facade.register(type, get_serializers()[type])

        assert 'json' == facade.get_type()
        facade.deserialize(type + '|some string')
        assert type == facade.get_type()

    def test_existing_serializer_can_be_replaced(self):
        """
        overwrite an existing serializer with a custom one
        """
        type = 'json'
        facade = SerializationFacade()
        facade.register(type, get_serializers()['dummy'])

        assert 'json|serialized' == facade.serialize(
            get_context()['object'], type)

    def test_serializer_list_can_be_set_at_facade_initialization(self):
        """
        initialize the serialization facade with a bunch of serializers
        """
        type = 'dummy'
        serialized = type + '|serialized'
        dict = {
            type: get_serializers()[type]
        }
        facade = SerializationFacade(dict)

        assert serialized == facade.serialize(
            get_context()['object'], type)

    def test_missing_type_in_serialized_string(self):
        """
        ensure that a string passed to the deserialize method contains the
        serializer type
        """
        expected = 'Serialized string should be of the form'
        with pytest.raises(BadSerializedStringFormat) as excinfo:
            SerializationFacade().deserialize('{"my_key": "my_val"}')

        assert expected in excinfo.value.message
