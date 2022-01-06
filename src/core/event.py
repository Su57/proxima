from typing import List, Callable, Union, Final
from abc import ABC, abstractmethod

from blinker import NamedSignal
from flask.signals import Namespace


class EventListener(ABC):

    @abstractmethod
    def __call__(self, sender, *args, **kwargs): ...


class Event:

    def __init__(self, observers: List[Union[EventListener, Callable[['Event'], None]]]):
        self._signal: Final[NamedSignal] = Namespace().signal(name=self.__class__.__name__)
        self._observers: List[Union[EventListener, Callable[['Event'], None]]] = observers

        for observer in self._observers:
            self._signal.connect(receiver=observer, sender=self)

    def register_observer(self, observer: EventListener):
        if observer not in self._observers:
            self._observers.append(observer)
            self._signal.connect(receiver=observer, sender=self)

    def remove_observer(self, observer: EventListener):
        if observer in self._observers:
            self._observers.remove(observer)
            self._signal.disconnect(receiver=observer, sender=self)

    def notify(self, *args, **kwargs):
        self._signal.send(self, *args, **kwargs)


__all__ = ["EventListener", "Event"]
