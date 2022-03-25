import entity.entity as entity

import security.player_profile as player_profile

class Player(entity.Entity):
    def __init__(self, uuid = None):
        super().__init__()
        self.type = "player"
        self.uuid = uuid

        self.x = 20
        self.y = 100
