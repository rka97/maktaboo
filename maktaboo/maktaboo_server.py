"""maktaboo-server - server for maktaboo, the simple bibliography manager."""
import socket
import configparser
import maktaboo_util


class MaktabooServer:
    def __init__(self, listen_ip, listen_port, listen_buffer_size):
        """Initialize the MaktabooServer object with the given IP-port pair.
        Note that this constructor does /not/ actually start listening.
        For that, you need to call the main_loop method.
        """
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.listen_buffer_size = listen_buffer_size
        # Create the server logger
        self.logger = maktaboo_util.get_basic_logger("MaktabooServer")

    def listen_to_messages(self):
        """Continuously listen to messages."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.listen_ip, self.listen_port))
        self.logger.info(
            "Starting the Maktaboo server on %s:%d.."
            % (self.listen_ip, self.listen_port)
        )
        while True:
            data, address = sock.recvfrom(self.listen_buffer_size)
            print("Received message: {}".format(data))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("maktaboo.conf")
    server_ip = config["server"]["ip"]
    server_port = int(config["server"]["port"])
    server_buffer_size = int(config["server"]["buffer size"])
    maktaboo_server = MaktabooServer(
        listen_ip=server_ip,
        listen_port=server_port,
        listen_buffer_size=server_buffer_size,
    )
    maktaboo_server.listen_to_messages()
