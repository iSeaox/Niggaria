import pygame
import time
import json

import utils.serializable as serializable

import client.packet.init_packet as init_packet
import client.gui.clickable.button as gui_button
import client.gui.clickable.clickable as clickable
import client.gui.clickable.text_field as text_field
import client.gui.loading_bar as load_bar

import network.net_preprocessor as net_preprocessor

import security.player_profile as player_profile
import security.profile_handler as profile_handler


TIMEOUT = 5  # time out pour la response server


class Launcher:
    def __init__(self, client, screen=None):
        self.client = client
        self.__screen = screen
        self.__fps = 30
        self.is_active = False
        self.abort = False
        self.logger = self.client.logger

        self.valid_button = gui_button.Button(10, 400, self.trigger_button, label="Jouer", padding_top=10, padding_side=20)
        self.t_field = text_field.TextField(50, 300, 200, 30, placeholder="Username")
        self.t_field_pass = text_field.TextField(50, 350, 200, 30, placeholder="Password", password=True)

        self.text_fields = []
        self.text_fields.append(self.t_field)
        self.text_fields.append(self.t_field_pass)

        self.loading_bar = load_bar.LoadingBar(10, 600)

        self.waiting_response = False
        self.server_response = None

        self.partial_packets = {}

    def start(self, screen):
        self.__screen = screen
        self.is_active = True

        while self.is_active:
            begin = time.time_ns() / 1_000_000_000

            self.update()
            self.render()
            pygame.display.flip()

            elapsed = (time.time_ns() / 1_000_000_000 - begin)
            waiting_time = (1 / self.__fps) - elapsed
            if waiting_time > 0:
                time.sleep(waiting_time)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_active = False
            elif event.type == pygame.KEYDOWN:
                self.t_field.trigger_key_down_event(event)
                self.t_field_pass.trigger_key_down_event(event)

                if event.key == 13:  # ENTER
                    self.valid_button.click(clickable.RIGHT_CLICK)
                elif event.key == 9:  # TAB
                    focused_id = None
                    for i in range(len(self.text_fields)):
                        if self.text_fields[i].is_focus:
                            focused_id = i
                    if focused_id is not None:
                        self.text_fields[focused_id].is_focus = False
                        self.text_fields[(focused_id + 1) % len(self.text_fields)].is_focus = True

        packets = net_preprocessor.gen_packet_list(self.client.tcp_queue)
        for r_packet in packets:

            packet = json.loads(r_packet[1])
            if packet["type"] == "profile_transfert_packet":
                if packet["authorized"]:
                    self.client.profile = player_profile.deserialize(packet["profile"])
                else:
                    self.logger.log(packet["message"], subject="refused")
                    self.server_response = packet["message"]
                    self.waiting_response = False

            elif packet["type"] == "player_transfert_packet":
                self.client.set_player(serializable.deserialize(packet["player"]))
                self.logger.log("player entity received", subject="load")

            elif packet["type"] == "world_transfert_packet":
                world = serializable.deserialize(packet["world"])
                world.chunks = [0] * world.size

                self.client.set_world(world)
                self.logger.log("------------- WORLD -------------")
                self.logger.log("world received", subject="load")

                self.client.get_world().set_local_player(self.client.get_player())
                self.client.get_world_updater().local_player = self.client.get_player()
                self.client.get_entity_updater().local_player = self.client.get_player()
                self.logger.log("world player linked with local player entity", subject="load")

            elif packet["type"] == "chunk_transfert_packet":
                chunk = serializable.deserialize(packet["chunk"])
                self.client.get_world().chunks[int(packet["id"])] = chunk
                self.logger.log("chunk number " + str(packet["id"] + 1) + "/" + str(self.client.get_world().size) + " received", subject="load")
                self.loading_bar.value = (packet["id"] + 1) / self.client.get_world().size

                if int(packet["id"]) == self.client.get_world().size - 1:
                    self.logger.log("---------------------------------")
                    self.client.texture_handler.load_textures(part="block")
                    self.client.texture_handler.load_textures(part="")
                    self.is_active = False
        # -----------------------------

        self.valid_button.check()
        for tf in self.text_fields:
            tf.check()

    def trigger_button(self, click_type):
        if not self.waiting_response:
            self.waiting_response = True
            if not(self.client.tcp_pipeline.is_alive()):
                self.client.tcp_pipeline.start()

            if self.client.tcp_pipeline.ready_event.wait(TIMEOUT):  # on attend que le thread de liaison tcp soit prêt

                packet_data = init_packet.InitPacket(self.t_field.content, self.t_field_pass.content).serialize()
                self.client.send_tcp_packet(str.encode(packet_data))

            else:
                print("SERVER NOT FOUND")

    def render(self):
        mid = pygame.display.get_surface().get_width() // 2

        if not self.waiting_response:
            self.__screen.fill((0, 0, 0))

            self.__screen.blit(self.client.texture_handler.loaded["gui.launcher.loading_tree"][5], (256, 256))
            s_valid_button = self.valid_button.render(self.client.texture_handler)
            if self.waiting_response:
                s_valid_button.set_alpha(100)
            self.valid_button.x = mid - (self.valid_button.width // 2)
            self.__screen.blit(s_valid_button, (self.valid_button.x, self.valid_button.y))

            for tf in self.text_fields:
                tf.x = mid - (tf.width // 2)
                self.__screen.blit(tf.render(self.client.texture_handler), (tf.x, tf.y))

            if self.server_response is not None:
                resp_code = self.server_response.split(":")[0]
                if resp_code == profile_handler.WRONG_PASSWORD_CODE:
                    s_cross = self.client.texture_handler.get_texture("gui.launcher.icons.red_cross")
                    self.__screen.blit(self.client.texture_handler.resize(s_cross, size_coef=2), (self.t_field_pass.x + self.t_field_pass.width + 10, self.t_field_pass.y + 3))

                elif resp_code == profile_handler.PROFILE_NOT_FOUND_CODE:
                    s_cross = self.client.texture_handler.get_texture("gui.launcher.icons.red_cross")
                    self.__screen.blit(self.client.texture_handler.resize(s_cross, size_coef=2), (self.t_field.x + self.t_field.width + 10, self.t_field.y + 3))
        else:
            self.__screen.fill((0, 0, 0))

            s_bar = self.client.texture_handler.resize(self.loading_bar.render(self.client.texture_handler), size_coef=3)
            self.loading_bar.x = mid - (s_bar.get_width() // 2)
            self.__screen.blit(s_bar, (self.loading_bar.x, self.loading_bar.y))

            tree_variant = round(self.loading_bar.value * 4)
            s_tree = self.client.texture_handler.get_texture("gui.launcher.loading_tree", variant=tree_variant)
            self.__screen.blit(s_tree, (mid - (s_tree.get_width() // 2), 256))

    def get_fps(self):
        return self.__fps
