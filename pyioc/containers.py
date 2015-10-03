# coding=utf-8
from __future__ import absolute_import

from future.standard_library import install_aliases

install_aliases()

from collections import namedtuple
from enum import Enum
import abc
import six

from pyioc.locators import ObjectLocator, LocatorBase

import pyioc.providers as providers

InstanceId = namedtuple('InstanceId', ('id', 'namespace'))


class FormatError(Exception):
    pass


class InstanceLifetime(Enum):
    """
    Enum representing possible lifetimes of an object in the container.
    """
    NewInstancePerCall = 1
    SingletonEager = 2
    SingletonLazy = 3


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
    def __init__(self, name='', locator=None):
        if locator is not None:
            if not isinstance(locator, LocatorBase):
                raise TypeError('locator must be instance of class derived from %s' % LocatorBase.__class__.__name__)
            self._locator = locator
        else:
            self._locator = ObjectLocator()
        self._name = name

    def register_object(self, key, obj):
        provider = providers.ObjectProvider(obj)
        self._register_provider_for_key(key, provider)

    def register_callable(self, key, callable_object, lifetime=InstanceLifetime.NewInstancePerCall):
        if lifetime == InstanceLifetime.NewInstancePerCall:
            provider = providers.NewInstancesProvider(callable_object)
        elif lifetime == InstanceLifetime.SingletonEager:
            provider = providers.EagerSingleInstanceProvider(callable_object)
        elif lifetime == InstanceLifetime.SingletonLazy:
            provider = providers.LazySingleInstanceProvider(callable_object)
        else:
            raise TypeError('Unsuported instance lifetime.')

        self._register_provider_for_key(key, provider)

    def register_callable_with_deps(self, key, callable_object, lifetime=InstanceLifetime.NewInstancePerCall):
        if lifetime == InstanceLifetime.NewInstancePerCall:
            provider = providers.NewInstancesWithDepsProvider(callable_object, self)
        elif lifetime == InstanceLifetime.SingletonEager:
            provider = providers.EagerSingleInstanceWithDepsProvider(callable_object, self)
        elif lifetime == InstanceLifetime.SingletonLazy:
            provider = providers.LazySingleInstanceWithDepsProvider(callable_object, self)
        else:
            raise TypeError('Unsuported instance lifetime.')

        self._register_provider_for_key(key, provider)

    def get(self, key):
        return self._resolve(key)

    @property
    def name(self):
        return self._name

    def _resolve(self, key):
        return self._locator.get(key).get()

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
            raise KeyError('Container with name: "%s" is already registerd' % name)

        self._sub_containers[container.name] = container

    def get_sub_container(self, name):
        return self._sub_containers[name]

    def _resolve(self, id):
        if isinstance(id, str):
            instance_id = self._name_resolver.parse(id)
            if instance_id.namespace:
                container = self._sub_containers[instance_id.namespace]
                return container.get(instance_id.id)
            else:
                provider = self._locator.get(instance_id.id)
                return provider.get()
        else:
            provider = self._locator.get(id)
            return provider.get()

