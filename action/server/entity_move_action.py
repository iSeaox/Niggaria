import action.action as action

import entity.human.player as player

class EntityMoveAction(action.Action):

    def __init__(self, entity = None):
        super().__init__()
        self.type = "entity_move_action"

        self.entity = entity
