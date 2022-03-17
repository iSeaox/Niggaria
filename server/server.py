import socket
import time

import network.net_listener as net_listener

class Server:
    def __init__(self, ip_addr, port, logger):
        self.__ip_addr = ip_addr
        self.__port = port

        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__socket.bind((self.__ip_addr, self.__port))

        self.__net_buffer_size = 1024
        self.buffer = []
        self.logger = logger
        self.net_listener = net_listener.NetListener(self)
        self.net_listener.start()

    def start(self):
        while(1):
            time.sleep(1)
            print(self.buffer)

    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
