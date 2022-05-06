import random
import struct

import utils.serializable as serializable

import block.solid.stone as b_stone
import block.solid.dirt as b_dirt


class Chunk(serializable.Serializable):

    def __init__(self, chunk_x = None, chunk_width = None):
        self.chunk_width = chunk_width
        self.chunk_x = chunk_x
        if(self.chunk_x != None):
            self.x = self.chunk_x * self.chunk_width

        self.blocks = []
        self.background_blocks = []

    def gen(self, noise):
        max_height = 40

        for i in range(self.chunk_width):
            x = i + self.chunk_width * self.chunk_x
            y = round(40 + noise[1][x % len(noise[1])] * max_height)
            temp = b_dirt.PROPERTY_SIMPLE | b_dirt.PROPERTY_BOTH_SIDE
            self.blocks.append(b_dirt.Dirt(x, y, property = temp))
            for offset in range(20):
                self.blocks.append(b_dirt.Dirt(x, y - offset, property = temp))

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
