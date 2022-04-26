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

    def gen(self, noise):
        max_height = 20

        for i in range(self.chunk_width):
            x = i + self.chunk_width * self.chunk_x
            y = round(20 + noise[1][x % len(noise[1])] * max_height)
            print(x, y)
            self.blocks.append(b_stone.Stone(x, y))

        return self
