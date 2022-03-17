import socket
import time

import network.net_listener as net_listener

class Client:
    def __init__(self, server_acces, logger):
        self.server_acces = server_acces
        self.logger = logger
        self.__net_buffer_size = 1024

        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.net_listener = net_listener.NetListener(self)
        self.net_listener.start()

        self.__socket.sendto(str.encode("Ceci est un test"), self.server_acces)
        self.__socket.sendto(str.encode("Ceci est un test1"), self.server_acces)
        time.sleep(2)
        self.__socket.sendto(str.encode("Ceci est un test2"), self.server_acces)
        self.__socket.sendto(str.encode("Ceci est un test3"), self.server_acces)

    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
