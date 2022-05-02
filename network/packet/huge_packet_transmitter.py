import utils.uid_generator as uid_generator

import network.packet.partial_packet as partial_packet

PACKET_SIZE = 4096

class HugePacketTransmitter:

    def __init__(self, handler):
        self.handler = handler
        self.buffer = {}

    def transmit_packet(self, raw_packet, client_access):
        total = len(raw_packet) // PACKET_SIZE + 1
        uid = uid_generator.gen_uid(8)
        packet = []
        i = 0
        while(i < total):
            pt_packet = partial_packet.PartialPacket(raw_packet[i * PACKET_SIZE:(i + 1) * PACKET_SIZE], uid, i, total)
            packet.append(pt_packet)
            i += 1

        self.buffer[uid] = packet

        for ptp in packet:
            self.handler.get_socket().sendto(ptp.serialize(), client_access)

    def acknowledgment_packet(self, packet_ack):
        pass
