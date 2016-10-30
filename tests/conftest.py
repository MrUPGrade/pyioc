# coding=utf-8

import pytest
from mock import Mock

from tests.fakes import TEST_CLASS_3_INSTANCE, TEST_CLASS_1_INSTANCE, TEST_CLASS_1_NAME, TEST_CLASS_3_NAME


@pytest.fixture
def mock_locator():
    """
    A mock for object locator  with testclass1 and testclass2 registered by name.

    :return: mocked locator with testclass1 and testclass2 registered
    """

    def side_efect(name):
        type_dict = {
            TEST_CLASS_1_NAME: TEST_CLASS_1_INSTANCE,
            TEST_CLASS_3_NAME: TEST_CLASS_3_INSTANCE
        }
        value = type_dict[name]

        return value

    mock = Mock()
    mock.get = Mock(side_effect=side_efect)
    return mock


@pytest.fixture
def mock_container():
    """
    A mock for  container with testclass1 and testclass2 registered by name.

    :return: mocked locator with testclass1 and testclass2 registered
    """

    def side_efect(name, context=None):
        type_dict = {
            TEST_CLASS_1_NAME: TEST_CLASS_1_INSTANCE,
            TEST_CLASS_3_NAME: TEST_CLASS_3_INSTANCE
        }
        value = type_dict[name]

        return value

    mock = Mock()
    mock.resolve = Mock(side_effect=side_efect)
    return mock
