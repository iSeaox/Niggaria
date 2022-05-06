

def preprocess_packet_queue(queue):
    packets = []

    temp_packet = ""
    while(not(self.tcp_queue.empty())):
        data = self.tcp_queue.get().decode()
