from src.twitch import Twitch

COMMAND_DESCRIPTION = """
 - `subscribe <username> to <channel>`
 - `publish video on <channel>`
 - `exit`
 """


def run_twitch_simulation() -> None:
    print(COMMAND_DESCRIPTION)
    twitch = Twitch()
    while True:
        command = input("Enter command: ")
        if command == "exit":
            twitch.exit()
        elif command.startswith("subscribe"):
            command_args = command.split()
            if len(command_args) != 4:
                print("Invalid command")
                continue
            username = command_args[1].lstrip("<").rstrip(">")
            channel = command_args[3].lstrip("<").rstrip(">")
            twitch.subscribe(username, channel)
            print("Subscribed user {} to channel {}".format(username, channel))
        elif command.startswith("publish"):
            command_args = command.split()
            if len(command_args) != 4:
                print("Invalid command")
                continue
            channel = command_args[3].lstrip("<").rstrip(">")
            twitch.publish(channel)
            print("Published video on channel {}".format(channel))


if '__name__' == '__main__':
    run_twitch_simulation()
    print("Exiting...")
