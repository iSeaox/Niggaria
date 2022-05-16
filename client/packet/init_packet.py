import network.packet.packet as packet


class InitPacket(packet.Packet):

    def __init__(self, user = None, password = None):
        super().__init__()
        self.side = packet.PACKET_CLIENT
        self.type = "init_packet"

        self.user = user
        self.password = password
