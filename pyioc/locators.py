# coding=utf-8
"""
Module containing implementation of the service locator.
"""
from __future__ import absolute_import

from future.standard_library import install_aliases

install_aliases()

import inspect
import six
import abc


class KeyToStringConverter(object):
    def generate_key(self, obj):
        if inspect.isclass(obj):
            return obj.__name__
        elif inspect.isfunction(obj):
            return 'func_%s' % obj.__name__
        else:
            return type(obj).__name__


class UnregisteredKeyError(KeyError):
    def __init__(self, key):
        self._key = key

    def __str__(self):
        return 'There is no object registered for the given "%s" key' % self._key

    def __unicode__(self):
        return self.__str__()


class KeyAlreadyRegisteredError(KeyError):
    def __init__(self, key):
        self._key = key

    def __str__(self):
        return 'There is already an object registered for the "%s" key' % self._key

    def __unicode__(self):
        return self.__str__()


@six.add_metaclass(abc.ABCMeta)
class LocatorBase(object):
    """
    Abstract Class Base declaring locator interface.
    """

    @abc.abstractmethod
    def register(self, key, obj):
        pass

    @abc.abstractmethod
    def locate(self, key):
        pass

    @abc.abstractmethod
    def get_or_default(self, key, default):
        pass

    def is_key_registered(self, key):
        pass


class ObjectLocator(LocatorBase):
    """
    Simple object locator implementation.
    """

    def __init__(self):
        self._objects = {}

    def register(self, key, obj):
        """
         Register object in locator under a specified key.

         :param key: Key under which object will be registered.
         :param obj: Object to register.
         """
        if key in self._objects:
            raise KeyAlreadyRegisteredError(key)

        self._set_instance(key, obj)

    def locate(self, key):
        """
        Returns the object registered for a given key.

        :param key: Key under which object was registered.
        :return: Object registered under the given key.
        """
        try:
            instance = self._get_instance(key)
        except KeyError:
            raise UnregisteredKeyError(key)

        return instance

    def get_or_default(self, key, default):
        """
        Gets the object for a given key. If the key is not present in the locator, returns value of *default* parameter.

        :param key: Key under which object was registered.
        :param default: Default value, if there is no object registered for a given key.
        :return: Object registered under the given key, or default.
        """
        try:
            instance = self._get_instance(key)
        except KeyError:
            return default

        return instance

    def is_key_registered(self, key):
        """
        Checks if there is object registered for a given key in the locator.

        :param key: Key to look for.
        :return: True if there is a key in the locator, otherwise False.
        """
        try:
            self._objects[key]
        except KeyError:
            return False
        return True

    def get_keys(self):
        return list(self._objects.keys())

    def _get_instance(self, key):
        return self._objects[key]

    def _set_instance(self, key, value):
        self._objects[key] = value
