from abc import ABC


class Subscriber(ABC):
    def notify(self) -> None:
        raise NotImplementedError


class TwitchUser(Subscriber):
    def __init__(self, name: str) -> None:
        self.__name = name

    def notify(self) -> None:
        print(f"\t{self.__name}")

