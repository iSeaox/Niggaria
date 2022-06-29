import struct
import matplotlib.pyplot as plt

import utils.serializable as serializable

import world.chunk as chunk
import world.noise.noise_handler as noise_handler

import block.solid.dirt as b_dirt
import block.air as b_air

import utils.file_utils as file_utils
import utils.bit_mask as bit_mask

CHUNK_WIDTH = 32
CHUNK_HEIGHT = 256


class World(serializable.Serializable):

    def __init__(self, size=64):
        self.entities = {}
        self.solid_bitmask = None
        self.size = size  # en nombre de chunk

        self.chunks = []

    def gen(self):
        n_handler = noise_handler.NoiseHandler("Niggaria")
        for i in range(self.size):
            new_chunk = chunk.Chunk(i, CHUNK_WIDTH, CHUNK_HEIGHT).gen(n_handler)
            self.chunks.append(new_chunk)

        blocks = {}
        for c in self.chunks:
            for b in c.blocks:
                if b != 0:
                    blocks[(b.x, b.y)] = b

        for b_pos in blocks.keys():
            b_up = self.get_block_at((b_pos[0], b_pos[1] + 1), blocks)
            b_down = self.get_block_at((b_pos[0], b_pos[1] - 1), blocks)
            b_right = self.get_block_at((b_pos[0] + 1, b_pos[1]), blocks)
            b_left = self.get_block_at((b_pos[0] - 1, b_pos[1]), blocks)
            b_up_right = self.get_block_at((b_pos[0] + 1, b_pos[1] + 1), blocks)
            b_up_left = self.get_block_at((b_pos[0] - 1, b_pos[1] + 1), blocks)

            blocks[b_pos].set_property(b_up, b_down, b_left, b_right, b_up_right, b_up_left)

        print("map width: ", (self.size * CHUNK_WIDTH))

    def load_bitmask(self):
        self.solid_bitmask = bit_mask.BitMask(CHUNK_WIDTH * self.size, CHUNK_HEIGHT)
        for chunk in self.chunks:
            for block in chunk.blocks:
                if block != 0 and block.is_solid():
                    self.solid_bitmask.set(block.y * self.size + block.x)

        return self.solid_bitmask

    def get_chunk(self, chunk_x):
        return self.chunks[chunk_x % self.size]

    def add_player_entity(self, player):
        self.entities[player.instance_uid] = player

    def remove_player_entity(self, player):
        if player.instance_uid in self.entities.keys():
            self.entities.pop(player.instance_uid)

    def set_local_player(self, player_entity):
        self.entities[player_entity.instance_uid] = player_entity

    def serialize(self):
        return super().serialize(("chunks","solid_bitmask"))

    def full_serialize(self):
        return super().serialize()

    def get_block_at(self, pos, block_dlist=None):
        if block_dlist is None:
            chunk = self.get_chunk(pos[0] // CHUNK_WIDTH)
            return chunk.get_block_at(pos[0], pos[1])

        elif pos in block_dlist.keys():
            return block_dlist[pos]

        return b_air.Air(pos[0], pos[1])

    def to_bytes(self):
        pass

    def to_files(self, path):
        files_data = {}
        for i in range(len(self.chunks)):
            working_file = file_utils.create_file(path + r"\chunk\chunk_"+str(i)+".chu")

            with working_file.open("wb+") as file:
                file.seek(0)
                file.write(self.chunks[i].to_file())

        working_file = file_utils.create_file(path + r"\world_desc.dat")
        with working_file.open("wb+") as file:
            file.seek(0)
            content = b'world_desc'

            # | size (2 bytes) |

            content += struct.pack("H", self.size)
            file.write(content)

        working_file = file_utils.create_file(path + r"\entities.dat")
        with working_file.open("wb+") as file:
            file.seek(0)
            header = b'entities_file'
            # | len_entities (2 bytes) |
            header += struct.pack("H", len(self.entities))
            content = b''
            for entity in self.entities:
                content += entity.to_bytes()
