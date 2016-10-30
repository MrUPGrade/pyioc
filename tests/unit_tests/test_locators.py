# coding=utf-8

import pytest

from pyioc.locators import ObjectLocator, KeyToStringConverter
from tests.fakes import TEST_CLASS_1_NAME, TestClass1


class Test_ObjectLocator(object):
    def test_if_registered_object_is_resolved_by_key(self):
        localtor = ObjectLocator()
        test_object = TestClass1()

        localtor.register(TEST_CLASS_1_NAME, test_object)
        instance = localtor.locate(TEST_CLASS_1_NAME)

        assert instance is not None
        assert test_object is instance

    def test_if_resolving_unregistered_object_raises_exception(self):
        locator = ObjectLocator()

        with pytest.raises(KeyError):
            locator.locate(TEST_CLASS_1_NAME)

    def test_if_registering_duplicate_entry_raises_exception(self):
        locator = ObjectLocator()
        test_object = TestClass1()

        locator.register(TEST_CLASS_1_NAME, test_object)

        with pytest.raises(KeyError):
            locator.register(TEST_CLASS_1_NAME, test_object)

    def test_if_class_can_be_used_as_key(self):
        locator = ObjectLocator()
        test_object = TestClass1()

        locator.register(TestClass1, test_object)
        instance = locator.locate(TestClass1)

        assert instance is not None
        assert isinstance(instance, TestClass1)

    def test_if_is_registered_returns_true_for_registered_providers(self):
        locator = ObjectLocator()
        test_object = TestClass1()

        locator.register(TEST_CLASS_1_NAME, test_object)

        assert locator.is_key_registered(TEST_CLASS_1_NAME)
        assert not locator.is_key_registered(test_object)

    def test_if_get_or_default_returns_registered_object(self):
        locator = ObjectLocator()
        test_object = TestClass1()

        locator.register(TEST_CLASS_1_NAME, test_object)

        ret1 = locator.get_or_default(TEST_CLASS_1_NAME, 'default')

        assert isinstance(ret1, TestClass1)
        assert ret1 is test_object

    def test_if_get_or_default_returns_default_when_no_object_for_given_key(self):
        locator = ObjectLocator()

        ret1 = locator.get_or_default(TEST_CLASS_1_NAME, 'default')

        assert isinstance(ret1, str)
        assert ret1 == 'default'

    def test_if_locator_returns_keys_for_registered_objects(self):
        locator = ObjectLocator()
        locator.register('key', 'value')

        keys = locator.get_keys()

        assert 'key' in keys
        assert len(keys) == 1


class Test_KeyToStringConverter(object):
    def test_func_name(self):
        converter = KeyToStringConverter()

        def func_1():
            pass

        ret1 = converter.generate_key(func_1)
        assert ret1 == 'func_func_1'

    def test_class_name(self):
        converter = KeyToStringConverter()

        ret1 = converter.generate_key(TestClass1)
        assert ret1 == 'TestClass1'

    def test_object_name(self):
        converter = KeyToStringConverter()

        ret1 = converter.generate_key(TestClass1())
        assert ret1 == 'TestClass1'

    def test_object_name_with_alias_type(self):
        from tests.fakes import TestClass1 as tc1

        converter = KeyToStringConverter()

        ret1 = converter.generate_key(tc1())
        assert ret1 == 'TestClass1'
