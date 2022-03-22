
PACKET_CLIENT = "client"
PACKET_SERVER = "server"

class Packet:
    def __init__(self):
        self.side = None
        self.type = "AbstractPacket"

    def serialize(self):
        raise NotImplementedError("serialize() method has to be overrid on child class")

    def deserialize(self):
        raise NotImplementedError("deserialize() method has to be overrid on child class")
