import threading
import socket

SOCKET_PORT = 20002

class TCPPipeLine(threading.Thread):

    def __init__(self, logger):
        Thead.__init__(self, name="tcp-pipeline", daemon = True)
        self.logger = logger

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind('localhost', SOCKET_PORT)

        self.waiting_transfert = []
        self.is_listenning = True

    def run(self):

        while(self.is_listenning):
            self.socket.listen(len(self.waiting_transfert))
            # Créer un nouveau objet Thread qui exécute le traitement 
