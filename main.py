from src import utils, database
from src.constants import TWITCH_DATABASE_PATH
from src.twitch import Twitch
from src.utils import InvalidCommandError

COMMAND_DESCRIPTION = """
 - `subscribe <username> to <channel>`
 - `publish video on <channel>`
 - `exit`
 """


def run_twitch_simulation() -> None:
    print(COMMAND_DESCRIPTION)
    twitch = Twitch(database.new_persistent_database(TWITCH_DATABASE_PATH))
    while True:
        try:
            command = input("Enter command: ")
            if command == "exit":
                twitch.exit()
                break
            elif command.startswith("subscribe"):
                username, channel = utils.parse_subscription_command(command)
                twitch.subscribe(username, channel)
            elif command.startswith("publish"):
                channel = utils.parse_publish_command(command)
                twitch.publish(channel)
        except InvalidCommandError as e:
            print(e)


if __name__ == '__main__':
    run_twitch_simulation()
    print("Exiting...")
