import time

PACKET_CLIENT = "client"
PACKET_SERVER = "server"

class Packet:
    def __init__(self):
        self.side = None
        self.type = "AbstractPacket"
        self.timestamp = None

    def serialize(self) -> str:
        self.timestamp = time.time_ns()
        return str(self.__dict__).replace("'", '"')


    def deserialize(self, json_dict: dict):
        for key in json_dict.keys():
            self.__dict__[key] = json_dict[key]
        return self
