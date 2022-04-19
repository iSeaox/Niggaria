import pygame
import math

BLOCK_WIDTH = 32

def render_entity(screen, entity, view, texture_handler):
    screen_size = screen.get_size()
    if(entity.type == "player"):
        s_player = pygame.Surface((50, 50))
        s_player.fill((0xA0, 0xA0, 0xA0))

        pseudo_font = pygame.font.Font(None, 20)
        s_text = pseudo_font.render(entity.name + " | "+ entity.instance_uid, True, (0xA0, 0xA0, 0xA0))

        real_x = (entity.predicted_x - view[0]) * BLOCK_WIDTH
        real_y = screen_size[1] - (entity.predicted_y - view[1]) * BLOCK_WIDTH

        if(real_x > 0):
            real_x = math.floor(real_x)
        elif(real_x < 0):
            real_x = math.ceil(real_x)

        if(real_y > 0):
            real_y = math.floor(real_y)
        elif(real_y < 0):
            real_y = math.ceil(real_y)

        screen.blit(s_text, (real_x, real_y - 25))
        screen.blit(s_player, (real_x, real_y))
