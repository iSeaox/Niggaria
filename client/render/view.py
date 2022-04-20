import math

class View:

    def __init__(self, pos, followed_entity, screen_size, bound = (0.45, 0.55)):
        self.pos = pos
        self.followed_entity = followed_entity
        self.screen_size = screen_size
        self.bound = bound
        self.last_pos_entity = ()
        self.block_width = 32

    def convert_postion(self, e_pos):
        real_x = (e_pos[0] - self.pos[0]) * self.block_width
        real_y = self.screen_size[1] - (e_pos[1] - self.pos[1]) * self.block_width

        return (real_x, real_y)

    def check(self):
        real_left_bound = self.bound[0] * self.screen_size[0]
        real_right_bound = self.bound[1] * self.screen_size[0]

        if(self.last_pos_entity != ()):
            delta_x_lb = (self.last_pos_entity[0] - real_left_bound) / self.block_width
            delta_x_rb = (self.last_pos_entity[0] - real_right_bound) / self.block_width

            if(delta_x_lb < 0):
                self.pos = (self.pos[0] - abs(delta_x_lb), self.pos[1])

            elif(delta_x_rb > 0):
                self.pos = (self.pos[0] + delta_x_rb, self.pos[1])
