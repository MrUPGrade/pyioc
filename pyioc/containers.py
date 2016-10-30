# coding=utf-8
from __future__ import absolute_import

from future.standard_library import install_aliases

install_aliases()

import abc
import six

from future.utils import iteritems
from collections import namedtuple
from enum import Enum

from pyioc.locators import ObjectLocator, LocatorBase

import pyioc.providers as providers

InstanceId = namedtuple('InstanceId', ('id', 'namespace'))
"""
Namedtuple defining ID of instance in namespace container.
"""


class FormatError(Exception):
    pass


class InstanceLifetime(Enum):
    """
    Enum representing possible lifetimes of an object in the container.
    """
    NewInstancePerCall = 0
    """
    New instance will be created every time container will be ask for object on given key.
    """
    Singleton = 1
    """
    New instance will be created the first time container will be asked for object under given key. Both the callable
    and object will be stored in the container.
    """


@six.add_metaclass(abc.ABCMeta)
class IdParserBase(object):
    @abc.abstractmethod
    def parse(self, key):
        pass


class SimpleIdParser(IdParserBase):
    def parse(self, key):
        return InstanceId(key, None)


class NamespaceIdParser(IdParserBase):
    def __init__(self, separator='__'):
        self._separator = separator

    def parse(self, key):
        if not isinstance(key, str):
            raise TypeError('Key argument must be string')

        values = key.split(self._separator)

        if len(values) == 1:
            return InstanceId(values[0], None)

        elif len(values) == 2:
            return InstanceId(values[1], values[0])

        else:
            raise FormatError('Wrong key format. Expected namespace%sclass' % self._separator)


class SimpleContainer(object):
    """
    a
    """

    def __init__(self, name='', locator=None):
        """
        Raises TypeError when locator object is not derived from LocatorBase class.

        :param name: Name for a container.
        :param locator: Locator instance that will be used for storing objects in the container.
        """
        if locator is not None:
            if not isinstance(locator, LocatorBase):
                raise TypeError('locator must be instance of class derived from %s' % LocatorBase.__class__.__name__)
            self._locator = locator
        else:
            self._locator = ObjectLocator()
        self._name = name

    def register_object(self, key, obj):
        """
        Registers object for a given key.

        :param key: Key under which the object will be registered
        :param obj: Object
        """
        provider = providers.ObjectProvider(obj)
        self._register_provider_for_key(key, provider)

    def register_callable(self, key, callable_object, lifetime=InstanceLifetime.NewInstancePerCall):
        """
        Registers a callable object that will be used to create a new instance of an object that will be returned upon
        calling the get_instance() method.

        Based on the lifetime parameter, either the callable will be stored, and called whenever object is needed, or
        the callable will be called on registering, and the returned object will be stored.

        :param key:
        :param callable_object: Callable object that will be used to create new object.
        :param lifetime: Specified lifetime of an object that is produced by callable.
        :return:
        """
        if lifetime == InstanceLifetime.NewInstancePerCall:
            provider = providers.NewInstancesProvider(callable_object)
        elif lifetime == InstanceLifetime.Singleton:
            provider = providers.LazySingleInstanceProvider(callable_object)
        else:
            raise TypeError('Unsupported instance lifetime.')

        self._register_provider_for_key(key, provider)

    def register_callable_with_deps(self, key, callable_object, lifetime=InstanceLifetime.NewInstancePerCall):
        if lifetime == InstanceLifetime.NewInstancePerCall:
            provider = providers.NewInstancesWithDepsProvider(callable_object, self)
        elif lifetime == InstanceLifetime.Singleton:
            provider = providers.LazySingleInstanceWithDepsProvider(callable_object, self)
        else:
            raise TypeError('Unsupported instance lifetime.')

        self._register_provider_for_key(key, provider)

    def resolve(self, key, context=None):
        """
        Return instance based on what was registered for a given key.

        :param key: Key under which the object or callable was registered.
        :return: Instance related to that key.
        """
        return self._resolve(key, context)

    def build(self, cls, context=None):
        """
        Build a new instance of class cls injecting dependencies of an object from objects registered in the container.

        :param cls: Class of which object to build.
        :return:
        """
        provider = providers.NewInstancesWithDepsProvider(cls, self)
        return provider.get_instance(context)

    @property
    def name(self):
        """
        The name of the container.

        :return: str with the name of the container.
        """
        return self._name

    def get_keys(self):
        """
        Get all keys registered in that container.

        :return: List of all keys registered in that container.
        """
        return self._locator.get_keys()

    def _resolve(self, key, context=None):
        if context:
            try:
                item = context[key]
            except KeyError:
                pass
            else:
                return item

        instance_provider = self._locator.locate(key)
        return instance_provider.get_instance(context)

    def _register_provider_for_key(self, id, provider):
        self._locator.register(id, provider)


class NamespacedContainer(SimpleContainer):
    def __init__(self, name='', locator=None, name_resolver=None):
        super(NamespacedContainer, self).__init__(name=name, locator=locator)
        self._sub_containers = {}
        self._name_resolver = name_resolver or NamespaceIdParser()

        self._sub_containers[self.name] = self

    def add_sub_container(self, container):
        try:
            name = container.name
        except:
            raise TypeError('Locator must be of type: "%s"  or its subclass' % SimpleContainer.__class__.__name__)

        if name in self._sub_containers.keys():
            raise KeyError('Container with name: "%s" is already registered' % name)

        self._sub_containers[container.name] = container

    def get_sub_container(self, name):
        return self._sub_containers[name]

    def get_all_keys(self):
        """
        Get all keys from container and all sub containers.
        This container keys will be stored under '' key in dictionary.
        All sub containers will be stored under container name.

        :return: Dictionary of keys registered in container and all sub containers.
        """
        result = {}
        result[self.name] = self.get_keys()

        for name, container in iteritems(self._sub_containers):
            result[name] = container.get_keys()

        return result

    def _resolve(self, id, context=None):
        if isinstance(id, str):
            instance_id = self._name_resolver.parse(id)

            if instance_id.namespace:
                container = self._sub_containers[instance_id.namespace]
                return container.resolve(instance_id.id, context)
            else:
                if context:
                    try:
                        item = context[instance_id.id]
                    except KeyError:
                        pass
                    else:
                        return item

                provider = self._locator.locate(instance_id.id)
                return provider.get_instance(context)

        else:
            provider = self._locator.locate(id)
            return provider.get_instance(context)
