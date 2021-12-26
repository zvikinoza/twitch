class InvalidCommandError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def parse_subscription_command(command: str) -> tuple[str, str]:
    starting_phrase = 'subscribe '
    if command[:len(starting_phrase)] != starting_phrase:
        raise InvalidCommandError('Invalid command')
    command = command[len(starting_phrase):]
    username, channel = command.split(' to ')
    if (
            channel[0] != '<' and
            channel[-1] != '>' or
            username[0] != '<' and
            username[-1] != '>'
    ):
        raise InvalidCommandError('Invalid command')
    username = username[1:-1]
    channel = channel[1:-1]
    if (
            not channel or
            not username or
            channel.find('>') != -1 or
            channel.find('<') != -1 or
            username.find('>') != -1 or
            username.find('<') != -1
    ):
        raise InvalidCommandError('Invalid command')
    return username, channel


def parse_publish_command(command: str) -> str:
    starting_phrase = 'publish video on '
    if command[:len(starting_phrase)] != starting_phrase:
        raise InvalidCommandError('Invalid command')
    channel = command[len(starting_phrase):]
    if channel[0] != '<' and channel[-1] != '>':
        raise InvalidCommandError('Invalid command')
    channel = channel[1:-1]
    if not channel or channel.find('>') != -1 or channel.find('<') != -1:
        raise InvalidCommandError('Invalid command')
    return channel
