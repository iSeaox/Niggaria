import pygame


def render_text(text, texture_handler, size=1, charset="gui.text.FR_charset", inter_space=2, space=5):
    inter_space *= size
    space *= size
    characters = []
    width = 0
    height = 0
    for char in text:
        if char == " ":
            s_char = pygame.Surface((space, 1))
        else:
            s_char = texture_handler.get_texture("gui.text.FR_charset", charset_key=char)
            s_char = texture_handler.resize(s_char, size_coef=size)

        width += s_char.get_width() + inter_space
        if s_char.get_height() > height:
            height = s_char.get_height()
        characters.append(s_char)

    text_surface = pygame.Surface((width, height))
    cursor_x = 0
    for s_char in characters:
        text_surface.blit(s_char, (cursor_x, 0))
        cursor_x += s_char.get_width() + inter_space

    return text_surface
