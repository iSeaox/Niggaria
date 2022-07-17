import struct
import random
from numpy import number

from pygame.math import Vector2

import utils.serializable as serializable

import block.solid.stone as b_stone
import block.solid.dirt as b_dirt
import block.air as b_air
import block.decoration.plant as b_plant


class Chunk(serializable.Serializable):

    def __init__(self, chunk_x=None, chunk_width=32, chunk_height=256, number_of_chunks=64):
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.number_of_chunks = number_of_chunks
        self.number_of_chunks = 32 if self.number_of_chunks < 32 else self.number_of_chunks
        self.chunk_x = chunk_x
        if self.chunk_x is not None:
            self.x = self.chunk_x * self.chunk_width

        self.blocks = [0] * self.chunk_width * self.chunk_height
        self.background_blocks = []

    def gen(self, noise_handler):
        depth = 256
        plant_ceil = 0.3
        min = 100
        for i in range(self.chunk_width):
            x = i + self.chunk_width * self.chunk_x

            value = noise_handler.get_1D_noise(x, res=1024, length_mod=self.number_of_chunks * self.chunk_width)
            value += noise_handler.get_1D_noise(x, res=512, length_mod=self.number_of_chunks * self.chunk_width) * 0.5
            value += noise_handler.get_1D_noise(x, res=256, length_mod=self.number_of_chunks * self.chunk_width) * 0.25
            value += noise_handler.get_1D_noise(x, res=128, length_mod=self.number_of_chunks * self.chunk_width) * 0.125
            value += noise_handler.get_1D_noise(x, res=64, length_mod=self.number_of_chunks * self.chunk_width) * 0.125
            value += noise_handler.get_1D_noise(x, res=32, length_mod=self.number_of_chunks * self.chunk_width) * 0.025
            y = round(256 + value * self.chunk_height)

            # plant_value = abs(noise[1][(x * 10) % len(noise[1])])
            # if plant_value < plant_ceil:
            #     self.blocks[self.__get_index(x, y + 1)] = b_plant.Plant(x, y + 1, variant=random.randint(0, 5))
            for offset in range(depth):
                if y - offset >= 0:
                    value = noise_handler.get_2D_noise(Vector2(x, y - offset), res=256, length_mod=self.number_of_chunks * self.chunk_width)
                    value += noise_handler.get_2D_noise(Vector2(x, y - offset), res=128, length_mod=self.number_of_chunks * self.chunk_width) * 0.7
                    value += noise_handler.get_2D_noise(Vector2(x, y - offset), res=64, length_mod=self.number_of_chunks * self.chunk_width) * 0.6
                    value += noise_handler.get_2D_noise(Vector2(x, y - offset), res=32, length_mod=self.number_of_chunks * self.chunk_width) * 0.5
                    value = (value + 0.3) * 0.5

                    if value < 0.28:
                        if offset < 5:
                            self.blocks[self.__get_index(x, y - offset)] = b_dirt.Dirt(x, y - offset, property=0)
                        else:
                            self.blocks[self.__get_index(x, y - offset)] = b_stone.Stone(x, y - offset, property=0)

        return self

    def get_blocks_btw(self, min_y, max_y):
        return self.blocks[self.chunk_width * min_y:self.chunk_width * max_y]

    def get_block_at(self, x, y):
        temp = self.blocks[self.__get_index(x, y)]
        if temp == 0:
            return b_air.Air(x, y)
        return temp

    def __get_index(self, x, y):
        return self.chunk_width * y + (x - (self.chunk_x * self.chunk_width))

    def to_file(self):

        # header
        # | chunk_x (4 bytes) | len_blocks (4 bytes) | len_background_block (4 bytes) |

        header = b'chunk_file'
        header += struct.pack("III", self.chunk_x, len(self.blocks), len(self.background_blocks))

        blocks_data = b''
        for block in self.blocks:
            blocks_data += block.to_bytes()

        return header + blocks_data
