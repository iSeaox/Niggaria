import network.packet.packet as packet

class HptAckPacket(packet.Packet):

    def __init__(self, uid_hpt = None, number = None, resend = None):
        super().__init__()
        self.side = packet.PACKET_CLIENT
        self.type = "hpt_ack_packet"

        self.uid_hpt = uid_hpt
        self.number = number
        self.resend = resend
