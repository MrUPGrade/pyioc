# coding=utf-8

import pytest
from mock import Mock

from pyioc.containers import *
from pyioc.locators import ObjectLocator
from tests.fakes import TestClass1


class Test_SimpleIdParser(object):
    def test_simple_id_parser(self):
        parser = SimpleIdParser()
        ret = parser.parse('test')
        assert ret.id == 'test'
        assert ret.namespace is None


class Test_NamespaceIdParser(object):
    def test_parse_namespace_from_id(self):
        parser = NamespaceIdParser(separator=':')
        ret = parser.parse('namespace:key')

        assert ret.namespace == 'namespace'
        assert ret.id == 'key'

    def test_if_parse_throws_type_error_when_id_not_string(self):
        parser = NamespaceIdParser()
        with pytest.raises(TypeError):
            parser.parse(1)

    def test_if_parse_get_namespace_based_on_provided_separator(self):
        parser = NamespaceIdParser(separator=';')
        ret = parser.parse('namespace;key')

        assert ret.namespace == 'namespace'
        assert ret.id == 'key'

    def test_if_parse_get_namespace_based_on_provided_separator_with_multiple_chars(self):
        parser = NamespaceIdParser(separator='__')
        ret = parser.parse('namespace__key')

        assert ret.namespace == 'namespace'
        assert ret.id == 'key'

    def test_if_parse_get_key_when_simple_id_provided(self):
        parser = NamespaceIdParser(separator=';')
        ret = parser.parse('key')

        assert ret.namespace is None
        assert ret.id == 'key'

    def test_if_parse_raises_error_when_more_then_one_ocurance_of_separator(self):
        parser = NamespaceIdParser(separator=';')
        with pytest.raises(FormatError):
            parser.parse('to;many;separators')


class Test_SimpleContainer(object):
    @staticmethod
    @pytest.fixture
    def mock_locator():
        mock = Mock(spec=ObjectLocator)
        return mock

    @classmethod
    def container(cls):
        return SimpleContainer

    def test_if_providing_locator_not_derived_from_abc_raises_error(self):
        container_class = self.container()

        with pytest.raises(TypeError):
            container_class(locator={})

    def test_register_singleton_lazy(self, mock_locator):
        container_class = self.container()
        container = container_class(name='name', locator=mock_locator)
        container.register_callable('key', TestClass1, lifetime=InstanceLifetime.SingletonLazy)

        args = mock_locator.register.call_args_list[0][0]
        assert args[0] == 'key'
        assert isinstance(args[1], providers.LazySingleInstanceProvider)

    def test_register_singleton_eager(self, mock_locator):
        class FakeClass(object):
            pass

        container_class = self.container()
        container = container_class(locator=mock_locator)
        container.register_callable('key', FakeClass, lifetime=InstanceLifetime.SingletonEager)

        args = mock_locator.register.call_args_list[0][0]
        assert args[0] == 'key'
        assert isinstance(args[1], providers.EagerSingleInstanceProvider)

    def test_register_object(self, mock_locator):
        container_class = self.container()
        container = container_class(locator=mock_locator)
        container.register_callable('key', TestClass1)

        args = mock_locator.register.call_args_list[0][0]
        assert args[0] == 'key'
        assert isinstance(args[1], providers.NewInstancesProvider)

    def test_register_class_fatory(self, mock_locator):
        container_class = self.container()
        container = container_class(locator=mock_locator)
        container.register_callable_with_deps('key', TestClass1)

        args = mock_locator.register.call_args_list[0][0]
        assert args[0] == 'key'
        assert isinstance(args[1], providers.NewInstancesWithDepsProvider)

    def test_register_class_fatory_singleton_eager(self, mock_locator):
        container_class = self.container()
        container = container_class(locator=mock_locator)
        container.register_callable_with_deps('key', TestClass1, lifetime=InstanceLifetime.SingletonEager)

        args = mock_locator.register.call_args_list[0][0]
        assert args[0] == 'key'
        assert isinstance(args[1], providers.EagerSingleInstanceWithDepsProvider)

    def test_register_class_fatory_singleton_lazy(self, mock_locator):
        container_class = self.container()
        container = container_class(locator=mock_locator)
        container.register_callable_with_deps('key', TestClass1, lifetime=InstanceLifetime.SingletonLazy)

        args = mock_locator.register.call_args_list[0][0]
        assert args[0] == 'key'
        assert isinstance(args[1], providers.LazySingleInstanceWithDepsProvider)

    def test_if_register_class_throws_error_when_wrong_life_time_provided(self):
        container_class = self.container()
        container = container_class()

        with pytest.raises(TypeError):
            container.register_callable_with_deps('key', TestClass1, lifetime=1)

    def test_if_register_callable_throws_error_when_wrong_life_time_provided(self):
        container_class = self.container()
        container = container_class()

        with pytest.raises(TypeError):
            container.register_callable('key', TestClass1, lifetime=1)

    def test_if_container_has_correct_name(self):
        container_class = self.container()
        localtor = container_class('my_name')
        assert localtor.name == 'my_name'


class Test_NamespaceContainer(Test_SimpleContainer):
    @classmethod
    def container(cls):
        return NamespacedContainer

    def test_adding_sub_containers(self):
        container_class = self.container()
        container = container_class('container')
        container.add_sub_container(SimpleContainer('sub_container_1'))

    def test_if_adding_and_getting_sub_container_return_same_instance(self):
        container_class = self.container()
        container = container_class('container')
        sub_container = SimpleContainer(name='sub_container')
        container.add_sub_container(sub_container)
        ret = container.get_sub_container('sub_container')

        assert isinstance(ret, SimpleContainer)
        assert ret is sub_container

    def test_if_adding_already_registered_sub_container_throws_error(self):
        container_class = self.container()
        container = container_class('container')
        sub_container = SimpleContainer(name='sub_container')

        container.add_sub_container(sub_container)
        with pytest.raises(KeyError):
            container.add_sub_container(sub_container)

    def test_if_adding_sub_container_that_is_not_a_container_object_raises_error(self):
        container_class = self.container()
        container = container_class('container')

        with pytest.raises(TypeError):
            container.add_sub_container({})
