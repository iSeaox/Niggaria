import pygame
import time
import json

import entity.human.player as player

import client.packet.init_packet as init_packet
import client.gui.clickable.button as gui_button
import client.gui.clickable.text_field as text_field
import client.gui.text_renderer as text_renderer

import security.player_profile as player_profile

import world.world as world

class Launcher:

    def __init__(self, client, screen = None):
        self.client = client
        self.__screen = screen
        self.__fps = 30
        self.is_active = False
        self.abort = False
        self.logger = self.client.logger

        self.test = gui_button.Button(10, 10, self.trigger_button, label = "Jouer", padding_top = 10, padding_side = 20)
        self.t_field = text_field.TextField(50, 50, 200, 30, placeholder="Username")
        self.t_field_pass = text_field.TextField(50, 100, 200, 30, placeholder="Password", password = True)

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
            elif(event.type == pygame.KEYDOWN):
                self.t_field.trigger_key_down_event(event)
                self.t_field_pass.trigger_key_down_event(event)

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
        self.t_field.check()
        self.t_field_pass.check()

    def render(self):
        self.__screen.fill((0, 0, 0))

        self.__screen.blit(self.client.texture_handler.loaded["gui.launcher.loading.loading_tree"][5], (256, 256))
        self.__screen.blit(self.test.render(self.client.texture_handler), (self.test.x, self.test.y))
        self.__screen.blit(self.t_field.render(self.client.texture_handler), (self.t_field.x, self.t_field.y))
        self.__screen.blit(self.t_field_pass.render(self.client.texture_handler), (self.t_field_pass.x, self.t_field_pass.y))

        s_cross = self.client.texture_handler.get_texture("gui.launcher.icons.red_cross")
        self.__screen.blit(self.client.texture_handler.resize(s_cross, size_coef = 2), (300, 100))

        s_mark = self.client.texture_handler.get_texture("gui.launcher.icons.check_mark")
        self.__screen.blit(self.client.texture_handler.resize(s_mark, size_coef = 2), (300, 80))

    def trigger_button(self, click_type):
        print(click_type)
