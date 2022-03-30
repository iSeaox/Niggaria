import pygame

def render_text(text, size = 1):
    image = pygame.image.load("textures/text/FR_charset.png").convert_alpha()
    for i in range(128):
        image.get_buffer().write(b'\xFF\xFF\xFF\x00', offset = i * 4)
    return image
