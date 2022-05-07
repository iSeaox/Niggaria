import network.packet.packet as packet

#Start UDP Communication Packet
class SUDPCPacket(packet.Packet):
    def __init__(self, uuid):
        super().__init__()
        self.side = packet.PACKET_CLIENT
        self.type = "sudpc_packet"

        self.uuid = uuid
