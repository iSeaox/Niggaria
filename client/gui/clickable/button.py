import pygame

import client.gui.clickable.clickable as clickable

import client.gui.text_renderer as text_renderer

class Button(clickable.ClickableContent):

    def __init__(self, x, y, width, height, trigger_method, text = "", padding = 5, padding_top = 5, padding_side = 5):
        super().__init__(x, y, width, height)

        self.padding = padding
        self.padding_top = padding_top
        self.padding_down = padding_side

        self.trigger_method = trigger_method
        self.text = text

    def click(self, click_type):
        self.trigger_method(click_type)

    def render(self):
        return text_renderer.render_text("test : abcdefghij")
