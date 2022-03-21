import socket
import time
import pygame

import network.net_listener as net_listener

import entity.human.player as player

class Client:
    def __init__(self, server_acces, logger):
        self.__run = False
        self.__fps = 10
        self.__player = player.Player()

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

        self.__socket.sendto(str.encode("HelloEvent"), self.server_acces)
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

    def update(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.__run = False
            elif(event.type == pygame.KEYDOWN):
                if(event.key == 100):
                    self.__actions_buffer.append((time.time_ns(), "R"))
                    self.__socket.sendto(str.encode("MR,"+str(time.time_ns())), self.server_acces)

        if(len(self.buffer) > 0):
            print(self.buffer)
            
        for packet in self.buffer:
            data = packet[0].decode().split(",")
            self.__player.x = int(data[0])
            self.__player.y = int(data[1])

            while(len(self.__actions_buffer) > 0 and self.__actions_buffer[0][0] <= int(data[2])):
                self.__actions_buffer = self.__actions_buffer[1:]

        self.buffer = self.buffer[1:]

        self.__player.predicted_x = self.__player.x
        self.__player.predicted_y = self.__player.y

        for action in self.__actions_buffer:
            if(action[1] == "R"):
                self.__player.predicted_x += 5

    def render(self, screen):
        screen.fill((0, 0, 0))

        s_player = pygame.Surface((50, 50))
        s_player.fill((0xA0, 0xA0, 0xA0))
        screen.blit(s_player, (self.__player.predicted_x, self.__player.predicted_y))

    def get_socket(self):
        return self.__socket

    def get_net_buffer_size(self):
        return self.__net_buffer_size
