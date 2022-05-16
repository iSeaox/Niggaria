from abc import ABC

import pygame

import client.gui.content as content

RIGHT_CLICK = 0
LEFT_CLICK = 1


class ClickableContent(content.Content, ABC):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.is_active = False
        self.is_hover = False

    def check(self):
        c_pos = pygame.mouse.get_pos()
        if self.x <= c_pos[0] <= (self.x + self.width) and self.y <= c_pos[1] <= (self.y + self.height):
            pressed_click = pygame.mouse.get_pressed()
            if pressed_click[0]:
                self.is_active = True
                self.is_hover = True
                self.click(LEFT_CLICK)
            elif pressed_click[2]:
                self.is_active = True
                self.is_hover = True
                self.click(RIGHT_CLICK)
            else:
                self.is_active = False
                self.is_hover = True
                self.hover()

        else:
            self.is_hover = False
            self.is_active = False

    def click(self, click_type):
        pass

    def hover(self):
        pass
