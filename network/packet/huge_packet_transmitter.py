import utils.uid_generator as uid_generator

import network.packet.partial_packet as partial_packet

PACKET_SIZE = 4096

class HugePacketTransmitter:

    def __init__(self, handler):
        self.handler = handler
        self.buffer = {}

    def transmit_packet(self, raw_packet, client_access):
        total = len(raw_packet) // PACKET_SIZE
        uid = uid_generator.gen_uid(8)
        packet = []
        i = 0
        while(i < total - 1):
            pt_packet = partial_packet.PartialPacket(raw_packet[i:i + PACKET_SIZE], uid, i, total)
            packet.append(pt_packet)
            i += 1

        pt_packet = partial_packet.PartialPacket(raw_packet[i:len(raw_packet) - 1], uid, i, total)
        packet.append(pt_packet)

        self.buffer[uid] = packet
        print(packet, total)
        print(len(packet))

    def acknowledgment_packet(self, packet_code):
        pass
