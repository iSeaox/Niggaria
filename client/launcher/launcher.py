import pygame
import time
import json

import entity.human.player as player

import client.packet.init_packet as init_packet
import client.gui.clickable.button as gui_button

import security.player_profile as player_profile

import world.world as world

class Launcher:

    def __init__(self, client, screen = None):
        self.client = client
        self.__screen = screen
        self.__fps = 10
        self.is_active = False
        self.abort = False
        self.logger = self.client.logger

        self.test = gui_button.Button(10, 10, 80, 80, self.trigger_button)

    def start(self, screen):
        self.__screen = screen
        self.is_active = True

        # packet_data = init_packet.InitPacket("marco", "marco").serialize()
        # self.client.get_socket().sendto(str.encode(packet_data), self.client.server_acces)
        # self.client.net_listener.start()

        while(self.is_active):
            begin = time.time_ns() / 1_000_000_000

            self.update()
            self.render()
            pygame.display.flip()

            elapsed = (time.time_ns() / 1_000_000_000 - begin)
            waiting_time = (1 / self.__fps) - elapsed
            if(waiting_time > 0):
                time.sleep(waiting_time)

    def update(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.is_active = False

        # ----- PACKET HANDLING -------
        while(len(self.client.buffer) > 0):
            raw = self.client.buffer[0]
            packet = json.loads(raw[0].decode())

            if(packet["type"] == "profile_transfert_packet"):
                if(packet["authorized"]):
                    self.client.profile = player_profile.deserialize(packet["profile"])
                else:
                    self.logger.log(packet["message"], subject="refused")
                    self.abort = True
                    self.is_active = False

            elif(packet["type"] == "player_transfert_packet"):
                self.client.set_player(player.Player().deserialize(packet["player"]))
                self.logger.log("player entity received", subject="load")

            elif(packet["type"] == "world_transfert_packet"):
                self.client.set_world(world.World().deserialize(packet["world"]))
                self.logger.log("world received", subject="load")

                self.client.get_world().set_local_player(self.client.get_player())
                self.client.get_world_updater().local_player = self.client.get_player()
                self.client.get_entity_updater().local_player = self.client.get_player()
                self.logger.log("world player linked with local player entity", subject="load")
                self.is_active = False


            self.client.buffer = self.client.buffer[1:]
        # -----------------------------

        self.test.check()

    def render(self):
        # self.__screen.blit(self.test.render(), (self.test.x, self.test.y))
        self.__screen.blit(self.client.texture_handler.get_texture("textures/gui/launcher/loading/loading_tree_6.png", size_coef = 10), (0, 0))
        # self.__screen.blit(self.client.texture_handler.get_texture("textures/launcher/loading/loading_tree_6.png", size_coef = 2), (3*128, 0))
        # self.__screen.blit(self.client.texture_handler.get_texture("textures/launcher/loading/loading_tree_6.png", size_coef = 1), (5*128, 0))

    def trigger_button(self, click_type):
        print(click_type)
