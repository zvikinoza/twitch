from abc import ABC

from src.user import EventListener, SubscribeListener, PublishListener


class EventManager(ABC):
    def subscribe(self, listener: EventListener) -> None:
        pass

    def publish(self) -> None:
        pass


class Channel(EventManager):
    def __init__(self, name: str, subscribe_listeners: list[SubscribeListener]) -> None:
        self.__name = name
        self.__subscribe_listeners = subscribe_listeners
        self.__publish_listeners = list()

    def subscribe(self, user: PublishListener) -> None:
        self.__publish_listeners.append(user)
        for listener in self.__subscribe_listeners:
            listener.notify(self.__name, user.get_name())

    def publish(self) -> None:
        print(f"Notifying subscribers of {self.__name}:")
        for listener in self.__publish_listeners:
            listener.notify()

    @property
    def get_name(self) -> str:
        return self.__name
