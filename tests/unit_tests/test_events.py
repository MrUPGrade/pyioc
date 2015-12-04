# coding=utf-8

from __future__ import absolute_import
import pytest
import mock
from pyioc.events import Event, EventAggregator, Listener, ListenerAlreadyRegistered


class FakeEvent(Event):
    pass


class FakeListener(Listener):
    def notify(self, event):
        pass


@pytest.fixture
def mock_listener():
    listener = mock.create_autospec(spec=FakeListener)
    return listener


class Test_EventAggregator(object):
    def test_if_listener_is_subscribed(self):
        aggregator = EventAggregator()
        listener = FakeListener()

        aggregator.subscribe(FakeEvent, listener)
        is_subscribed = aggregator.is_listener_subscribed(FakeEvent, listener)

        assert is_subscribed == True

    def test_if_is_not_subscribed_when_no_events_registered(self):
        aggregator = EventAggregator()
        listener = FakeListener()

        is_subscribed = aggregator.is_listener_subscribed(FakeEvent, listener)

        assert is_subscribed == False

    def test_if_is_not_subscribed_when_diferent_listener_registered_for_given_event(self):
        aggregator = EventAggregator()
        listener_registered = FakeListener()
        listener_unregistered = FakeListener()

        aggregator.subscribe(FakeEvent, listener_registered)
        is_subscribed = aggregator.is_listener_subscribed(FakeEvent, listener_unregistered)

        assert is_subscribed == False

    def test_if_listener_is_published_and_unpublished(self):
        aggregator = EventAggregator()
        listener = FakeListener()

        aggregator.subscribe(FakeEvent, listener)
        aggregator.unsubscribe(FakeEvent, listener)

    def test_if_listener_is_calle_when_event_is_published(self, mock_listener):
        aggregator = EventAggregator()
        event = FakeEvent()

        aggregator.subscribe(FakeEvent, mock_listener)
        aggregator.publish(event=event)

        mock_listener.notify.assert_called_once_with(event)

    def test_if_listener_is_not_called_when_unsubscribed(self, mock_listener):
        aggregator = EventAggregator()
        event = FakeEvent()

        aggregator.subscribe(FakeEvent, mock_listener)
        aggregator.unsubscribe(FakeEvent, mock_listener)
        aggregator.publish(event=event)

        mock_listener.notify.assert_not_called()

    def test_if_registering_duplicatet_listener_for_given_event_raises_error(self):
        aggregator = EventAggregator()

        aggregator.subscribe(FakeEvent, mock_listener)
        with pytest.raises(ListenerAlreadyRegistered):
            aggregator.subscribe(FakeEvent, mock_listener)

