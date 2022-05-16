import network.packet.packet as packet


class ChunkTransfertPacket(packet.Packet):

    def __init__(self, chunk=None, id=None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "chunk_transfert_packet"
        self.id = id

        self.chunk = chunk
