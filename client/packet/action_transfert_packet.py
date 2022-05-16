import network.packet.packet as packet


class ActionTransfertPacket(packet.Packet):
    def __init__(self, action, profile):
        super().__init__()
        self.side = packet.PACKET_CLIENT
        self.type = "action_transfert_packet"

        self.action = action
        self.uuid = profile.uuid
