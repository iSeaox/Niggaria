import network.packet.packet as packet

class ActionTransfertPacket(packet.Packet):
    def __init__(self, action = None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "action_transfert_packet"

        self.action = action
