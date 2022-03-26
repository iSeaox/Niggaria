
AUTHORIZED_TYPE = (int, str, bool, list, dict, float)

class Serializable:
    def serialize(self):
        json_dict = {}
        for key in self.__dict__.keys():
            if(type(self.__dict__[key]) in AUTHORIZED_TYPE or self.__dict__[key] == None):
                json_dict[key] = self.__dict__[key]
            else:
                json_dict[key] = self.__dict__[key].serialize()

        return json_dict

    def deserialize(self, json_dict: dict):
        for key in json_dict.keys():
            self.__dict__[key] = json_dict[key]
        return self
