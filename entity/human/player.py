import entity.entity as entity
import security.player_profile as player_profile
from pygame import Vector2


class Player(entity.Entity):
    def __init__(self, uuid=None, name=None):
        super().__init__()

        self.type = "player"
        self.uuid = uuid
        self.name = name

        self.x = 20
        self.y = 30

        self.predicted_x = 20
        self.predicted_y = 30

        self.velocity = [0, 0]
        self.predicted_velocity = [0, 0]
