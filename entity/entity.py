

class Entity:
    def __init__(self):
        self.type = "abstract_entity"

        self.x = 0
        self.y = 0

        self.predicted_x = 0
        self.predicted_y = 0

    def serialize(self):
        return self.__dict__

    def deserialize(self, json_dict: dict):
        for key in json_dict.keys():
            self.__dict__[key] = json_dict[key]
        return self
