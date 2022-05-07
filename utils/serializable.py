import sys

from pygame import Vector2

import utils.deserialization_error as des_error

AUTHORIZED_TYPE = (int, str, bool, float)


class Serializable:
    def serialize(self, omit=None):
        json_dict = {}
        for key in self.__dict__.keys():
            if key != omit:
                if type(self.__dict__[key]) in AUTHORIZED_TYPE or self.__dict__[key] is None:
                    json_dict[key] = self.__dict__[key]
                elif type(self.__dict__[key]) == list:
                    json_dict[key] = []
                    for item in self.__dict__[key]:
                        if type(item) in AUTHORIZED_TYPE:
                            json_dict[key].append(item)
                        else:
                            json_dict[key].append(item.serialize())

                elif type(self.__dict__[key]) == dict:
                    json_dict[key] = {}
                    for subdict_key in self.__dict__[key].keys():
                        json_dict[key][subdict_key] = self.__dict__[key][subdict_key].serialize()
                elif type(self.__dict__[key]) == Vector2:
                    json_dict[key] = {"x": self.__dict__[key].x, "y": self.__dict__[key].y, "extended_type": self.__dict__[key].__module__ + "." + self.__dict__[key].__class__.__name__}
                else:
                    json_dict[key] = self.__dict__[key].serialize()

        json_dict["extended_type"] = self.__module__ + "." + self.__class__.__name__

        return json_dict

    def to_bytes(self):
        pass


def deserialize(json_dict):
    if "extended_type" in json_dict.keys():
        extended_type = json_dict["extended_type"]
        mod_name = ""
        class_name = ""
        et_splitted = extended_type.split(".")
        for i in range(len(et_splitted)):
            if i + 1 == len(et_splitted):
                class_name = et_splitted[i]
            else:
                mod_name += et_splitted[i] + "."
        mod_name = mod_name[:len(mod_name) - 1]

        if mod_name in sys.modules.keys():
            mod = sys.modules[mod_name]
            new_obj = mod.__dict__[class_name]()

            for key in new_obj.__dict__.keys():
                if key in json_dict.keys():
                    current_value = json_dict[key]

                    if current_value is None or type(current_value) in AUTHORIZED_TYPE:
                        new_obj.__dict__[key] = current_value

                    elif type(current_value) == list:
                        new_obj.__dict__[key] = __deserialize_list(current_value)

                    elif type(current_value) == dict and "extended_type" in current_value.keys():
                        new_obj.__dict__[key] = deserialize(current_value)

                    elif type(current_value) == dict:
                        new_obj.__dict__[key] = __deserialize_dict(current_value)

            return new_obj

        else:
            raise des_error.DeserializationError("Can't deserialize : module not found")
    else:
        raise des_error.DeserializationError("Bad serialization : no extended_type")


def __deserialize_list(json_list):
    new_list = []
    for item in json_list:
        if item is None or type(item) in AUTHORIZED_TYPE:
            new_list.append(item)
        elif type(item) == list:
            new_list.append(__deserialize_list(item))
        elif type(item) == dict and "extended_type" in item.keys():
            new_list.append(deserialize(item))

    return new_list


def __deserialize_dict(json_dict):
    new_dict = {}

    for key in json_dict.keys():
        # KEY CHECK
        effective_key = key
        if type(key) in AUTHORIZED_TYPE:
            effective_key = key
        elif type(key) == dict and "extended_type" in key.keys():
            effective_key = deserialize(key)
        else:
            raise des_error.DeserializationError("Dict key can't be a list or a dict")
        # --------
        # VALUE CHECK
        json_value = json_dict[key]
        if json_value is None or type(json_value) in AUTHORIZED_TYPE:
            new_dict[effective_key] = json_value

        elif type(json_value) == list:
            new_dict[effective_key] = __deserialize_list(json_value)

        elif type(json_value) == dict and "extended_type" in json_value.keys():
            new_dict[effective_key] = deserialize(json_value)

        elif type(json_value) == dict:
            new_dict[effective_key] = __deserialize_dict(json_value)

    return new_dict
