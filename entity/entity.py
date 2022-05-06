import utils.serializable as serializable
import utils.uid_generator as uid_generator
from pygame import Vector2


class Entity(serializable.Serializable):
    def __init__(self):
        self.type = "abstract_entity"
        self.instance_uid = uid_generator.gen_uid(8)

        # self.position = Vector2(0, 0)
        # self.velocity = Vector2(0, 0)
        # self.acceleration = Vector2(0, 0)

        self.x = 0
        self.y = 0
