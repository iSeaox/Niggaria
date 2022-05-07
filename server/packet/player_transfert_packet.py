import network.packet.packet as packet


class PlayerTransfertPacket(packet.Packet):
    def __init__(self, player=None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "player_transfert_packet"

        self.player = player
