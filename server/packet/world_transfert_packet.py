import network.packet.packet as packet


class WorldTransfertPacket(packet.Packet):
    def __init__(self, world=None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "world_transfert_packet"

        self.world = world
