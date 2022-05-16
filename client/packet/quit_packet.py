import network.packet.packet as packet


class QuitPacket(packet.Packet):
    def __init__(self, profile):
        super().__init__()
        self.side = packet.PACKET_CLIENT
        self.type = "quit_packet"

        self.profile = profile
