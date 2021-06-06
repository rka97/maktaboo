"""maktaboo-cli-client - a simple and straightforward CLI client for maktaboo."""
import socket
import configparser
import enum
import click
import questionary


def send_message(message, ip, port):
    """Send a UDP message to the specified ip-port pair."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (ip, port))


class ActionType(enum.Enum):
    """Types of actions supported by the program."""

    ADD_BIB = "Add bibliography file to database"
    FIX_PDF_METADATA = "Fix PDF metadata"
    QUIT = "Quit"

    @classmethod
    def get_values(cls):
        values = [action.value for action in cls]
        return values


def listen_to_user_input(server_ip, server_port):
    """Continuously listen to user input and sends messages to the server."""
    click.echo("Welcome to the Maktaboo CLI client.")

    action_prompts = ActionType.get_values()
    while True:
        action = ActionType(
            questionary.select("Choose an action:", choices=action_prompts).ask()
        )
        if action == ActionType.QUIT:
            break


@click.command()
@click.option(
    "--config-file",
    default="maktaboo.conf",
    help="configuration file path",
    type=click.File("r"),
)
def main(config_file):
    config = configparser.ConfigParser()
    config.read_file(config_file)
    server_ip = config["server"]["ip"]
    server_port = int(config["server"]["port"])
    listen_to_user_input(server_ip, server_port)


if __name__ == "__main__":
    main()
