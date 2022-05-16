import action.server.entity_move_action as entity_move_action
import action.client.key_action as key_action

import server.packet.action_transfert_packet as action_transfert_packet

import utils.clock as clock

from pygame import Vector2


class ServerPlayer:
    def __init__(self, player, tcp_access, profile, server_tps):
        self.player = player

        self.tcp_access = tcp_access
        self.udp_access = None
        self.profile = profile

        self.clock = clock.Clock()
        self.__server_tps = server_tps

    def get_mouvement_with_timestep(self, timestep, velocity):
        return velocity * timestep / (1_000_000_000 / self.__server_tps)

    def update_player_action(self, data):
        em_packets = []
        action = data['action']

        if action['type'] == "key_action":
            if action['action'] == key_action.ACTION_DOWN:
                if action['key'] == key_action.KEY_RIGHT:
                    self.player.acceleration += Vector2(1, 0)
                    self.player.position += self.get_mouvement_with_timestep(self.clock.get_time() - data['timestamp'], -self.player.velocity + (self.player.velocity + Vector2(1, 0)))
                elif action['key'] == key_action.KEY_LEFT:
                    self.player.acceleration += Vector2(-1, 0)
                    self.player.position += self.get_mouvement_with_timestep(self.clock.get_time() - data['timestamp'], -self.player.velocity + (self.player.velocity + Vector2(-1, 0)))
                elif action['key'] == key_action.KEY_JUMP:
                    pass
                    # self.player.acceleration += Vector2(0, 0.5)
            elif action['action'] == key_action.ACTION_UP:
                if action['key'] == key_action.KEY_RIGHT:
                    self.player.acceleration += Vector2(-1, 0)
                    self.player.position += self.get_mouvement_with_timestep(self.clock.get_time() - data['timestamp'], -self.player.velocity + (self.player.velocity + Vector2(-1, 0)))

                    em_action = entity_move_action.EntityMoveAction(self.player)
                    em_action.timestamp = data["timestamp"]
                    em_packets.append(action_transfert_packet.ActionTransfertPacket(em_action, True).serialize())
                elif action['key'] == key_action.KEY_LEFT:
                    self.player.acceleration += Vector2(1, 0)
                    self.player.position += self.get_mouvement_with_timestep(self.clock.get_time() - data['timestamp'], -self.player.velocity + (self.player.velocity + Vector2(1, 0)))

                    em_action = entity_move_action.EntityMoveAction(self.player)
                    em_action.timestamp = data["timestamp"]
                    em_packets.append(action_transfert_packet.ActionTransfertPacket(em_action, True).serialize())

        return em_packets

    def update_player(self, world_size):
        self.player.velocity += self.player.acceleration
        self.player.acceleration = Vector2(0, 0)
        self.player.position += self.get_mouvement_with_timestep(self.clock.time_step(), self.player.velocity)

        self.player.position.x %= world_size
