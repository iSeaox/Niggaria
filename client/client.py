import socket
import time
import json
import pygame
import queue

from server.server import SERVER_TPS

import network.net_listener as net_listener
import network.tcp_pipeline as tcp_pipeline

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

import world.world as world


CLIENT_FPS = 60

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

class Client:
    def __init__(self, server_access, logger):

        self.debug_map_gen = True

        self.__run = False
        self.__fps = CLIENT_FPS
        self.__tps = SERVER_TPS
        self.__player = None
        self.__world = None


        self.__entity_updater = entity_updater.EntityUpdater()
        self.__world_updater = world_updater.WorldUpdater(self.__entity_updater)

        self.__loading = True
        self.profile = None

        self.__actions_buffer = []
        self.__key_buffer = {0: False, 1: False, 2: False}

        self.server_access = server_access
        self.logger = logger
        self.__net_buffer_size = 1024 * 256


        self.buffer = []
        self.tcp_queue = queue.Queue(maxsize=0)

        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.net_listener = net_listener.NetListener(self)

        self.tcp_pipeline = tcp_pipeline.TCPPipelineClient(self.logger, self.tcp_queue, ("localhost", 20002), self, debug=True)

        self.texture_handler = texture_handler.TextureHandler(self.logger)
        self.__launcher = launcher.Launcher(self)

        self.view = None


    def start(self):
        self.__run = True

        pygame.init()

        screen_info = pygame.display.Info()
        self.logger.log("the screen size is "+ str(screen_info.current_w) +":"+ str(screen_info.current_h), subject="info")

        screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
        pygame.display.set_caption("Niggaria")

        self.texture_handler.load_textures(part="gui")
        self.__launcher.start(screen)
        self.view = view_handler.View((0, 17), self.__player, screen.get_size(), 2, self.__world.size)
        fpt = self.__fps / self.__tps
        tick_counter = 0
        tick = 0

        while(self.__run):
            begin = time.time_ns() / 1_000_000_000

            if(not(tick_counter % fpt)):
                tick_counter = 0
                tick += 1
                tick %= self.__tps
                self.tick()

            tick_counter += 1

            self.update(tick, fpt)
            self.render(screen)
            pygame.display.flip()

            elapsed = (time.time_ns() / 1_000_000_000) - begin
            waiting_time = (1 / self.__fps) - elapsed
            if(waiting_time > 0):
                sleep(waiting_time)

        raw_packet = quit_packet.QuitPacket(self.profile).serialize()
        self.__socket.sendto(str.encode(raw_packet), self.server_access)

    def update(self, tick, fpt):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.__run = False
            elif(event.type == pygame.KEYDOWN):
                if(event.key == 100):
                    self.__key_buffer[key_action.KEY_RIGHT] = True

                    new_action = key_action.KeyAction(key_action.KEY_RIGHT, key_action.ACTION_DOWN)
                    self.__entity_updater.push_local_action(new_action)
                    raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                    self.__socket.sendto(str.encode(raw_packet), self.server_access)

                elif(event.key == 113):
                    self.__key_buffer[key_action.KEY_LEFT] = True

                    new_action = key_action.KeyAction(key_action.KEY_LEFT, key_action.ACTION_DOWN)
                    self.__entity_updater.push_local_action(new_action)
                    raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                    self.__socket.sendto(str.encode(raw_packet), self.server_access)

                # elif(event.key == 32):
                #     self.__key_buffer[key_action.KEY_JUMP] = True
                #     if(self.__player.predicted_y == 25):
                #         pass
                #         self.__player.velocity[1] = 0.9
                #
                #     new_action = key_action.KeyAction(key_action.KEY_JUMP, key_action.ACTION_DOWN)
                #     raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                #     self.__socket.sendto(str.encode(raw_packet), self.server_acces)

            elif(event.type == pygame.KEYUP):
                if(event.key == 100):
                    self.__key_buffer[key_action.KEY_RIGHT] = False

                    new_action = key_action.KeyAction(key_action.KEY_RIGHT, key_action.ACTION_UP)
                    self.__entity_updater.push_local_action(new_action)
                    raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                    self.__socket.sendto(str.encode(raw_packet), self.server_access)

                elif(event.key == 113):
                    self.__key_buffer[key_action.KEY_LEFT] = False
                    new_action = key_action.KeyAction(key_action.KEY_LEFT, key_action.ACTION_UP)
                    self.__entity_updater.push_local_action(new_action)
                    raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                    self.__socket.sendto(str.encode(raw_packet), self.server_access)

                # elif(event.key == 32):
                #     self.__key_buffer[key_action.KEY_JUMP] = False
                #
                #     new_action = key_action.KeyAction(key_action.KEY_JUMP, key_action.ACTION_UP)
                #     self.__entity_updater.push_local_action(new_action)
                #     raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                #     self.__socket.sendto(str.encode(raw_packet), self.server_acces)

        if(self.debug_map_gen):
            speed = 2
            if(pygame.key.get_pressed()[1073741903]):
                self.view.pos = (self.view.pos[0] + speed, self.view.pos[1])
            elif(pygame.key.get_pressed()[1073741904]):
                self.view.pos = (self.view.pos[0] - speed, self.view.pos[1])
            elif(pygame.key.get_pressed()[1073741905]):
                self.view.pos = (self.view.pos[0], self.view.pos[1] - speed)
            elif(pygame.key.get_pressed()[1073741906]):
                self.view.pos = (self.view.pos[0], self.view.pos[1] + speed)

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
                    if(em_action.entity.uuid == self.__player.uuid):
                        self.__entity_updater.push_local_action(em_action)
                    else:
                        self.__entity_updater.push_action(em_action.entity, em_action)

            self.buffer = self.buffer[1:]
        # -------------------------------------

        self.__world_updater.update(self.__world, tick, fpt)

        if(not(self.debug_map_gen)):
            self.view.check()
        else:
            cur_pos = self.view.pos
            self.view.pos = (cur_pos[0] % (self.view.world_size * world.CHUNK_WIDTH), cur_pos[1])

    def tick(self):
        GRAVITY_INTENSITY = 0.13
        player = self.__player

        if(player.predicted_y >= 25):
            player.velocity[1] -= GRAVITY_INTENSITY

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
