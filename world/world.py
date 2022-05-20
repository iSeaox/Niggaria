import struct
import matplotlib.pyplot as plt

import utils.serializable as serializable

import world.chunk as chunk
import world.generator.noise as noise

import block.solid.dirt as b_dirt

import utils.file_utils as file_utils
import utils.bit_mask as bit_mask

CHUNK_WIDTH = 32
CHUNK_HEIGHT = 256


class World(serializable.Serializable):

    def __init__(self, size=50):
        self.entities = {}
        self.solid_bitmask = None
        self.size = size  # en nombre de chunk

        self.chunks = []

        # ----- Client Side --------
        self.fog_bitmask = None

    def gen(self):
        nb_point = 26

        gen_noise = noise.gen_smooth_noise(nb_point, (self.size * CHUNK_WIDTH) // (nb_point - 1), diff_max=2)
        gen_noise_bis = noise.gen_smooth_noise(nb_point * 2, (self.size * CHUNK_WIDTH) // (nb_point - 1) // 6, diff_max=2)

        fig, (ax1, ax2, ax3) = plt.subplots(3)
        ax1.plot(gen_noise[0], gen_noise[1], "ro")
        ax2.plot(gen_noise_bis[0], gen_noise_bis[1], "ro")

        sum_noise = ([], [])
        for i in range(len(gen_noise[0])):
            sum_noise[0].append(gen_noise[0][i])
            sum_noise[1].append(gen_noise[1][i] + gen_noise_bis[1][i % len(gen_noise_bis[0])] * 0.15)

        ax3.plot(sum_noise[0], sum_noise[1], "ro")
        plt.show()

        for i in range(self.size):
            new_chunk = chunk.Chunk(i, CHUNK_WIDTH, CHUNK_HEIGHT).gen(sum_noise)
            self.chunks.append(new_chunk)

        blocks = {}
        for c in self.chunks:
            for b in c.blocks:
                if b != 0:
                    blocks[(b.x, b.y)] = b

        for b_pos in blocks.keys():
            blocks[b_pos].property = 0
            b_up = self.get_block_at((b_pos[0], b_pos[1] + 1), blocks)
            b_down = self.get_block_at((b_pos[0], b_pos[1] - 1), blocks)
            b_right = self.get_block_at((b_pos[0] + 1, b_pos[1]), blocks)
            b_left = self.get_block_at((b_pos[0] - 1, b_pos[1]), blocks)
            b_up_right = self.get_block_at((b_pos[0] + 1, b_pos[1] + 1), blocks)
            b_up_left = self.get_block_at((b_pos[0] - 1, b_pos[1] + 1), blocks)

            if b_up is not None and b_up.is_solid():
                if b_down is not None and b_down.is_solid():
                    blocks[b_pos].property |= b_dirt.PROPERTY_HEIGHT_CENTER
                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_HEIGHT_DOWN

            else:
                if b_down is not None and b_down.is_solid():
                    blocks[b_pos].property |= b_dirt.PROPERTY_HEIGHT_TOP
                    blocks[b_pos].property |= b_dirt.PROPERTY_GRASS

                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_GRASS
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIMPLE

            if b_right is not None and b_right.is_solid():
                if b_left is not None and b_left.is_solid():
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIDE_MID
                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIDE_LEFT

            else:
                if b_left is not None and b_left.is_solid():
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIDE_RIGHT
                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_BOTH_SIDE

            if blocks[b_pos].property & b_dirt.PROPERTY_SIDE_MID == b_dirt.PROPERTY_SIDE_MID and blocks[b_pos].property & b_dirt.PROPERTY_HEIGHT_MASK == 0:
                if b_up_right is None or not b_up_right.is_solid():
                    if b_up_left is None or not b_up_left.is_solid():
                        blocks[b_pos].property |= b_dirt.PROPERTY_CORNER_ADJUST_BOTH
                    else:
                        blocks[b_pos].property |= b_dirt.PROPERTY_CORNER_ADJUST_RIGHT
                else:
                    if b_up_left is None or not b_up_left.is_solid():
                        blocks[b_pos].property |= b_dirt.PROPERTY_CORNER_ADJUST_LEFT

        print("map width: ", (self.size * CHUNK_WIDTH))

    def load_bitmask(self):
        self.solid_bitmask = bit_mask.BitMask(CHUNK_WIDTH * self.size, CHUNK_HEIGHT)
        for chunk in self.chunks:
            for block in chunk.blocks:
                if block != 0 and block.is_solid():
                    self.solid_bitmask.set(block.x, block.y)

        return self.solid_bitmask

    def load_fog_bitmask(self, radius=5):
        self.fog_bitmask = bit_mask.BitMask(CHUNK_WIDTH * self.size, CHUNK_HEIGHT)
        for offset in range(len(self.solid_bitmask)):
            if self.solid_bitmask.is_set(offset):
                x, y = self.fog_bitmask.convert_offset(offset)

                working_interval = [i for i in range(-radius, radius + 1)]
                working_interval.remove(0)
                for dx in working_interval:
                    for dy in working_interval:
                        if dx * dx + dy * dy <= radius * radius:
                            if not self.solid_bitmask.is_set(dx + x, dy + y):
                                self.fog_bitmask.clear(x, y)
                                break
                            else:
                                self.fog_bitmask.set(x, y)


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
        return super().serialize(("chunks","solid_bitmask", "fog_bitmask"))

    def full_serialize(self):
        return super().serialize()

    def get_block_at(self, pos, block_dlist=None):
        if block_dlist is None:
            chunk = self.get_chunk(pos[0] // CHUNK_WIDTH)
            return chunk.get_block_at(pos[0], pos[1])

        elif pos in block_dlist.keys():
            return block_dlist[pos]
        return

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
