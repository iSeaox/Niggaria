import utils.serializable as serializable

import block.solid.stone as b_stone

CHUNK_WIDTH = 32

class Chunk(serializable.Serializable):

    def __init__(self, chunk_x = None):

        self.chunk_x = chunk_x
        if(self.chunk_x != None):
            self.x = self.chunk_x * CHUNK_WIDTH

        self.blocks = []
        self.background_block = []

    def gen(self):
        self.blocks.append(b_stone.Stone(10, 20))
        self.blocks.append(b_stone.Stone(0, 0))
        self.blocks.append(b_stone.Stone(11, 20))
        self.blocks.append(b_stone.Stone(12, 20))
        self.blocks.append(b_stone.Stone(13, 20))
        self.blocks.append(b_stone.Stone(14, 20))
        self.blocks.append(b_stone.Stone(15, 20))
        self.blocks.append(b_stone.Stone(16, 20))

        self.blocks.append(b_stone.Stone(17, 21))
        self.blocks.append(b_stone.Stone(18, 21))
        self.blocks.append(b_stone.Stone(19, 22))
        self.blocks.append(b_stone.Stone(20, 21))

        return self
