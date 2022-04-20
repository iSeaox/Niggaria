import random

import utils.serializable as serializable

import block.solid.stone as b_stone


class Chunk(serializable.Serializable):

    def __init__(self, chunk_x = None, chunk_width = None):
        self.chunk_width = chunk_width
        self.chunk_x = chunk_x
        if(self.chunk_x != None):
            self.x = self.chunk_x * self.chunk_width

        self.blocks = []
        self.background_block = []

    def gen(self):
        self.blocks.append(b_stone.Stone(0 + self.chunk_width * self.chunk_x, 26))

        for i in range(self.chunk_width):

            self.blocks.append(b_stone.Stone(i + self.chunk_width * self.chunk_x, 20 + random.randint(-1, 1)))

        return self
