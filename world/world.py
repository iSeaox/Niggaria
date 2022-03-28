import utils.serializable as serializable

import entity.human.player as player

class World(serializable.Serializable):

    def __init__(self):
        self.entities = {}

    def add_player_entity(self, player):
        self.entities[player.instance_uid] = player

    def remove_player_entity(self, player):
        if(player.instance_uid in self.entities.keys()):
            self.entities.pop(player.instance_uid)

    def deserialize(self, json_dict: dict):
        self = super().deserialize(json_dict)

        for key in self.entities.keys():
            if(self.entities[key]["type"] == "player"):
                self.entities[key] = player.Player().deserialize(self.entities[key])

        return self

    def set_local_player(self, player_entity):
        self.entities[player_entity.instance_uid] = player_entity
