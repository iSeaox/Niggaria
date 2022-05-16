import utils.serializable as serializable

STONE_BLOCK = 0

class Block(serializable.Serializable):

    def __init__(self, x = None, y = None, type = None, nbt=None):
        self.x = x
        self.y = y
        self.type = type
        self.nbt = nbt
        self.id = None
