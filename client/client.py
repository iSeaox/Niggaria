import socket
import time
import json
import pygame

import network.net_listener as net_listener

import entity.human.player as player

import client.packet.init_packet as init_packet
import client.packet.action_transfert_packet as action_transfert_packet
import client.packet.quit_packet as quit_packet
import client.render.entity_renderer as entity_renderer

import security.player_profile as player_profile

import action.client.key_action as key_action

class Client:
    def __init__(self, server_acces, logger):
        self.__run = False
        self.__fps = 10
        self.__player = None
        self.__loading = True
        self.profile = None

        self.__actions_buffer = []

        self.server_acces = server_acces
        self.logger = logger
        self.__net_buffer_size = 1024

        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.net_listener = net_listener.NetListener(self)
        self.buffer = []

    def start(self):
        self.__run = True

        pygame.init()
        screen = pygame.display.set_mode((720, 480))
        pygame.display.set_caption("Niggaria")

        packet_data = init_packet.InitPacket("pedro", "pedro").serialize()
        self.__socket.sendto(str.encode(packet_data), self.server_acces)
        self.net_listener.start()

        while(self.__run):
            begin = time.time_ns() / 1_000_000_000

            self.update()
            self.render(screen)
            pygame.display.flip()

            elapsed = (time.time_ns() / 1_000_000_000 - begin)
            waiting_time = (1 / self.__fps) - elapsed
            if(waiting_time > 0):
                time.sleep(waiting_time)

        raw_packet = quit_packet.QuitPacket(self.profile).serialize()
        self.__socket.sendto(str.encode(raw_packet), self.server_acces)

    def update(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.__run = False
            elif(not(self.__loading)):
                if(event.type == pygame.KEYDOWN):
                    if(event.key == 100):
                        new_action = key_action.KeyAction(key_action.KEY_RIGHT)
                        self.__actions_buffer.append(new_action)
                        raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                        self.__socket.sendto(str.encode(raw_packet), self.server_acces)

        # --------- PACKET HANDLING ---------
        if(len(self.buffer) > 0):
            print(self.buffer)

        while(len(self.buffer) > 0):
            raw = self.buffer[0]
            packet = json.loads(raw[0].decode())

            if(packet["type"] == "profile_transfert_packet"):
                if(packet["authorized"]):
                    self.profile = player_profile.deserialize(packet["profile"])
                else:
                    self.logger.log(packet["message"], subject="refused")
                    self.__run = False

            elif(packet["type"] == "player_transfert_packet"):
                self.__player = player.Player().deserialize(packet["player"])
                self.logger.log("player entity received", subject="load")
                self.__loading = False

            elif(packet["type"] == "entity_position_update_packet"):
                self.__player.x = packet["new_x"]
                self.__player.y = packet["new_y"]

                while(len(self.__actions_buffer) > 0 and self.__actions_buffer[0].timestamp <= packet["action_timestamp"]):
                    self.__actions_buffer = self.__actions_buffer[1:]

            self.buffer = self.buffer[1:]
        # -------------------------------------

        if(not(self.__loading)):
            self.__player.predicted_x = self.__player.x
            self.__player.predicted_y = self.__player.y

            for action in self.__actions_buffer:
                if(action.type == "key_action"):
                    if(action.key == key_action.KEY_RIGHT):
                        self.__player.predicted_x += 5

    def render(self, screen):
        if(not(self.__loading)):
            screen.fill((0, 0, 0))

            entity_renderer.render_entity(screen, self.__player)

    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
