import entity.entity as entity
import security.player_profile as player_profile
from pygame import Vector2


class Player(entity.Entity):
    def __init__(self, uuid=None, name=None):
        super().__init__()

        self.type = "player"
        self.uuid = uuid
        self.name = name

        self.position = Vector2(20, 30)
