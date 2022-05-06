import struct

import utils.serializable as serializable
import utils.uid_generator as uid_generator
from pygame import Vector2


ABSTRACT_ENTITY = 0
PLAYER_ENTITY = 1

class Entity(serializable.Serializable):
    def __init__(self):
        self.type = "abstract_entity"
        self.id = ABSTRACT_ENTITY
        self.instance_uid = uid_generator.gen_uid(8)

        # self.position = Vector2(0, 0)
        # self.velocity = Vector2(0, 0)
        # self.acceleration = Vector2(0, 0)

        self.x = 0
        self.y = 0

        self.predicted_x = 0
        self.predicted_y = 0

        self.velocity = [0, 0]

    def add_velocity(vector):
        self.velocity[0] += vector[0]
        self.velocity[1] += vector[1]

    def to_bytes(self):
        # | id (2 bytes) | uid (8 bytes) | x (8 bytes) | y (8 bytes) |
        content = struct.pack("H", self.id)
        content += str.encode(self.instance_uid)
        content += struct.pack("dd", self.x, self.y)

        return content
