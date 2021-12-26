import sqlite3
from abc import ABC
from collections import Iterator


class TwitchDatabase(ABC):
    def put(self, key: str, value: str) -> None:
        raise NotImplementedError

    def get(self, key: str) -> set[str]:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def items(self) -> Iterator[tuple[str, str]]:
        raise NotImplementedError


class InMemoryDatabase(TwitchDatabase):
    def __init__(self) -> None:
        self._db: dict[str, set[str]] = {}

    def put(self, channel: str, user: str) -> None:
        if channel not in self._db:
            self._db[channel] = set()
        self._db[channel].add(user)

    def get(self, channel: str) -> set[str]:
        return self._db[channel]

    def items(self) -> Iterator[tuple[str, str]]:
        for channel, users in self._db.items():
            for user in users:
                yield user, channel

    def close(self) -> None:
        pass


class PersistentDatabase(TwitchDatabase):
    def __init__(self, con: sqlite3.Connection) -> None:
        self._con = con
        self._cur = con.cursor()

    def put(self, channel: str, user: str) -> None:
        self._cur.execute('select * from Twitch where (subscriber=? AND channel=?)', (user, channel))
        if self._cur.fetchone() is None:
            insert_command = "insert into Twitch values (?, ?)"
            self._cur.execute(insert_command, (user, channel))
            self._con.commit()

    def get(self, channel: str) -> set[str]:
        select_command = "select subscriber from Twitch where channel = ?"
        subscribers = self._cur.execute(select_command, (channel,))
        return set(subscriber[0] for subscriber in subscribers)

    def close(self) -> None:
        self._cur.close()

    def items(self) -> Iterator[tuple[str, str]]:
        select_command = "select subscriber, channel from Twitch"
        return iter(self._cur.execute(select_command))


def new_temporary_database() -> TwitchDatabase:
    con = sqlite3.connect(":memory:")
    con.cursor().execute("create table if not exists Twitch (subscriber, channel)")
    return PersistentDatabase(con)


def new_persistent_database(database_file: str) -> TwitchDatabase:
    con = sqlite3.connect(database_file)
    con.cursor().execute("create table if not exists Twitch (subscriber, channel)")
    return PersistentDatabase(con)
