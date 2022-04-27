import sys
import matplotlib.pyplot as plt

import utils.serializable as serializable

import entity.human.player as player

import world.chunk as chunk
import world.generator.noise as noise

CHUNK_WIDTH = 32

class World(serializable.Serializable):

    def __init__(self, size = 6):
        self.entities = {}
        self.size = size# en nombre de chunk

        self.chunks = []

    def gen(self):
        nb_point = 8
        gen_noise = noise.gen_smooth_noise(nb_point, (self.size * CHUNK_WIDTH) // nb_point)
        plt.plot(gen_noise[0], gen_noise[1], "ro")
        plt.show()

        for i in range(self.size):
            new_chunk = chunk.Chunk(i, CHUNK_WIDTH).gen(gen_noise)
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
