import utils.serializable as serializable

import block.solid.stone as b_stone

class Chunk(serializable.Serializable):

    def __init__(self):

        self.blocks = []
        self.background_block = []

    def gen(self):
        self.blocks.append(b_stone.Stone(80, 80))

        return self
