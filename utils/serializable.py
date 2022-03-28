
AUTHORIZED_TYPE = (int, str, bool, float)

class Serializable:
    def serialize(self):
        json_dict = {}
        for key in self.__dict__.keys():
            if(type(self.__dict__[key]) in AUTHORIZED_TYPE or self.__dict__[key] == None):
                json_dict[key] = self.__dict__[key]
            elif(type(self.__dict__[key]) == list):
                json_dict[key] = []
                for item in self.__dict__[key]:
                    json_dict[key].append(item.serialize())

            elif(type(self.__dict__[key]) == dict):
                json_dict[key] = {}
                for subdict_key in self.__dict__[key].keys():
                    json_dict[key][subdict_key] = self.__dict__[key][subdict_key].serialize()
            else:
                json_dict[key] = self.__dict__[key].serialize()

        return json_dict

    def deserialize(self, json_dict: dict):
        for key in json_dict.keys():
            self.__dict__[key] = json_dict[key]
        return self
