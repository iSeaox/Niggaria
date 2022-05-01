import network.packet.packet as packet

class PartialPacket(packet.Packet):

    def __init__(self, partial_data = None, uid_hpt = None, number = None, total = None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "partial_packet"

        self.partial_data = partial_data
        self.uid_hpt = uid_hpt
        self.number = number
        self.total = total
