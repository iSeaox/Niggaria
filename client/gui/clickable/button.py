import pygame

import client.gui.clickable.clickable as clickable

import client.gui.text_renderer as text_renderer


class Button(clickable.ClickableContent):

    def __init__(self, x, y, trigger_method, label="", padding_top=5, padding_side=5):
        super().__init__(x, y, -1, -1)
        self.padding_top = padding_top
        self.padding_side = padding_side
        self.trigger_method = trigger_method
        self.label = label

    def click(self, click_type):
        self.trigger_method(click_type)

    def render(self, texture_handler):
        if self.label != "" and self.label is not None:
            s_label = text_renderer.render_text(self.label, texture_handler, size=1)
        else:
            s_label = pygame.Surface((1, 1))

        if self.width == -1 or self.height == -1:
            self.width = s_label.get_width() + (self.padding_side * 2)
            self.height = s_label.get_height() + (self.padding_top * 2)

        if self.is_hover:
            s_button = pygame.Surface((self.width + 6, self.height + 6))
            s_button.blit(s_label, (self.padding_side + 3, self.padding_top + 3))
        else:
            s_button = pygame.Surface((self.width, self.height))
            s_button.blit(s_label, (self.padding_side, self.padding_top))
        pygame.draw.rect(s_button, (255, 255, 255), (0, 0, s_button.get_width(), s_button.get_height()), border_radius=5, width=2)

        return s_button
