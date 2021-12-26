import sqlite3

from src import database, constants
from src.database import InMemoryDatabase
from src.twitch import Twitch

MockDatabase = InMemoryDatabase


def test_twitch_subscribe() -> None:
    db = MockDatabase()
    twitch = Twitch(db)
    twitch.subscribe('Alice', 'BackToTheFuture')
    assert db.get('BackToTheFuture') == {'Alice'}


def test_twitch_multi_user_subscribe() -> None:
    db = MockDatabase()
    twitch = Twitch(db)
    for username in constants.TESTING_USERNAMES:
        twitch.subscribe(username, 'BackToTheFuture')
    assert db.get('BackToTheFuture') == constants.TESTING_USERNAMES


def test_twitch_multi_channel_subscribe() -> None:
    db = MockDatabase()
    twitch = Twitch(db)
    for username in constants.TESTING_USERNAMES:
        for channel in constants.TESTING_CHANNELS:
            twitch.subscribe(username, channel)
    for channel in constants.TESTING_CHANNELS:
        assert db.get(channel) == constants.TESTING_USERNAMES


def test_twitch_temporary_database() -> None:
    db = database.new_temporary_database()
    twitch = Twitch(db)
    for username in constants.TESTING_USERNAMES:
        for channel in constants.TESTING_CHANNELS:
            twitch.subscribe(username, channel)
    for channel in constants.TESTING_CHANNELS:
        assert db.get(channel) == constants.TESTING_USERNAMES
    db.close()


def test_twitch_persistent_database() -> None:
    db = database.new_persistent_database("test_twitch.db")
    twitch = Twitch(db)
    for username in constants.TESTING_USERNAMES:
        for channel in constants.TESTING_CHANNELS:
            twitch.subscribe(username, channel)
    db.close()
    con = sqlite3.connect("test_twitch.db")
    cur = con.cursor()
    for channel in constants.TESTING_CHANNELS:
        select_command = "select subscriber from Twitch where channel = ?"
        subscribers = cur.execute(select_command, (channel,))
        assert set(subscriber[0] for subscriber in subscribers) == constants.TESTING_USERNAMES
    cur.execute("drop table Twitch")
    cur.close()
