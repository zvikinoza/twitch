import json

from src.channel import Channel
from src.user import UserNotifier, SubscribeListener


class DataBase(SubscribeListener):
    def __init__(self, users={}, channels={}, channel_subscribers={}) -> None:
        self.__users = users
        self.__channels = channels
        self.__channel_subscribers = channel_subscribers

    def get_user(self, username: str) -> UserNotifier:
        if username not in self.__users:
            self.__users[username] = UserNotifier(username)
        return self.__users[username]

    def get_channel(self, channel: str) -> Channel:
        if channel not in self.__channels:
            self.__channels[channel] = Channel(channel, [self])
        return self.__channels[channel]

    def close(self, database) -> None:
        json.dump(self.__channel_subscribers, open(database, "w"))

    def notify(self, channel, username) -> None:
        self.__channel_subscribers[channel].add(username)


def connect(database) -> DataBase:
    users = {}
    channels = {}
    channel_subscribers = json.load(open(database, "r"))
    for channel,users in channel_subscribers.items():
        channels[channel] = Channel(channel)
        for user in users:
            users[user] = UserNotifier(user)
    return DataBase(users, channels, channel_subscribers)