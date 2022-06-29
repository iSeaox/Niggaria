import struct

import utils.serializable as serializable

AIR_BLOCK = 0
STONE_BLOCK = 1
DIRT_BLOCK = 2


class Block(serializable.Serializable):
    def __init__(self, x=None, y=None, type=None, property=0, variant=0):
        self.x = x
        self.y = y
        self.type = type
        self.id = None
        self.variant = variant
        self.property = property

    def to_bytes(self):
        # | id (2 bytes) | variant (1 bytes) | property (4 bytes) | x (4 bytes) | y (4 bytes) |
        # = 15 bytes
        return struct.pack("HBI ii", self.id, self.variant, self.property, self.x, self.y)

    def is_solid(self):
        raise NotImplementedError()

    def is_air(self):
        raise NotImplementedError()

    def set_property(self, *args):
        raise NotImplementedError()
