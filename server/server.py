import socket
import time
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

import world.world as world

SERVER_TPS = 20

class Server:
    def __init__(self, ip_addr, port, logger):
        self.__run = False
        self.__tps = SERVER_TPS
        self.__ip_addr = ip_addr
        self.__port = port

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
            begin = time.time_ns() / 1_000_000_000

            self.tick()

            elapsed = (time.time_ns() / 1_000_000_000 - begin)
            waiting_time = (1 / self.__tps) - elapsed
            if(waiting_time > 0):
                time.sleep(waiting_time)

    def tick(self):
        move_actions = {}

        if(len(self.buffer) > 0):
            print(self.buffer)

        while(len(self.buffer) > 0):
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
                        concerned_player.x += 0.2
                    elif(pressed_key == key_action.KEY_LEFT):
                        concerned_player.x -= 0.2

                    concerned_player.x %= self.server_world.size * world.CHUNK_WIDTH

                em_action = entity_move_action.EntityMoveAction(concerned_player)
                em_action.timestamp = data["timestamp"]
                raw_packet = action_transfert_packet.ActionTransfertPacket(em_action, True).serialize()
                self.__socket.sendto(str.encode(raw_packet), packet[1])

                em_action.timestamp = time.time_ns()
                move_actions[em_action.entity.instance_uid] = (em_action, data["uuid"])

            self.buffer = self.buffer[1:]

        for move_action in move_actions.values():
            for other_player_uuid in self.__connected_players.keys():
                if(other_player_uuid != move_action[1]):
                    raw_packet = action_transfert_packet.ActionTransfertPacket(move_action[0]).serialize()
                    self.__socket.sendto(str.encode(raw_packet), self.__connected_players[other_player_uuid]["access"])



    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
