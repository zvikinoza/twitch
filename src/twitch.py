from abc import ABC

from src.channel import TwitchChannel, Channel
from src.database import TwitchDatabase
from src.user import TwitchUser, Subscriber


class StreamingPlatform(ABC):
    def subscribe(self, username: str, channel: str) -> None:
        raise NotImplementedError

    def publish(self, channel: str) -> None:
        raise NotImplementedError

    def exit(self) -> None:
        pass


class Twitch(StreamingPlatform):
    def __init__(self, db: TwitchDatabase) -> None:
        self.__db = db
        self.__channels: dict[str, Channel] = {}
        self.__subscribers: dict[str, Subscriber] = {}
        for username, channel in self.__db.items():
            self.__add_subscription(username, channel)

    def subscribe(self, username: str, channel: str) -> None:
        self.__db.put(channel, username)
        self.__add_subscription(username, channel)

    def publish(self, channel: str) -> None:
        if channel not in self.__channels:
            return
        self.__channels[channel].publish()

    def exit(self) -> None:
        self.__db.close()

    def __add_subscription(self, username: str, channel: str) -> None:
        if username not in self.__subscribers:
            self.__subscribers[username] = TwitchUser(username)
        if channel not in self.__channels:
            self.__channels[channel] = TwitchChannel(channel)
        self.__channels[channel].subscribe(self.__subscribers[username])
