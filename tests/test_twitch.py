
def test_twitch_subscribe() -> None:
    db = Database()
    twitch = Twitch(db)
    twitch.subscribe('Alice', 'BackToTheFuture')
    assert twitch.get_subscriptions('Alice') == ['BackToTheFuture']


def test_twitch_subscribe() -> None:
    db = Database()
    twitch = Twitch(db)
    twitch.subscribe('Alice', 'BackToTheFuture')
    assert twitch.get_subscriptions('Alice') == ['BackToTheFuture']

    