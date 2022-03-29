import socket
import time
import json
import pygame

import network.net_listener as net_listener

import entity.human.player as player

import client.packet.init_packet as init_packet
import client.packet.action_transfert_packet as action_transfert_packet
import client.packet.quit_packet as quit_packet
import client.render.world_renderer as world_renderer
import client.update.entity_updater as entity_updater
import client.update.world_updater as world_updater

import security.player_profile as player_profile

import action.client.key_action as key_action
import action.server.connection_action as connection_action
import action.server.entity_move_action as entity_move_action

import world.world as world

CLIENT_FPS = 60

class Client:
    def __init__(self, server_acces, logger):
        self.__run = False
        self.__fps = CLIENT_FPS
        self.__player = None
        self.__world = None

        self.__entity_updater = entity_updater.EntityUpdater()
        self.__world_updater = world_updater.WorldUpdater(self.__entity_updater)

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

        packet_data = init_packet.InitPacket("marco", "marco").serialize()
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

        if(not(self.__loading)):
            if(pygame.key.get_pressed()[100]):
                new_action = key_action.KeyAction(key_action.KEY_RIGHT)
                self.__entity_updater.push_local_action(new_action)
                raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                self.__socket.sendto(str.encode(raw_packet), self.server_acces)
            if(pygame.key.get_pressed()[113]):
                new_action = key_action.KeyAction(key_action.KEY_LEFT)
                self.__entity_updater.push_local_action(new_action)
                raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                self.__socket.sendto(str.encode(raw_packet), self.server_acces)

        # --------- PACKET HANDLING ---------
        # if(len(self.buffer) > 0):
        #     print(self.buffer)

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

            elif(packet["type"] == "world_transfert_packet"):
                self.__world = world.World().deserialize(packet["world"])
                self.logger.log("world received", subject="load")

                self.__world.set_local_player(self.__player)
                self.__world_updater.local_player = self.__player
                self.__entity_updater.local_player = self.__player
                self.logger.log("world player linked with local player entity", subject="load")
                self.__loading = False

            elif(packet["type"] == "action_transfert_packet"):
                if(packet["action"]["type"] == "connection_action"):
                    c_action = packet["action"]
                    if(c_action["connection_type"] == connection_action.JOIN_SERVER):
                        packet_player = player.Player().deserialize(c_action["player"])
                        self.__world.add_player_entity(packet_player)
                        self.logger.log(packet_player.name + " joined the game", subject="join")

                    elif(c_action["connection_type"] == connection_action.QUIT_SERVER):
                        packet_player = player.Player().deserialize(c_action["player"])
                        self.__world.remove_player_entity(packet_player)
                        self.logger.log(packet_player.name + " left the game", subject="quit")

                elif(packet["action"]["type"] == "entity_move_action"):
                    em_action = entity_move_action.EntityMoveAction().deserialize(packet["action"])
                    if(packet["ack"] == True):
                        self.__entity_updater.push_local_action(em_action)
                    else:
                        self.__entity_updater.push_action(em_action.entity, em_action)

            self.buffer = self.buffer[1:]
        # -------------------------------------

        if(not(self.__loading)):
            self.__world_updater.update(self.__world)


    def render(self, screen):
        if(not(self.__loading)):
            screen.fill((0, 0, 0))

            world_renderer.render_world(screen, self.__world)

    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
