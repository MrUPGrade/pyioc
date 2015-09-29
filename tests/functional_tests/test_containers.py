# coding=utf-8

from pyioc.locators import ObjectLocator
from pyioc.containers import SimpleContainer, NamespacedContainer, InstanceLifetime
from tests.fakes import *


class Test_SimpleContainer(object):
    @classmethod
    def get_container(cls):
        return SimpleContainer

    def test_registering_singleton(self):
        locator = ObjectLocator()
        container_class = self.get_container()
        container = container_class()
        container._locator = locator
        container.register_callable(TEST_CLASS_1_NAME, TestClass1, lifetime=InstanceLifetime.SingletonLazy)

        ret1 = locator.is_key_registered(TEST_CLASS_1_NAME)
        assert ret1 is True

        ret2 = container.get(TEST_CLASS_1_NAME)
        ret3 = container.get(TEST_CLASS_1_NAME)

        assert isinstance(ret2, TestClass1)
        assert id(ret2) == id(ret3)

    def test_registering_class(self):
        locator = ObjectLocator()
        container_class = self.get_container()
        container = container_class()
        container._locator = locator
        container.register_callable(TEST_CLASS_1_NAME, TestClass1)

        ret1 = locator.is_key_registered(TEST_CLASS_1_NAME)
        assert ret1 is True

        ret2 = container.get(TEST_CLASS_1_NAME)
        ret3 = container.get(TEST_CLASS_1_NAME)

        assert isinstance(ret2, TestClass1)
        assert id(ret2) != id(ret3)

    def test_registering_function_as_object(self):
        locator = ObjectLocator()
        container_class = self.get_container()
        container = container_class()
        container._locator = locator
        container.register_object(TEST_FUNC_1_NAME, TestFunc1)

        ret1 = container.get(TEST_FUNC_1_NAME)
        assert ret1 is not None
        assert isinstance(ret1, type(TestFunc1))

    def test_if_container_retrieves_classes_with_dependencies(self):
        class ClassWithDeps(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b

        container_class = self.get_container()
        container = container_class()

        container.register_object('a', 'simple_string')
        container.register_callable('b', TestClass1)
        container.register_callable_with_deps('ClassWithDeps', ClassWithDeps, lifetime=InstanceLifetime.NewInstancePerCall)

        class_with_deps = container.get('ClassWithDeps')

        assert isinstance(class_with_deps, ClassWithDeps)
        assert class_with_deps.a == 'simple_string'
        assert isinstance(class_with_deps.b, TestClass1)


class Test_NamespaceContainer(Test_SimpleContainer):
    @classmethod
    def get_container(cls):
        return NamespacedContainer

    def test_1(self):
        container_class = self.get_container()
        container = container_class('componenet')
        container.register_callable(TEST_CLASS_2_NAME, TestClass2)

        sub_container = SimpleContainer(name='sub')
        sub_container.register_callable(TEST_CLASS_1_NAME, TestClass1)

        container.add_sub_container(sub_container)

        ret1 = container.get(TEST_CLASS_2_NAME)
        assert isinstance(ret1, TestClass2)

        ret2 = container.get('%s__%s' % ('sub', TEST_CLASS_1_NAME))
        assert isinstance(ret2, TestClass1)

    def test_if_container_retrieves_classes_with_dependencies_from_sub_containers(self):
        class ClassWithDeps(object):
            def __init__(self, sub__a, b):
                self.a = sub__a
                self.b = b

        container_class = self.get_container()
        container = container_class('root')
        sub_container = container_class('sub')

        sub_container.register_object('a', 'simple_string')
        container.register_callable('b', TestClass1)
        container.register_callable_with_deps('ClassWithDeps', ClassWithDeps, lifetime=InstanceLifetime.NewInstancePerCall)

        container.add_sub_container(sub_container)

        class_with_deps = container.get('ClassWithDeps')

        assert isinstance(class_with_deps, ClassWithDeps)
        assert class_with_deps.a == 'simple_string'
        assert isinstance(class_with_deps.b, TestClass1)
