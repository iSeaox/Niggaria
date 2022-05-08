import struct
import random

import utils.serializable as serializable

import block.solid.dirt as b_dirt
import block.decoration.plant as b_plant


class Chunk(serializable.Serializable):

    def __init__(self, chunk_x=None, chunk_width=None):
        self.chunk_width = chunk_width
        self.chunk_x = chunk_x
        if self.chunk_x is not None:
            self.x = self.chunk_x * self.chunk_width

        self.blocks = []
        self.background_blocks = []

    def gen(self, noise):
        max_height = 40
        plant_ceil = 0.3

        for i in range(self.chunk_width):
            x = i + self.chunk_width * self.chunk_x
            y = round(40 + noise[1][x % len(noise[1])] * max_height)
            temp = b_dirt.PROPERTY_SIMPLE | b_dirt.PROPERTY_BOTH_SIDE

            plant_value = abs(noise[1][(x * 10) % len(noise[1])])
            if plant_value < plant_ceil:
                self.blocks.append(b_plant.Plant(x, y + 1, variant=random.randint(0, 5)))
            for offset in range(30):
                self.blocks.append(b_dirt.Dirt(x, y - offset, property=temp))

        return self

    def to_file(self):

        # header
        # | chunk_x (4 bytes) | len_blocks (4 bytes) | len_background_block (4 bytes) |

        header = b'chunk_file'
        header += struct.pack("III", self.chunk_x, len(self.blocks), len(self.background_blocks))

        blocks_data = b''
        for block in self.blocks:
            blocks_data += block.to_bytes()

        return header + blocks_data
