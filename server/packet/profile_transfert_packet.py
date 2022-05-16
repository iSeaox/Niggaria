import network.packet.packet as packet


class ProfileTransfertPacket(packet.Packet):
    def __init__(self, profile=None, message=None, authorized=None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "profile_transfert_packet"

        self.profile = profile
        self.message = message
        self.authorized = authorized
