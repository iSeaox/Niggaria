import socket
import json
import pygame
import queue

from server.server import SERVER_TPS
import server.packet.connection_packet as connection_packet

import network.udp_listener as udp_listener
import network.tcp_pipeline as tcp_pipeline
import network.net_preprocessor as net_preprocessor

import utils.serializable as serializable
import utils.clock as clock

import client.packet.action_transfert_packet as action_transfert_packet
import client.packet.quit_packet as quit_packet
import client.packet.sudpc_packet as sudpc_packet

import client.render.world_renderer as world_renderer
import client.render.texture_handler as texture_handler
import client.render.view as view_handler

import client.update.entity_updater as entity_updater
import client.update.world_updater as world_updater

import client.launcher.launcher as launcher

import action.client.key_action as key_action

import world.world as world


CLIENT_FPS = 60


class Client:
    def __init__(self, server_access, logger):

        self.debug_map_gen = True

        self.__run = False
        self.__fps = CLIENT_FPS
        self.__tps = SERVER_TPS
        self.__player = None
        self.__world = None
        self.__clock = clock.Clock(self.__fps)

        self.__entity_updater = entity_updater.EntityUpdater(self.__fps)
        self.__world_updater = world_updater.WorldUpdater(self.__entity_updater)

        self.__loading = True
        self.profile = None

        self.__actions_buffer = []

        self.server_access = server_access
        self.logger = logger
        self.__net_buffer_size = 1024 * 256

        self.udp_queue = queue.Queue(maxsize=0)
        self.tcp_queue = queue.Queue(maxsize=0)

        self.__udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_listener = udp_listener.UDPListener(self.logger, self.__udp_socket, self.udp_queue)

        self.tcp_pipeline = tcp_pipeline.TCPPipelineClient(self.logger, self.tcp_queue, ("localhost", 20002), self, debug=False)

        self.texture_handler = texture_handler.TextureHandler(self.logger)
        self.__launcher = launcher.Launcher(self)

        self.view = None

    def start(self):
        self.__run = True

        pygame.init()

        screen_info = pygame.display.Info()
        self.logger.log("the screen size is " + str(screen_info.current_w) + ":" + str(screen_info.current_h), subject="info")

        screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
        pygame.display.set_caption("Niggaria")

        self.texture_handler.load_textures(part="gui")
        self.__launcher.start(screen)
        self.view = view_handler.View((0, 17), self.__player, screen.get_size(), 2, self.__world.size)
        self.init_udp()
        self.udp_listener.start()

        while self.__run:
            self.__clock.start_tick()

            self.update()
            self.render(screen)
            pygame.display.flip()

            self.__clock.tick()

        q_packet = quit_packet.QuitPacket(self.profile).serialize()
        self.send_tcp_packet(str.encode(q_packet))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False
            elif event.type == pygame.KEYDOWN:
                new_action = None
                if event.key == pygame.K_d:
                    new_action = key_action.KeyAction(key_action.KEY_RIGHT, key_action.ACTION_DOWN)
                elif event.key == pygame.K_q:
                    new_action = key_action.KeyAction(key_action.KEY_LEFT, key_action.ACTION_DOWN)
                elif event.key == pygame.K_SPACE:
                    new_action = key_action.KeyAction(key_action.KEY_JUMP, key_action.ACTION_DOWN)
                if new_action:
                    self.__entity_updater.push_local_action(new_action)
                    raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                    self.send_udp_packet(str.encode(raw_packet))
            elif event.type == pygame.KEYUP:
                new_action = None
                if event.key == pygame.K_d:
                    new_action = key_action.KeyAction(key_action.KEY_RIGHT, key_action.ACTION_UP)
                elif event.key == pygame.K_q:
                    new_action = key_action.KeyAction(key_action.KEY_LEFT, key_action.ACTION_UP)
                elif event.key == pygame.K_SPACE:
                    new_action = key_action.KeyAction(key_action.KEY_JUMP, key_action.ACTION_UP)
                if new_action:
                    self.__entity_updater.push_local_action(new_action)
                    raw_packet = action_transfert_packet.ActionTransfertPacket(new_action, self.profile).serialize()
                    self.send_udp_packet(str.encode(raw_packet))

        if self.debug_map_gen:
            speed = 2
            if pygame.key.get_pressed()[1073741903]:
                self.view.pos = (self.view.pos[0] + speed, self.view.pos[1])
            elif pygame.key.get_pressed()[1073741904]:
                self.view.pos = (self.view.pos[0] - speed, self.view.pos[1])
            elif pygame.key.get_pressed()[1073741905]:
                self.view.pos = (self.view.pos[0], self.view.pos[1] - speed)
            elif pygame.key.get_pressed()[1073741906]:
                self.view.pos = (self.view.pos[0], self.view.pos[1] + speed)

        packets = net_preprocessor.gen_packet_list(self.tcp_queue)
        for r_packet in packets:
            packet = json.loads(r_packet[1])
            if packet["type"] == "connection_packet":
                if packet["connection_type"] == connection_packet.JOIN_SERVER:
                    packet_player = serializable.deserialize(packet["player"])
                    self.__world.add_player_entity(packet_player)
                    self.logger.log(packet_player.name + " joined the game", subject="join")

                elif packet["connection_type"] == connection_packet.QUIT_SERVER:
                    packet_player = serializable.deserialize(packet["player"])
                    self.__world.remove_player_entity(packet_player)
                    self.logger.log(packet_player.name + " left the game", subject="quit")

        while not self.udp_queue.empty():
            raw = self.udp_queue.get()
            packet = json.loads(raw[0].decode())

            if packet["type"] == "action_transfert_packet":
                if packet["action"]["type"] == "entity_move_action":
                    em_action = serializable.deserialize(packet["action"])
                    if em_action.entity.uuid == self.__player.uuid:
                        self.__entity_updater.push_local_action(em_action)
                    else:
                        self.__entity_updater.push_action(em_action.entity, em_action)

        self.__world_updater.update(self.__world)

        if not self.debug_map_gen:
            self.view.check()
        else:
            cur_pos = self.view.pos
            self.view.pos = (cur_pos[0] % (self.view.world_size * world.CHUNK_WIDTH), cur_pos[1])

    def render(self, screen):
        screen.fill((0, 0, 0))
        world_renderer.render_world(screen, self.__world, self.view, self.texture_handler)

    def send_udp_packet(self, packet):
        self.__udp_socket.sendto(packet, self.server_access)

    def send_tcp_packet(self, packet):
        self.tcp_pipeline.send_packet(packet)

    def init_udp(self):
        pck = sudpc_packet.SUDPCPacket(self.profile.uuid).serialize()
        self.send_udp_packet(str.encode(pck))

    def get_socket(self):
        return self.__udp_socket

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
