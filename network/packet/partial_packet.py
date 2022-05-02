import network.packet.packet as packet
import struct

class PartialPacket(packet.Packet):

#
#  | Partial_Packet_ID (1 byte) | Total (4 byte) | Number (4 byte) | UID_HPT (8 byte) | Partial_Data ..... |
#
#
#
#
#
#
#
#

    def __init__(self, partial_data = None, uid_hpt = None, number = None, total = None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "partial_packet"

        self.partial_data = partial_data
        self.uid_hpt = uid_hpt
        self.number = number
        self.total = total

    def serialize(self):
        packet = b'\xFF'
        packet += struct.pack("II", self.total, self.number)
        packet += str.encode(self.uid_hpt)
        packet += str.encode(self.partial_data.replace("'", '"').replace("True", "true").replace("False", "false").replace("None", "null"))
        return packet
