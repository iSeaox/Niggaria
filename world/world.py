import sys
import matplotlib.pyplot as plt

import utils.serializable as serializable

import entity.human.player as player

import world.chunk as chunk
import world.generator.noise as noise

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
