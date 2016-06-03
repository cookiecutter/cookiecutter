#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_serializers
----------------

Tests for `cookiecutter.serialization` serializer classes.
"""

from __future__ import unicode_literals

import pytest

from cookiecutter.serialization import \
    JsonSerializer, PickleSerializer, AbstractSerializer


class __Dummy(object):
    """
    fixture class
    """

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def __eq__(self, other):
        return self.get_name() == other


class __Py27Serializer(AbstractSerializer):
    """
    fixture class to check some non covered part of the AbstractSerializer
    under python 2.7
    """

    def _do_serialize(self, subject):
        """
        serialize a given subject to its JSON representation
        :param subject: the subject to serialize
        """
        return subject

    def _do_deserialize(self, bstring):
        """
        deserialize a given JSON string to its Python object
        :param bstring: the bytes string to deserialize
        """
        return bstring


@pytest.fixture
def get_serializers():
    """
    serializer provider
    """
    return {
        JsonSerializer: {"key": "value"},
        PickleSerializer: __Dummy('dummy'),
        __Py27Serializer: 'string'
    }


class TestSerialization(object):

    def test_serialize_return_type(self):
        """
        The serialize method should return a bytes string
        """
        serializers = get_serializers()
        for kclass in serializers:
            assert type(kclass().serialize(serializers[kclass])) == bytes

    def test_deserialize(self):
        """
        The deserialize method should return the previous object
        """
        serializers = get_serializers()
        for kclass in serializers:
            serializer = kclass()
            obj = serializers[kclass]
            string = serializer.serialize(obj)
            assert obj == serializer.deserialize(string)
