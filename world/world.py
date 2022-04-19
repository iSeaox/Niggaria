import sys

import utils.serializable as serializable

import entity.human.player as player

import world.chunk as chunk

class World(serializable.Serializable):

    def __init__(self):
        self.entities = {}

        self.chunks = []

    def gen(self):
        new_chunk = chunk.Chunk().gen()
        self.chunks.append(new_chunk)

    def add_player_entity(self, player):
        self.entities[player.instance_uid] = player

    def remove_player_entity(self, player):
        if(player.instance_uid in self.entities.keys()):
            self.entities.pop(player.instance_uid)


    def set_local_player(self, player_entity):
        self.entities[player_entity.instance_uid] = player_entity
