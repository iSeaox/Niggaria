import threading


class UDPListener(threading.Thread):
    def __init__(self, logger, socket, target_queue):
        threading.Thread.__init__(self, name="udp-listener", daemon=True)
        self.logger = logger
        self.target_queue = target_queue
        self.socket = socket

        self.__listen = True
        self.is_start = False

    def run(self):
        self.is_start = True
        self.logger.log("activation of the UDP listener: waiting for DGRAM")
        while self.__listen:
            received_packet = self.socket.recvfrom(4096)
            self.target_queue.put(received_packet)
        self.logger.log("End of listening", object="stop")

    def stop(self):
        self.__listen = False
