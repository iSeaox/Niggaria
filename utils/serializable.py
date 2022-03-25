class Serializable:
    def serialize(self):
        return self.__dict__

    def deserialize(self, json_dict: dict):
        for key in json_dict.keys():
            self.__dict__[key] = json_dict[key]
        return self
