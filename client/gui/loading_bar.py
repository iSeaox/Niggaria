from abc import ABC

import client.gui.content as content

NB_MAX_STEP = 62

class LoadingBar(content.Content):
    def __init__(self, x, y):
        super().__init__(x, y, 128, 16)
        self.value = 0  # in percentage

    def render(self, texture_handler):
        empty_bar = texture_handler.get_texture("gui.launcher.loading_bar.empty_bar").copy()
        current_step = round(NB_MAX_STEP * self.value)
        fill_step = texture_handler.get_texture("gui.launcher.loading_bar.fill_bar_step").copy()
        next_step = texture_handler.get_texture("gui.launcher.loading_bar.next_bar_step").copy()
        x = 0
        for x in range(current_step):
            empty_bar.blit(fill_step, (1 + x, 1))
        if current_step != NB_MAX_STEP:
            empty_bar.blit(next_step, (2 + x, 1))

        return empty_bar
