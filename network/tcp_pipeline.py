import threading
import socket


class TCPListener(threading.Thread):
    def __init__(self, logger, connection, pipeline, id, debug=False):
        threading.Thread.__init__(self, name="tcp-listener-"+str(id), daemon=True)
        self.logger = logger
        self.connection = connection
        self.pipeline = pipeline
        self.__debug = debug

    def run(self):
        while True:
            try:
                data = self.connection.recv(4096)
                self.pipeline.queue.put((self.connection.getpeername(), data))
                if self.__debug:
                    self.logger.log(str((self.connection.getpeername(), data)), subject="debug")
            except ConnectionResetError:
                break

            if not data:
                break

        if self.__debug:
            self.logger.log("connection lost with " + str(self.connection.getpeername()), subject="debug")
        self.pipeline.connection_lost_function(self.connection.getpeername())
        self.pipeline.end(self)
        self.connection.close()


class TCPPipeLineServer(threading.Thread):
    def __init__(self, logger, queue, connection_lost_function, debug=False, port=20002):
        threading.Thread.__init__(self, name="tcp-pipeline", daemon=True)
        self.logger = logger

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.__debug = debug
        self.connection_lost_function = connection_lost_function
        self.thread_id = 0

        self.listener_pool = {}
        self.queue = queue

        self.is_listening = True

    def run(self):
        if self.__debug:
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
