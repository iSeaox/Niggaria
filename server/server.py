import socket
import time
import json

import server.packet.profile_transfert_packet as profile_transfert_packet
import server.packet.player_transfert_packet as player_transfert_packet

import security.profile_handler as profile_handler

import network.net_listener as net_listener

import entity.human.player as player

class Server:
    def __init__(self, ip_addr, port, logger):
        self.__run = False
        self.__tps = 20
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
        if(len(self.buffer) > 0):
            print(self.buffer)

        while(len(self.buffer) > 0):
            packet = self.buffer[0]
            data = json.loads(packet[0].decode())
            if(data["type"] == "init_packet"):
                self.__player_access = packet[1]
                (ath, msg, profile) = profile_handler.use_profile(data["user"], data["password"])
                new_player_entity = player.Player(profile.uuid)

                if(ath):
                    self.__connected_players[profile.uuid] = {"access": packet[1], "entity": new_player_entity}

                raw_packet = profile_transfert_packet.ProfileTransfertPacket(profile, msg, ath).serialize()
                self.__socket.sendto(str.encode(raw_packet), packet[1])

                raw_packet = player_transfert_packet.PlayerTransfertPacket(new_player_entity).serialize()
                self.__socket.sendto(str.encode(raw_packet), packet[1])

            elif(data["type"] == "action_transfert_packet"):
                concerned_player = self.__connected_players[data["uuid"]]["entity"]
                concerned_player.x += 5
            elif(data[0] == "MR"):
                self.__player.x += 5
                self.__socket.sendto(str.encode(str(self.__player.x) + "," + str(self.__player.y) + "," + data[1]), self.__player_access)

            self.buffer = self.buffer[1:]



    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
