import action.action as action

import entity.human.player as player

class EntityMoveAction(action.Action):

    def __init__(self, entity = None):
        super().__init__()
        self.type = "entity_move_action"

        self.entity = entity
        if(entity != None):
            self.new_x = entity.x
            self.new_y = entity.y

    def deserialize(self, json_dict: dict):
        self = super().deserialize(json_dict)
        if(self.entity["type"] == "player"):
            self.entity = player.Player().deserialize(self.entity)

        return self
