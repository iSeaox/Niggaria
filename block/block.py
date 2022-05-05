import struct

import utils.serializable as serializable

STONE_BLOCK = 0
DIRT_BLOCK = 1

class Block(serializable.Serializable):

    def __init__(self, x = None, y = None, type = None, property = 0):
        self.x = x
        self.y = y
        self.type = type
        self.id = None
        self.variante = 0
        self.property = property


    def to_bytes(self):

        # | id (2 bytes) | variante (1 bytes) | property (4 bytes) | x (4 bytes) | y (4 bytes) |
        # = 15 bytes

        return struct.pack("HBI ii", self.id, self.variante, self.property, self.x, self.y)
