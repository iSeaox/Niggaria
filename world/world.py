import sys
import matplotlib.pyplot as plt

import utils.serializable as serializable

import entity.human.player as player

import world.chunk as chunk
import world.generator.noise as noise

import block.solid.dirt as b_dirt

CHUNK_WIDTH = 32

class World(serializable.Serializable):

    def __init__(self, size = 10):
        self.entities = {}
        self.size = size# en nombre de chunk

        self.chunks = []

    def gen(self):
        nb_point = 7
        gen_noise = noise.gen_smooth_noise(nb_point, (self.size * CHUNK_WIDTH) // (nb_point - 1), diff_max=2)
        gen_noise_bis = noise.gen_smooth_noise(nb_point * 2, (self.size * CHUNK_WIDTH) // (nb_point - 1) // 6, diff_max=2)

        fig, (ax1, ax2, ax3) = plt.subplots(3)
        ax1.plot(gen_noise[0], gen_noise[1], "ro")
        ax2.plot(gen_noise_bis[0], gen_noise_bis[1], "ro")

        sum_noise = ([], [])
        for i in range(len(gen_noise[0])):
            sum_noise[0].append(gen_noise[0][i])
            sum_noise[1].append(gen_noise[1][i] + gen_noise_bis[1][i % len(gen_noise_bis[0])] * 0.10)

        ax3.plot(sum_noise[0], sum_noise[1], "ro")
        plt.show()

        for i in range(self.size):
            new_chunk = chunk.Chunk(i, CHUNK_WIDTH).gen(sum_noise)
            self.chunks.append(new_chunk)

        blocks = {}
        for c in self.chunks:
            for b in c.blocks:
                blocks[(b.x, b.y)] = b

        for b_pos in blocks.keys():
            blocks[b_pos].property = 0
            b_up = (b_pos[0], b_pos[1] + 1)
            b_down = (b_pos[0], b_pos[1] - 1)
            b_right = (b_pos[0] + 1, b_pos[1])
            b_left = (b_pos[0] - 1, b_pos[1])
            b_up_right = (b_pos[0] + 1, b_pos[1] + 1)
            b_up_left = (b_pos[0] - 1, b_pos[1] + 1)

            if(b_up in blocks.keys()):
                if(b_down in blocks.keys()):
                    blocks[b_pos].property |= b_dirt.PROPERTY_HEIGHT_CENTER
                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_HEIGHT_DOWN

            else:
                if(b_down in blocks.keys()):
                    blocks[b_pos].property |= b_dirt.PROPERTY_HEIGHT_TOP
                    blocks[b_pos].property |= b_dirt.PROPERTY_GRASS

                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIMPLE

            if(b_right in blocks.keys()):
                if(b_left in blocks.keys()):
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIDE_MID
                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIDE_LEFT

            else:
                if(b_left in blocks.keys()):
                    blocks[b_pos].property |= b_dirt.PROPERTY_SIDE_RIGHT
                else:
                    blocks[b_pos].property |= b_dirt.PROPERTY_BOTH_SIDE

            if(blocks[b_pos].property & b_dirt.PROPERTY_SIDE_MID == b_dirt.PROPERTY_SIDE_MID and blocks[b_pos].property & b_dirt.PROPERTY_HEIGHT_MASK == 0):
                if(not(b_up_right in blocks.keys())):
                    if(not(b_up_left in blocks.keys())):
                        blocks[b_pos].property |= b_dirt.PROPERTY_CORNER_ADJUST_BOTH
                    else:
                        blocks[b_pos].property |= b_dirt.PROPERTY_CORNER_ADJUST_RIGHT
                else:
                    if(not(b_up_left in blocks.keys())):
                        blocks[b_pos].property |= b_dirt.PROPERTY_CORNER_ADJUST_LEFT





        print("map width: ", (self.size * CHUNK_WIDTH), " | ", -3 % (self.size * CHUNK_WIDTH))

    def get_chunk(self, chunk_x):
        return self.chunks[chunk_x % self.size]

    def add_player_entity(self, player):
        self.entities[player.instance_uid] = player

    def remove_player_entity(self, player):
        if(player.instance_uid in self.entities.keys()):
            self.entities.pop(player.instance_uid)


    def set_local_player(self, player_entity):
        self.entities[player_entity.instance_uid] = player_entity

    def serialize(self):
        return super().serialize("chunks")

    def full_serialize(self):
        return super().serialize()
