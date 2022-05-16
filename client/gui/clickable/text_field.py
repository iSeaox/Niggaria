import pygame

import client.gui.clickable.clickable as clickable

import client.gui.text_renderer as text_renderer

class TextField(clickable.ClickableContent):
    def __init__(self, x, y, width, height, placeholder = "", password = False):
        super().__init__(x, y, width, height)

        self.is_focus = False
        self.is_password = password

        self.content = ""
        self.placeholder = placeholder
        self.focus_bar_tick = 0

        self.__permited_character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

    def render(self, texture_handler):
        if(self.content == ""):
            s_content = text_renderer.render_text(self.placeholder, texture_handler, size=1)
            s_content.set_alpha(100)
        elif(self.is_password):
            temp = ""
            for i in self.content:
                temp += "*"
            s_content = text_renderer.render_text(temp, texture_handler, size=1)
        else:
            s_content = text_renderer.render_text(self.content, texture_handler, size=1)

        padding_left = 10
        l_fps = 30

        s_textfield = pygame.Surface((self.width, self.height))
        s_textfield.blit(s_content, (padding_left, (self.height // 2) - (s_content.get_height() // 2)))
        if(self.is_focus and self.focus_bar_tick % l_fps <= (l_fps // 2)):
            s_focus_bar = text_renderer.render_text("|", texture_handler)
            if(self.content != ""):
                left_offset = padding_left + s_content.get_width()
            else:
                left_offset = padding_left
            s_textfield.blit(s_focus_bar, (left_offset, (self.height // 2) - (s_content.get_height() // 2)))
        pygame.draw.rect(s_textfield, (255, 255, 255), (0, 0, s_textfield.get_width(), s_textfield.get_height()), border_radius=3, width = 2)

        return s_textfield

    def check(self):
        super().check()
        self.focus_bar_tick += 1

        pressed_click = pygame.mouse.get_pressed()
        if(pressed_click[0] or pressed_click[2]):
            if(not(self.is_active)):
                self.is_focus = False
            else:
                self.is_focus = True

    def trigger_key_down_event(self, event):
        if(self.is_focus):
            if(event.key == 8):
                if(len(self.content) >= 1):
                    self.content = self.content[:-1]
            elif(event.unicode in self.__permited_character):
                self.content += event.unicode
