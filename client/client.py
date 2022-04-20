import socket
import time
import json
import pygame

import network.net_listener as net_listener

import utils.serializable as serializable

import entity.human.player as player

import client.packet.action_transfert_packet as action_transfert_packet
import client.packet.quit_packet as quit_packet

import client.render.world_renderer as world_renderer
import client.render.texture_handler as texture_handler
import client.render.view as view_handler

import client.update.entity_updater as entity_updater
import client.update.world_updater as world_updater

import client.launcher.launcher as launcher


import action.client.key_action as key_action
import action.server.connection_action as connection_action
import action.server.entity_move_action as entity_move_action


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
        self.__net_buffer_size = 1024 * 32

        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.net_listener = net_listener.NetListener(self)

        self.buffer = []

        self.texture_handler = texture_handler.TextureHandler(self.logger)
        self.__launcher = launcher.Launcher(self)

        self.view = None

    def start(self):
        self.__run = True

        pygame.init()
        screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Niggaria")

        self.texture_handler.load_textures(part="gui")
        self.__launcher.start(screen)
        self.view = view_handler.View((0, 17), self.__player, screen.get_size(), 2, self.__world.size)


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

            if(packet["type"] == "action_transfert_packet"):
                if(packet["action"]["type"] == "connection_action"):
                    c_action = packet["action"]
                    if(c_action["connection_type"] == connection_action.JOIN_SERVER):
                        packet_player = serializable.deserialize(c_action["player"])
                        self.__world.add_player_entity(packet_player)
                        self.logger.log(packet_player.name + " joined the game", subject="join")

                    elif(c_action["connection_type"] == connection_action.QUIT_SERVER):
                        packet_player = serializable.deserialize(c_action["player"])
                        self.__world.remove_player_entity(packet_player)
                        self.logger.log(packet_player.name + " left the game", subject="quit")

                elif(packet["action"]["type"] == "entity_move_action"):
                    em_action = serializable.deserialize(packet["action"])
                    if(packet["ack"] == True):
                        self.__entity_updater.push_local_action(em_action)
                    else:
                        self.__entity_updater.push_action(em_action.entity, em_action)

            self.buffer = self.buffer[1:]
        # -------------------------------------

        self.__world_updater.update(self.__world)
        self.view.check()


    def render(self, screen):
        screen.fill((0, 0, 0))

        world_renderer.render_world(screen, self.__world, self.view, self.texture_handler)

    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size

    def get_player(self):
        return self.__player

    def set_player(self, player):
        self.__player = player

    def get_world(self):
        return self.__world

    def set_world(self, world):
        self.__world = world

    def get_world_updater(self):
        return self.__world_updater

    def get_entity_updater(self):
        return self.__entity_updater

    def get_socket(self):
        return self.__socket
