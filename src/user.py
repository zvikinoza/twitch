from abc import ABC


class EventListener(ABC):
    def notify(self) -> None:
        pass


class SubscribeListener:
    def notify(self, channel_name: str, username: str) -> None:
        pass


class PublishListener(EventListener):
    def notify(self) -> None:
        pass

    def get_name(self) -> str:
        pass


class UserNotifier(PublishListener):
    def __init__(self, username: str) -> None:
        self.__username = username

    def notify(self) -> None:
        print(self.__username)

    @property
    def get_username(self) -> str:
        return self.__username
