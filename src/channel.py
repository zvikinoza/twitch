from abc import ABC

from src.user import Subscriber


class Channel(ABC):
    def subscribe(self, subscriber: Subscriber) -> None:
        raise NotImplementedError

    def publish(self) -> None:
        raise NotImplementedError


class TwitchChannel(Channel):
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__subscribers: list[Subscriber] = []

    def subscribe(self, subscriber: Subscriber) -> None:
        self.__subscribers.append(subscriber)

    def publish(self) -> None:
        print(f"Notifying subscribers of {self.__name}:")
        for subscriber in self.__subscribers:
            subscriber.notify()
