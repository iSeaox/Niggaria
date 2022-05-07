def gen_packet_list(queue):
    packets = []

    while not(queue.empty()):
        data = queue.get()
        packets.append(data)

    return packets

def preprocess_packet(packet):
    packets = []

    data = packet[1].decode()
    out = []
    openned = 0
    f_id = 0

    for i in range(len(data)):
        if(data[i] == "{"):
            openned +=1
            if(openned == 1):
                f_id = i

        elif(data[i] == "}"):
            openned -= 1
            if(openned == 0):
                out.append(data[f_id:i+1])

    for pck in out:
        packets.append((packet[0], pck))

    return packets
