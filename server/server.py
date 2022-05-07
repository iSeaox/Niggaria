import socket
import json
import queue

import server.packet.profile_transfert_packet as profile_transfert_packet
import server.packet.player_transfert_packet as player_transfert_packet
import server.packet.action_transfert_packet as action_transfert_packet
import server.packet.world_transfert_packet as world_transfert_packet
import server.packet.chunk_transfert_packet as chunk_transfert_packet
import server.packet.connection_packet as connection_packet
import server.container.entity.human.server_player as server_player

import security.profile_handler as profile_handler

import network.udp_listener as udp_listener
import network.tcp_pipeline as tcp_pipeline
import network.net_preprocessor as net_preprocessor

import entity.human.player as player

import action.server.entity_move_action as entity_move_action
import action.client.key_action as key_action

import utils.clock as clock

import world.world as world


SERVER_TPS = 20


class Server:
    def __init__(self, ip_addr, port, logger):
        self.__run = False
        self.__tps = SERVER_TPS
        self.__ip_addr = ip_addr
        self.__port = port
        self.__clock = clock.Clock(SERVER_TPS)

        self.logger = logger

        self.__net_buffer_size = 4096
        self.buffer = []
        self.udp_queue = queue.Queue(maxsize=0)
        self.tcp_queue = queue.Queue(maxsize=0)

        self.__udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__udp_socket.bind((self.__ip_addr, self.__port))

        self.udp_listener = udp_listener.UDPListener(self.logger, self.__udp_socket, self.udp_queue)
        self.udp_listener.start()

        self.tcp_pipeline = tcp_pipeline.TCPPipeLineServer(self.logger, self.tcp_queue, self.connection_lost_handler, debug=True)
        self.tcp_pipeline.start()

        self.__connected_players = []
        self.__connected_players_data = {}
        self.__connected_players_OUTDATED = {}

        self.server_world = world.World()
        self.server_world.gen()

        # self.server_world.to_files(r'.\data\server\world')

    def start(self):
        self.__run = True
        while self.__run:
            self.__clock.start_tick()

            self.tick()

            self.__clock.tick()

    def tick(self):
        if len(self.buffer) > 0:
            print(self.buffer)
        # --------------------------- TCP Treatment -----------------------
        packets = net_preprocessor.gen_packet_list(self.tcp_queue)
        for r_packet in packets:
            tcp_access = r_packet[0]
            packet = json.loads(r_packet[1])
            if packet["type"] == "init_packet":
                (ath, msg, profile) = profile_handler.use_profile(packet["user"], packet["password"])
                if ath and self.get_server_player_by_uuid(profile.uuid):
                    (ath, msg, profile) = (False, profile_handler.ALREADY_CONNECTED_CODE + " | already connected", None)

                prt_packet = profile_transfert_packet.ProfileTransfertPacket(profile, msg, ath).serialize()
                temp_server_player = server_player.ServerPlayer(None, tcp_access, profile)
                self.send_tcp_packet(temp_server_player, str.encode(prt_packet))

                if ath:
                    new_player_entity = player.Player(profile.uuid, profile.user)
                    temp_server_player.player = new_player_entity
                    self.__connected_players.append(temp_server_player)
                    self.logger.log(temp_server_player.profile.user + " join the game", subject="join")

                    # ---- Joining Player Only ----
                    plt_packet = player_transfert_packet.PlayerTransfertPacket(new_player_entity).serialize()
                    self.send_tcp_packet(temp_server_player, str.encode(plt_packet))

                    wt_packet = world_transfert_packet.WorldTransfertPacket(self.server_world).serialize()
                    self.send_tcp_packet(temp_server_player, str.encode(wt_packet))

                    for i in range(self.server_world.size):
                        ct_packet = chunk_transfert_packet.ChunkTransfertPacket(chunk=self.server_world.chunks[i], id=i).serialize()
                        self.send_tcp_packet(temp_server_player, str.encode(ct_packet))

                    # ---- Others players ----
                    con_packet = connection_packet.ConnectionPacket(temp_server_player.player, connection_packet.JOIN_SERVER).serialize()
                    for spl in self.__connected_players:
                        if spl.profile.uuid != temp_server_player.profile.uuid:
                            self.send_tcp_packet(spl, str.encode(con_packet))

            elif packet["type"] == "quit_packet":
                concerned_server_player = self.get_server_player_by_uuid(packet["profile"]["uuid"])
                self.quit_player(concerned_server_player)

        # -------------------------- UDP Treatment -----------------------
        packets = net_preprocessor.gen_packet_list(self.udp_queue)
        for packet in packets:
            data = json.loads(packet[0].decode())

            if data["type"] == "sudpc_packet":
                self.get_server_player_by_uuid(data["uuid"]).udp_access = packet[1]

            if data["type"] == "action_transfert_packet":
                concerned_player = self.__connected_players_OUTDATED[data["uuid"]]["entity"]
                if data["action"]["type"] == "key_action":
                    pressed_key = data["action"]["key"]
                    if pressed_key == key_action.KEY_RIGHT:
                        if data['action']['action'] == key_action.ACTION_DOWN:
                            self.__connected_players_data[data['uuid']]['right'] = [True, data['timestamp']]
                        else:
                            time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['right'][1]
                            concerned_player.x += time_elapsed * (1.2 * 10 ** -8)

                            if self.__connected_players_data[data['uuid']]['left'][0]:
                                time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['left'][1]
                                concerned_player.x -= time_elapsed * (1.2 * 10 ** -8)
                                self.__connected_players_data[data['uuid']]['left'][1] = data['timestamp']

                            concerned_player.x %= self.server_world.size * world.CHUNK_WIDTH

                            em_action = entity_move_action.EntityMoveAction(concerned_player)
                            em_action.timestamp = data["timestamp"]
                            raw_packet = action_transfert_packet.ActionTransfertPacket(em_action, True).serialize()
                            self.__udp_socket.sendto(str.encode(raw_packet), packet[1])

                            self.__connected_players_data[data['uuid']]['right'][0] = False

                    elif pressed_key == key_action.KEY_LEFT:
                        if data['action']['action'] == key_action.ACTION_DOWN:
                            self.__connected_players_data[data['uuid']]['left'] = [True, data['timestamp']]
                        else:
                            if self.__connected_players_data[data['uuid']]['right'][0]:
                                time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['right'][1]
                                concerned_player.x += time_elapsed * (1.2 * 10 ** -8)
                                self.__connected_players_data[data['uuid']]['right'][1] = data['timestamp']

                            time_elapsed = data['timestamp'] - self.__connected_players_data[data['uuid']]['left'][1]
                            concerned_player.x -= time_elapsed * (1.2 * 10 ** -8)

                            concerned_player.x %= self.server_world.size * world.CHUNK_WIDTH

                            em_action = entity_move_action.EntityMoveAction(concerned_player)
                            em_action.timestamp = data["timestamp"]
                            raw_packet = action_transfert_packet.ActionTransfertPacket(em_action, True).serialize()
                            self.__udp_socket.sendto(str.encode(raw_packet), packet[1])

                            self.__connected_players_data[data['uuid']]['left'][0] = False

        for player_uuid in self.__connected_players_OUTDATED.keys():
            concerned_player = self.__connected_players_OUTDATED[player_uuid]['entity']

            if self.__connected_players_data[player_uuid]['right'][0]:
                time_elapsed = self.__clock.get_time() - self.__connected_players_data[player_uuid]['right'][1]
                concerned_player.x += time_elapsed * (1.2 * 10 ** -8)
                self.__connected_players_data[player_uuid]['right'][1] = self.__clock.get_time()

            if self.__connected_players_data[player_uuid]['left'][0]:
                time_elapsed = self.__clock.get_time() - self.__connected_players_data[player_uuid]['left'][1]
                concerned_player.x -= time_elapsed * (1.2 * 10 ** -8)
                self.__connected_players_data[player_uuid]['left'][1] = self.__clock.get_time()

            for other_player_uuid in self.__connected_players_OUTDATED.keys():
                if player_uuid != other_player_uuid:
                    em_action = entity_move_action.EntityMoveAction(self.__connected_players_OUTDATED[other_player_uuid]['entity'])
                    em_action.timestamp = self.__clock.get_time()
                    raw_packet = action_transfert_packet.ActionTransfertPacket(em_action).serialize()
                    self.__udp_socket.sendto(str.encode(raw_packet), self.__connected_players_OUTDATED[player_uuid]['access'])

    def send_udp_packet(self, server_player, packet):
        self.__udp_socket.sendto(packet, server_player.udp_access)

    def send_tcp_packet(self, server_player, packet):
        self.tcp_pipeline.send_packet(server_player, packet)

    def connection_lost_handler(self, tcp_name):
        concerned_player = self.get_server_player_by_tcpname(tcp_name)
        if concerned_player is not None:
            self.quit_player(concerned_player)

    def quit_player(self, serv_player):
        con_packet = connection_packet.ConnectionPacket(serv_player.player, connection_packet.QUIT_SERVER).serialize()
        self.__connected_players.remove(serv_player)
        self.logger.log(serv_player.profile.user + " left the game", subject="quit")
        for spl in self.__connected_players:
            self.tcp_pipeline.send_packet(spl, str.encode(con_packet))

    def get_socket(self):
        return self.__udp_socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size

    def get_server_player_by_uuid(self, uuid):
        for s_player in self.__connected_players:
            if s_player.profile.uuid == uuid:
                return s_player

    def get_server_player_by_tcpname(self, tcpname):
        for s_player in self.__connected_players:
            if s_player.tcp_access == tcpname:
                return s_player
