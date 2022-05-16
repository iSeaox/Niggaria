import threading
import socket

import network.net_preprocessor as net_preprocessor


class TCPListener(threading.Thread):
    def __init__(self, logger, connection, pipeline, id, debug=False):
        threading.Thread.__init__(self, name="tcp-listener-"+str(id), daemon=True)
        self.logger = logger
        self.connection = connection
        self.pipeline = pipeline
        self.__debug = debug

    def run(self):
        temp_packet = b''
        # i = 0
        while True:
            try:
                data = self.connection.recv(4096)
                # print(i)
                temp_packet += data
                # i += 1

                if len(data) != 4096 or data[len(data) - 1] == 125:  # 125 est le code b'}'
                    if self.__debug:
                        self.logger.log(str((self.connection.getpeername(), temp_packet)), subject="debug")

                    splitted_packet = net_preprocessor.preprocess_packet((self.connection.getpeername(), temp_packet))
                    for pck in splitted_packet:
                        self.pipeline.queue.put(pck)
                    temp_packet = b''

            except ConnectionResetError:
                break

            if not data:
                break

        self.logger.log("connection lost with " + str(self.connection.getpeername()), subject="debug")
        self.pipeline.connection_lost_function(self.connection.getpeername())
        self.pipeline.end(self)
        self.connection.close()


class TCPPipeLineServer(threading.Thread):
    def __init__(self, logger, queue, connection_lost_function, debug=False, port=20002):
        threading.Thread.__init__(self, name="tcp-pipeline", daemon=True)
        self.logger = logger

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        self.__debug = debug
        self.connection_lost_function = connection_lost_function
        self.thread_id = 0

        self.listener_pool = {}
        self.queue = queue

        self.is_listening = True

    def run(self):
        self.logger.log("activation of the TCP pipeline: waiting for connection", subject="debug")
        self.socket.listen()

        while self.is_listening:
            (con, addr) = self.socket.accept()

            if self.__debug:
                self.logger.log("starting a new TCP listener", subject="debug")
            listener = TCPListener(self.logger, con, self, self.thread_id, debug=self.__debug)
            self.thread_id += 1
            self.listener_pool[addr] = listener
            listener.start()

        self.socket.close()

    def send_packet(self, server_player, packet):
        if server_player.tcp_access in self.listener_pool.keys():
            self.listener_pool[server_player.tcp_access].connection.sendall(packet)

    def end(self, tcp_listener):
        del self.listener_pool[tcp_listener.connection.getpeername()]


class TCPPipelineClient(threading.Thread):
    def __init__(self, logger, queue, server_access, client, debug=False):
        threading.Thread.__init__(self, name="tcp-pipeline", daemon=True)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logger
        self.server_access = server_access
        self.client = client
        self.__debug = debug
        self.__listener = None

        self.queue = queue

        self.ready_event = threading.Event()

    def run(self):
        if self.__debug:
            self.logger.log("launching a TCP pipeline", subject="debug")
        self.socket.connect(self.server_access)
        if self.__debug:
            self.logger.log("TCP pipeline: connection", subject="debug")
        self.__listener = TCPListener(self.logger, self.socket, self, 0, debug=self.__debug)
        self.__listener.start()
        self.ready_event.set()

        self.__listener.join()

    def send_packet(self, packet):
        self.__listener.connection.sendall(packet)

    def end(self, tcp_listener):
        if self.__debug:
            self.logger.log("connection with server closed", subject="debug")
