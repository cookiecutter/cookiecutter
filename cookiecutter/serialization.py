# -*- coding: utf-8 -*-

# from __future__ import unicode_literals

import json
import inspect
import re
import pickle
import base64
import sys

from abc import ABCMeta, abstractmethod
from cookiecutter.exceptions import UnknownSerializerType, \
    BadSerializedStringFormat, InvalidSerializerType, InvalidType


def get_context():
    """
    high level context provider API to be used by hooks
    it reads serialized context from stdin
    """
    serializer = SerializationFacade()
    return serializer.deserialize(sys.stdin.readlines()[0])


def put_context(context):
    """
    high level context updater API to be used by hooks
    it serializes a given context object
    :param context: context dictionary
    """
    print(SerializationFacade().serialize(context))


class AbstractSerializer(object):
    """
    abstract base class for serializers
    """
    __metaclass__ = ABCMeta

    def serialize(self, subject):
        """
        serialize a given subject to its bytes string representation
        :param subject: the subject to serialize
        """
        serialized = self._do_serialize(subject)

        return base64.encodestring(self.__encode(serialized))

    def deserialize(self, bstring):
        """
        deserialize a given bytes string to its Python object
        :param bstring: the bytes string to deserialize
        """
        serialized = base64.decodestring(bstring)

        return self._do_deserialize(self.__decode(serialized))

    @abstractmethod
    def _do_serialize(self, subject):
        """
        abstract method to be implemented by serializer
        it should do the serialization
        :param subject: the subject to serialize
        """

    @abstractmethod
    def _do_deserialize(self, string):
        """
        abstract method to be implemented by serializer
        it should do the deserialization
        :param string: the string to deserialize
        """

    def __encode(self, subject):
        """
        sanitize encoding for a given subject, if needed
        :param subject: the subject to treat
        """
        try:
            sanitized = subject.encode()
        except:
            sanitized = subject

        return sanitized

    def __decode(self, subject):
        """
        revert encoding sanitization for a given subject, if it has been done
        previously
        :param subject: the subject to treat
        """
        try:
            original = subject.decode()
        except:
            original = subject

        return original


class JsonSerializer(AbstractSerializer):
    """
    The JSON serializer is the default serializer registered by the
    serialization facade
    It can serve as an example of the API that must implement custom
    serializers
    """

    def _do_serialize(self, subject):
        """
        serialize a given subject to its JSON representation
        :param subject: the subject to serialize
        """
        return json.dumps(subject)

    def _do_deserialize(self, string):
        """
        deserialize a given JSON string to its Python object
        :param string: the string to deserialize
        """
        return json.loads(string)


class PickleSerializer(AbstractSerializer):
    """
    The Pickle serializer should be used to serialize objects
    """

    def _do_serialize(self, subject):
        """
        serialize a given subject to its string representation
        :param subject: the subject to serialize
        """
        return pickle.dumps(subject, 2)

    def _do_deserialize(self, string):
        """
        deserialize a given string to its Python object
        :param string: the string to deserialize
        """
        return pickle.loads(string)


class SerializationFacade(object):
    """
    The SerializationFacade is the public API that customers should use.
    """

    def __init__(self, serializers=None):
        self.__serializers = {}
        self.__current_type = 'json'
        self.register('json', JsonSerializer)

        if serializers is not None:
            for type in serializers:
                self.register(type, serializers[type])

    def serialize(self, subject):
        """
        serialize a given subject using a specific type (JSON by default)
        :param subject: the subject to serialize
        :param type: the serializer type to use
        """
        return self.__current_type + '|' \
            + self.__decode(
                self.__get_serializer(
                    self.__current_type).serialize(subject)) \
            + '$'

    def deserialize(self, string):
        """
        deserialize a given string which must be of the form:
        serializer_type|serialized_object
        :param string: the string to deserialize
        """
        parts = self.__get_last_serialized_part(string).split('|')

        if len(parts) < 2:
            raise BadSerializedStringFormat(
                message='Serialized string should be of the form '
                'serializer_type|serialized_string$'
            )

        return self.__get_serializer(parts[0]).deserialize(
            self.__encode(parts[1]))

    def use(self, type):
        """
        define the type of the serializer to use
        :param type: the serializer type
        """
        self.__current_type = type

        return self

    def get_type(self):
        """
        get the type of the current serializer
        """
        return self.__current_type

    def register(self, type, serializer):
        """
        register a custom serializer
        :param type: type of the serializer to register
        :param serializer: custom serializer to register
        """
        self.__check_type(type)
        oserializer = serializer() if inspect.isclass(
            serializer) else serializer
        self.__check_serializer_api(oserializer)
        self.__serializers[type] = oserializer

    def __get_type_pattern(self):
        """
        get the validation pattern for serializer types
        """
        return '[a-zA-Z_][a-zA-Z_][a-zA-Z_0-9\-\.]+'

    def __get_serializer(self, type):
        """
        get the serializer of a given type
        :param type: type of the target serializer
        """
        if type in self.__serializers:
            self.__current_type = type
            return self.__serializers[type]

        else:
            raise UnknownSerializerType(type)

    def __check_serializer_api(self, serializer):
        """
        ensure that a given serializer implements the expected API
        :param serializer: serializer to check its public interface
        """
        if not isinstance(serializer, AbstractSerializer):
            raise InvalidType(AbstractSerializer.__name__)

    def __check_type(self, type):
        """
        ensure a given type is well formed and does not contain invalid chars
        :param type: the type to check
        """
        pattern = '^' + self.__get_type_pattern() + '$'
        if not re.match(pattern, type):
            raise InvalidSerializerType()

    def __get_last_serialized_part(self, string):
        """
        extract the last serialized part found in a mixed string
        """
        pattern = self.__get_type_pattern() + '\|[^\$]+'
        serialized_parts = re.findall(pattern, string)

        return serialized_parts[-1] if serialized_parts else string

    def __decode(self, serialized):
        """
        prepare the serialized string for crossprocessing
        :param serialized: serialized string to treat
        """
        return serialized.decode().replace("\n", "*")

    def __encode(self, encoded):
        """
        prepare the encoded string for deserialization
        :param encoded: encoded string to treat
        """
        return encoded.replace("*", "\n").encode()
