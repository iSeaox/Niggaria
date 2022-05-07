def preprocess_packet_queue(queue):
    packets = []

    temp_packet = ""
    while not(queue.empty()):
        data = queue.get()
        packets.append(data)

    return packets
