import time

import utils.serializable as serializable

PACKET_CLIENT = "client"
PACKET_SERVER = "server"


class Packet(serializable.Serializable):
    def __init__(self):
        self.side = None
        self.type = "AbstractPacket"
        self.timestamp = None

    def serialize(self) -> str:
        self.timestamp = time.time_ns()
        return str(super().serialize()).replace("'", '"').replace("True", "true").replace("False", "false").replace("None", "null")
