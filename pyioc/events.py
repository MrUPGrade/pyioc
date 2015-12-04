import six
import abc
from collections import defaultdict


class ListenerAlreadyRegistered(Exception):
    pass


@six.add_metaclass(abc.ABCMeta)
class Event(object):
    pass


@six.add_metaclass(abc.ABCMeta)
class Event1(Event):
    pass


@six.add_metaclass(abc.ABCMeta)
class Listener(object):
    @abc.abstractmethod
    def notify(self, event):
        pass


class EventAggregator(object):
    def __init__(self):
        self._listeners = defaultdict(list)

    def subscribe(self, event_type, listener):
        event_listeners = self._listeners[event_type]
        if listener in event_listeners:
            raise ListenerAlreadyRegistered()

        event_listeners.append(listener)

    def unsubscribe(self, event_type, listener):
        listeners = self._listeners[event_type]
        listeners.remove(listener)

    def publish(self, event):
        event_listeners = self._listeners[event.__class__]
        for listener in event_listeners:
            listener.notify(event)

    def is_listener_subscribed(self, event_type, listener):
        if not event_type in self._listeners:
            return False

        event_listeners = self._listeners[event_type]
        if listener in event_listeners:
            return True

        return False
