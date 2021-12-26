from src import database
from src.constants import TWITCH_DATABASE


class Twitch:
    def __init__(self) -> None:
        self.__db = database.connect(TWITCH_DATABASE)

    def subscribe(self, username: str, channel: str) -> None:
        user_notifier = self.__db.get_user(username)
        channel_event_manager = self.__db.get_channel(channel)
        channel_event_manager.subscribe(user_notifier)

    def publish(self, channel: str) -> None:
        channel_event_manager = self.__db.get_channel(channel)
        channel_event_manager.publish()

    def exit(self) -> None:
        self.__db.close(TWITCH_DATABASE)
