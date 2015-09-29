# coding=utf-8
from __future__ import absolute_import
from future.standard_library import install_aliases

install_aliases()

import inspect
import six
import abc


class SignatureError(TypeError):
    pass


def _check_if_init_implemented(obj):
    if six.PY2:
        if inspect.ismethod(obj.__init__):
            return True
    if six.PY3:
        if inspect.isfunction(obj.__init__):
            return True

    return False


def validate_if_callable_without_args(obj):
    if not callable(obj):
        raise TypeError('Object have to be callable')

    if inspect.isclass(obj):
        if _check_if_init_implemented(obj):
            obj_to_inspect = obj.__init__
        else:
            return
    else:
        obj_to_inspect = obj

    spec = inspect.getargspec(obj_to_inspect)
    args = spec.args
    par_len = len(args)
    if par_len > 1:
        raise SignatureError('Callable cant have arguments')
    elif par_len == 1:
        if args[0] != 'self':
            raise SignatureError('callable cant have arguments')


@six.add_metaclass(abc.ABCMeta)
class ProviderBase(object):
    @abc.abstractmethod
    def get(self):
        pass


class ObjectProvider(ProviderBase):
    def __init__(self, obj):
        self._obj = obj

    def get(self):
        return self._obj


class NewInstancesProvider(ProviderBase):
    def __init__(self, callable_object):
        validate_if_callable_without_args(callable_object)
        self._callable_object = callable_object

    def get(self):
        return self._callable_object()


class LazySingleInstanceProvider(ProviderBase):
    def __init__(self, callable_object):
        validate_if_callable_without_args(callable_object)
        self._instance = None
        self._callable_object = callable_object

    def get(self):
        if not self._instance:
            self._instance = self._callable_object()
        return self._instance


class EagerSingleInstanceProvider(ProviderBase):
    def __init__(self, callable_object):
        validate_if_callable_without_args(callable_object)
        self._instance = callable_object()

    def get(self):
        return self._instance


class NewInstancesWithDepsProvider(ProviderBase):
    def __init__(self, callable_object, container):
        if not callable(callable_object):
            raise TypeError('Argument "callable_object" must be a callable')

        self._callable_object = callable_object
        self._container = container

    def get(self):
        return self._build_object()

    def _build_object(self):
        if inspect.isclass(self._callable_object):
            if _check_if_init_implemented(self._callable_object):
                args = inspect.getargspec(self._callable_object.__init__).args
            else:
                args = ()
        else:
            args = inspect.getargspec(self._callable_object).args

        new_args = []
        for arg in args:
            if arg == 'self':
                continue

            new_args.append(self._container.get(arg))

        if new_args:
            return self._callable_object(*new_args)

        return self._callable_object()


class EagerSingleInstanceWithDepsProvider(NewInstancesWithDepsProvider):
    def __init__(self, callable_object, container):
        super(EagerSingleInstanceWithDepsProvider, self).__init__(callable_object, container)
        self._instance = self._build_object()

    def get(self):
        return self._instance


class LazySingleInstanceWithDepsProvider(NewInstancesWithDepsProvider):
    def __init__(self, callable_object, container):
        super(LazySingleInstanceWithDepsProvider, self).__init__(callable_object, container)
        self._instance = None

    def get(self):
        if not self._instance:
            self._instance = self._build_object()
        return self._instance
