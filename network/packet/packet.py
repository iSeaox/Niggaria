import time

PACKET_CLIENT = "client"
PACKET_SERVER = "server"

AUTHORIZED_TYPE = (int, str, bool, list, dict, float)

class Packet:
    def __init__(self):
        self.side = None
        self.type = "AbstractPacket"
        self.timestamp = None

    def serialize(self) -> str:
        self.timestamp = time.time_ns()

        json_dict = {}
        for key in self.__dict__.keys():
            if(type(self.__dict__[key]) in AUTHORIZED_TYPE or self.__dict__[key] == None):
                json_dict[key] = self.__dict__[key]
            else:
                json_dict[key] = self.__dict__[key].serialize()

        return str(json_dict).replace("'", '"').replace("True", "true").replace("False", "false").replace("None", "null")


    def deserialize(self, json_dict: dict):
        for key in json_dict.keys():
            self.__dict__[key] = json_dict[key]
        return self
