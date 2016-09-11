# coding=utf-8
from __future__ import absolute_import

import pytest

from pyioc.providers import validate_if_callable_without_args, SignatureError, ObjectProvider, NewInstancesProvider, \
    LazySingleInstanceProvider, LazySingleInstanceWithDepsProvider, NewInstancesWithDepsProvider, \
    EagerSingleInstanceProvider, EagerSingleInstanceWithDepsProvider
from tests.fakes import TestClass1, TEST_CLASS_1_INSTANCE


class Test_validate_if_callable_without_args(object):
    def test_if_raises_error_on_non_collable(self):
        with pytest.raises(TypeError):
            validate_if_callable_without_args(1)

    def test_if_raises_error_on_non_empty_args_list_on_function(self):
        def fake_func(a):
            return a

        with pytest.raises(TypeError):
            validate_if_callable_without_args(fake_func)

    def test_if_raises_error_on_non_empty_args_list_on_lambda(self):
        with pytest.raises(TypeError):
            validate_if_callable_without_args(lambda x: x)

    def test_if_not_raises_error_on_empty_arg_list_on_function(self):
        def fake_func():
            pass

        validate_if_callable_without_args(fake_func)

    def test_if_not_raises_error_on_empty_arg_list_on_lambda(self):
        validate_if_callable_without_args(lambda: 0)

    def test_if_raises_error_on_not_empty_arg_list_on_method(self):
        class FakeClass(object):
            def method_with_args(self, a):
                pass

        with pytest.raises(SignatureError):
            validate_if_callable_without_args(FakeClass.method_with_args)

    def test_if_not_rases_error_on_method_without_args(self):
        class FakeClass(object):
            def method_without_args(self):
                pass

        validate_if_callable_without_args(FakeClass.method_without_args)

    def test_if_not_rases_error_on_class_with_constructor(self):
        class FakeClass(object):
            def __init__(self):
                pass

        validate_if_callable_without_args(FakeClass)

    def test_if_not_rases_error_on_class_without_constructor(self):
        class FakeClass(object):
            pass

        validate_if_callable_without_args(FakeClass)

    def test_if_rases_error_on_class_with_constructor_with_args(self):
        class FakeClass(object):
            def __init__(self, a):
                pass

        with pytest.raises(SignatureError):
            validate_if_callable_without_args(FakeClass)


class Test_ObjectProvider(object):
    def test_if_single_instance_provider_returns_instance(self):
        provider = ObjectProvider(TEST_CLASS_1_INSTANCE)
        ret1 = provider.get()
        ret2 = provider.get()

        assert isinstance(ret1, TestClass1)
        assert isinstance(ret2, TestClass1)
        assert ret1 is ret2


class Test_NewInstancesProvider(object):
    def test_if_provider_returns_instance(self):
        provider = NewInstancesProvider(TestClass1)
        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_provider_returns_new_instances_each_time(self):
        provider = NewInstancesProvider(TestClass1)
        ret1 = provider.get()
        ret2 = provider.get()

        assert isinstance(ret1, TestClass1)
        assert isinstance(ret2, TestClass1)
        assert ret1 is not ret2

    def test_if_provider_raise_error_when_callable_requires_arguments(self):
        def func1(a):
            return a

        with pytest.raises(TypeError):
            NewInstancesProvider(func1)

    def test_if_provider_raise_error_when_initialized_with_not_callable(self):
        with pytest.raises(TypeError):
            NewInstancesProvider(1)


class Test_LazySingletonProvider(object):
    def test_if_object_provider_returns_instance(self):
        provider = LazySingleInstanceProvider(TestClass1)
        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_object_provider_always_return_same_instance(self):
        provider = LazySingleInstanceProvider(TestClass1)
        ret1 = provider.get()
        ret2 = provider.get()

        assert isinstance(ret1, TestClass1)
        assert isinstance(ret2, TestClass1)
        assert ret1 is ret2

    def test_if_provider_raise_error_when_callable_requires_arguments(self):
        def func1(a):
            return a

        with pytest.raises(TypeError):
            LazySingleInstanceProvider(func1)

    def test_if_provider_raise_error_when_initialized_with_not_callable(self):
        with pytest.raises(TypeError):
            LazySingleInstanceProvider(1)


class Test_EagerSingleInstanceProvider(object):
    def test_if_single_instance_provider_returns_instance(self):
        provider = EagerSingleInstanceProvider(TestClass1)
        ret1 = provider.get()
        ret2 = provider.get()

        assert isinstance(ret1, TestClass1)
        assert isinstance(ret2, TestClass1)
        assert ret1 is ret2

    def test_if_provider_raise_error_when_callable_requires_arguments(self):
        def func1(a):
            return a

        with pytest.raises(TypeError):
            EagerSingleInstanceProvider(func1)

    def test_if_provider_raise_error_when_initialized_with_not_callable(self):
        with pytest.raises(TypeError):
            EagerSingleInstanceProvider(1)


class Test_NewInstancesWithDepsProvider(object):
    def test_if_returns_new_instance_of_a_class(self, mock_locator):
        provider = NewInstancesWithDepsProvider(TestClass1, mock_locator)

        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_returns_different_instance_of_a_class(self, mock_locator):
        provider = NewInstancesWithDepsProvider(TestClass1, mock_locator)

        ret1 = provider.get()
        ret2 = provider.get()

        assert isinstance(ret1, TestClass1)
        assert isinstance(ret2, TestClass1)
        assert ret1 is not ret2

    def test_if_provider_injects_registered_init_depts(self, mock_locator):
        class ClassWIthDeps(object):
            def __init__(self, testclass1):
                self.testclass1 = testclass1

        provider = NewInstancesWithDepsProvider(ClassWIthDeps, mock_locator)

        ret1 = provider.get()

        assert isinstance(ret1, ClassWIthDeps)
        assert isinstance(ret1.testclass1, TestClass1)

    def test_if_provider_inject_registered_depts_to_function(self, mock_locator):
        def func_with_deps(testclass1):
            return testclass1

        provider = NewInstancesWithDepsProvider(func_with_deps, mock_locator)

        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_provider_raise_error_when_initialized_with_not_callable(self, mock_locator):
        with pytest.raises(TypeError):
            NewInstancesWithDepsProvider(1, mock_locator)


class Test_LazySingleInstanceWithDepsProvider(object):
    class ClassWIthDeps(object):
        def __init__(self, testclass1):
            self.testclass1 = testclass1

    def test_if_returns_instance_of_a_class(self, mock_locator):
        provider = LazySingleInstanceWithDepsProvider(TestClass1, mock_locator)

        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_returns_different_instance_of_a_class(self, mock_locator):
        provider = LazySingleInstanceWithDepsProvider(TestClass1, mock_locator)

        ret1 = provider.get()
        ret2 = provider.get()

        assert isinstance(ret1, TestClass1)
        assert isinstance(ret2, TestClass1)
        assert ret1 is ret2

    def test_if_provider_inject_registered_depts_to_function(self, mock_locator):
        def func_with_deps(testclass1):
            return testclass1

        provider = LazySingleInstanceWithDepsProvider(func_with_deps, mock_locator)

        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_provider_raise_error_when_initialized_with_not_callable(self, mock_locator):
        with pytest.raises(TypeError):
            LazySingleInstanceWithDepsProvider(1, mock_locator)


class Test_EagerSingleInstanceWithDepsProvider(object):
    class ClassWIthDeps(object):
        def __init__(self, testclass1):
            self.testclass1 = testclass1

    def test_if_returns_instance_of_a_class(self, mock_locator):
        provider = EagerSingleInstanceWithDepsProvider(TestClass1, mock_locator)

        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_returns_different_instance_of_a_class(self, mock_locator):
        provider = EagerSingleInstanceWithDepsProvider(TestClass1, mock_locator)

        ret1 = provider.get()
        ret2 = provider.get()

        assert isinstance(ret1, TestClass1)
        assert isinstance(ret2, TestClass1)
        assert ret1 is ret2

    def test_if_provider_inject_registered_depts_to_function(self, mock_locator):
        def func_with_deps(testclass1):
            return testclass1

        provider = EagerSingleInstanceWithDepsProvider(func_with_deps, mock_locator)

        ret1 = provider.get()

        assert isinstance(ret1, TestClass1)

    def test_if_provider_raise_error_when_initialized_with_not_callable(self, mock_locator):
        with pytest.raises(TypeError):
            LazySingleInstanceWithDepsProvider(1, mock_locator)
