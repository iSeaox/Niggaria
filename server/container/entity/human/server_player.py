from copy import copy
from pygame import Vector2

import action.client.key_action as key_action
import action.server.entity_move_action as entity_move_action
import server.packet.action_transfert_packet as action_transfert_packet
import utils.clock as clock


class ServerPlayer:
    def __init__(self, player, tcp_access, profile, server_tps):
        self.player = player

        self.tcp_access = tcp_access
        self.udp_access = None
        self.profile = profile

        self.clock = clock.Clock()
        self.__server_tps = server_tps

        self.gravity = [False, Vector2(0, -0.001)]

    def last_pos(self, timestep, velocity):
        return velocity * (timestep / (1_000_000_000 / self.__server_tps))

    def update_player_action(self, data):
        em_packets = []
        action = data['action']

        if action['type'] == "key_action":
            if action['action'] == key_action.ACTION_DOWN:
                if action['key'] == key_action.KEY_RIGHT:
                    self.player.acceleration += Vector2(1, 0)
                    self.player.position += self.last_pos(self.clock.get_time() - data['timestamp'], Vector2(1, 0))

                elif action['key'] == key_action.KEY_LEFT:
                    self.player.acceleration += Vector2(-1, 0)
                    self.player.position += self.last_pos(self.clock.get_time() - data['timestamp'], Vector2(-1, 0))

                elif action['key'] == key_action.KEY_JUMP:
                    self.player.acceleration += Vector2(0, 0.05)
                    self.player.position += self.last_pos(self.clock.get_time() - data['timestamp'], Vector2(0, 0.05))

            elif action['action'] == key_action.ACTION_UP:
                if action['key'] == key_action.KEY_RIGHT:
                    self.player.acceleration += Vector2(-1, 0)
                    self.player.position += self.last_pos(self.clock.get_time() - data['timestamp'], Vector2(-1, 0))

                    em_action = entity_move_action.EntityMoveAction(self.player)
                    em_action.timestamp = data["timestamp"]
                    em_packets.append(action_transfert_packet.ActionTransfertPacket(em_action, True).serialize())

                elif action['key'] == key_action.KEY_LEFT:
                    self.player.acceleration += Vector2(1, 0)
                    self.player.position += self.last_pos(self.clock.get_time() - data['timestamp'], Vector2(1, 0))

                    em_action = entity_move_action.EntityMoveAction(self.player)
                    em_action.timestamp = data["timestamp"]
                    em_packets.append(action_transfert_packet.ActionTransfertPacket(em_action, True).serialize())

            elif (action['action'], action['key']) == (-1, -1):
                self.clock.time = self.clock.get_time()
                self.gravity[0] = True

        return em_packets

    def update_player(self, world_size):
        timestep = self.clock.time_step()

        if self.gravity[0] and False:
            self.player.acceleration += self.gravity[1] * (timestep / (1_000_000_000 / self.__server_tps))

        self.player.velocity += self.player.acceleration
        self.player.acceleration = Vector2(0, 0)
        self.player.position += self.last_pos(timestep, self.player.velocity)

        self.player.position.x %= world_size
