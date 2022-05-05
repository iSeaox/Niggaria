import socket
import json

import server.packet.profile_transfert_packet as profile_transfert_packet
import server.packet.player_transfert_packet as player_transfert_packet
import server.packet.action_transfert_packet as action_transfert_packet
import server.packet.world_transfert_packet as world_transfert_packet

import security.profile_handler as profile_handler

import network.net_listener as net_listener

import entity.human.player as player

import action.server.connection_action as connection_action
import action.server.entity_move_action as entity_move_action
import action.client.key_action as key_action

import utils.time as time

import world.world as world


SERVER_TPS = 20


class Server:
    def __init__(self, ip_addr, port, logger):
        self.__run = False
        self.__debug = False
        self.__tps = SERVER_TPS
        self.__ip_addr = ip_addr
        self.__port = port
        self.__clock = time.Clock(SERVER_TPS)

        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__socket.bind((self.__ip_addr, self.__port))

        self.__net_buffer_size = 1024
        self.buffer = []
        self.logger = logger
        self.net_listener = net_listener.NetListener(self)
        self.net_listener.start()

        self.__connected_players = {}
        self.server_world = world.World()
        self.server_world.gen()

    def start(self):
        self.__run = True

        while(self.__run):
            self.__clock.start_tick()

            self.tick()
            self.__clock.tick()

    def tick(self):
        if self.__debug and len(self.buffer) > 0: self.logger.log(self.buffer)

        while len(self.buffer) > 0:
            packet = self.buffer[0]
            data = json.loads(packet[0].decode())

            if(data["type"] == "init_packet"):
                self.__player_access = packet[1]
                (ath, msg, profile) = profile_handler.use_profile(data["user"], data["password"])
                if(ath and (profile.uuid in self.__connected_players.keys())):
                    (ath, msg, profile) = (False, profile_handler.ALREADY_CONNECTED_CODE+ "already connected", None)

                raw_packet = profile_transfert_packet.ProfileTransfertPacket(profile, msg, ath).serialize()
                self.__socket.sendto(str.encode(raw_packet), packet[1])

                if(ath):
                    new_player_entity = player.Player(profile.uuid, profile.user)
                    self.__connected_players[profile.uuid] = {"access": packet[1], "entity": new_player_entity}
                    self.server_world.add_player_entity(new_player_entity)

                    # ---- DATA FOR JOINING PLAYER ----
                    raw_packet = player_transfert_packet.PlayerTransfertPacket(new_player_entity).serialize()
                    self.__socket.sendto(str.encode(raw_packet), packet[1])

                    raw_packet = world_transfert_packet.WorldTransfertPacket(self.server_world).serialize()
                    self.__socket.sendto(str.encode(raw_packet), packet[1])
                    # ---- DATA FOR OTHERS ----
                    c_action = connection_action.ConnectionAction(new_player_entity, connection_action.JOIN_SERVER)
                    raw_packet = action_transfert_packet.ActionTransfertPacket(c_action).serialize()
                    for player_info in self.__connected_players.values():
                        if(player_info["entity"].instance_uid != new_player_entity.instance_uid):
                            self.__socket.sendto(str.encode(raw_packet), player_info["access"])

                    self.logger.log(new_player_entity.name + " joined the game", subject="join")

            elif(data["type"] == "quit_packet"):
                if(data["profile"]["uuid"] in self.__connected_players.keys()):
                    c_action = connection_action.ConnectionAction(self.__connected_players[data["profile"]["uuid"]]["entity"], connection_action.QUIT_SERVER)

                    self.server_world.remove_player_entity(self.__connected_players[data["profile"]["uuid"]]["entity"])
                    self.__connected_players.pop(data["profile"]["uuid"])
                    self.logger.log(data["profile"]["user"] + " left the game", subject="quit")
                    raw_packet = action_transfert_packet.ActionTransfertPacket(c_action).serialize()
                    for player_info in self.__connected_players.values():
                        self.__socket.sendto(str.encode(raw_packet), player_info["access"])
            elif(data["type"] == "action_transfert_packet"):
                concerned_player = self.__connected_players[data["uuid"]]["entity"]
                if(data["action"]["type"] == "key_action"):
                    pressed_key = data["action"]["key"]
                    if(pressed_key == key_action.KEY_RIGHT):
                        if data['action']['action'] == key_action.ACTION_DOWN:
                            self.__connected_players_data[data['uuid']]['right'] = [True, data['timestamp']]
                        else:
                            time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['right'][1]
                            concerned_player.x += time_elapsed * (1.2 * 10 ** -8)

                            if self.__connected_players_data[data['uuid']]['left'][0]:
                                time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['left'][1]
                                concerned_player.x -= time_elapsed * (1.2 * 10 ** -8)
                                self.__connected_players_data[data['uuid']]['left'][1] = data['timestamp']


                            concerned_player.x %= self.server_world.size * world.CHUNK_WIDTH

                            em_action = entity_move_action.EntityMoveAction(concerned_player)
                            em_action.timestamp = data["timestamp"]
                            raw_packet = action_transfert_packet.ActionTransfertPacket(em_action, True).serialize()
                            self.__socket.sendto(str.encode(raw_packet), packet[1])

                            self.__connected_players_data[data['uuid']]['right'][0] = False

                    elif(pressed_key == key_action.KEY_LEFT):
                        if data['action']['action'] == key_action.ACTION_DOWN:
                            self.__connected_players_data[data['uuid']]['left'] = [True, data['timestamp']]
                        else:
                            if self.__connected_players_data[data['uuid']]['right'][0]:
                                time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['right'][1]
                                concerned_player.x += time_elapsed * (1.2 * 10 ** -8)
                                self.__connected_players_data[data['uuid']]['right'][1] = data['timestamp']

                            time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['left'][1]
                            concerned_player.x -= time_elapsed * (1.2 * 10 ** -8)


                            concerned_player.x %= self.server_world.size * world.CHUNK_WIDTH

                            em_action = entity_move_action.EntityMoveAction(concerned_player)
                            em_action.timestamp = data["timestamp"]
                            raw_packet = action_transfert_packet.ActionTransfertPacket(em_action, True).serialize()
                            self.__socket.sendto(str.encode(raw_packet), packet[1])

                            self.__connected_players_data[data['uuid']]['left'][0] = False

            self.buffer.pop(0)

        for player_uuid in self.__connected_players.keys():
            concerned_player = self.__connected_players[player_uuid]['entity']

            if self.__connected_players_data[player_uuid]['right'][0]:
                time_elapsed = self.__clock.get_time() - self.__connected_players_data[player_uuid]['right'][1]
                concerned_player.x += time_elapsed * (1.2 * 10 ** -8)
                self.__connected_players_data[player_uuid]['right'][1] = self.__clock.get_time()

            if self.__connected_players_data[player_uuid]['left'][0]:
                time_elapsed = self.__clock.get_time() - self.__connected_players_data[player_uuid]['left'][1]
                concerned_player.x -= time_elapsed * (1.2 * 10 ** -8)
                self.__connected_players_data[player_uuid]['left'][1] = self.__clock.get_time()

            for other_player_uuid in self.__connected_players.keys():
                if player_uuid != other_player_uuid:
                    em_action = entity_move_action.EntityMoveAction(self.__connected_players[other_player_uuid]['entity'])
                    em_action.timestamp = self.__clock.get_time()
                    raw_packet = action_transfert_packet.ActionTransfertPacket(em_action).serialize()
                    self.__socket.sendto(str.encode(raw_packet), self.__connected_players[player_uuid]['access'])


    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
