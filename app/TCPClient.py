import socket
from config import Config

class DataSender:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        self.sock.connect((Config.SCOREBOARD_HOST, Config.SCOREBOARD_PORT))

    def send(self, msg):

        try:
            self.sock.send(msg)
        except:
            return ('send_error')

