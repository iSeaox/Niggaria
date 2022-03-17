import threading

class NetListener(threading.Thread):
    def __init__(self, handler):
        threading.Thread.__init__(self, name="net-listener", daemon=True)
        self.__handler = handler
        self.__listen = True

    def run(self):
        self.__handler.logger.log("Listening...")
        while(self.__listen):
            received_packet = self.__handler.get_socket().recvfrom(self.__handler.get_net_buffer_size())
            self.__handler.buffer.append(received_packet)
        self.__handler.logger.log("End of listening", object="stop")

    def stop(self):
        self.__listen = False
