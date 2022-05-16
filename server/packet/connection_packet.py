import network.packet.packet as packet

JOIN_SERVER = 0
QUIT_SERVER = 1


class ConnectionPacket(packet.Packet):
    def __init__(self, player=None, connection_type=None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "connection_packet"

        self.player = player
        self.connection_type = connection_type
