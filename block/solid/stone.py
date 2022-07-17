import block.block as block

PROPERTY_SIMPLE = 0x8000_0000

PROPERTY_SIDE_LEFT = 0x2000_0000
PROPERTY_SIDE_RIGHT = 0x4000_0000
PROPERTY_SIDE_MID = 0x6000_0000
PROPERTY_BOTH_SIDE = 0x0

PROPERTY_BOTH_HEIGHT = 0x1800_0000
PROPERTY_HEIGHT_TOP = 0x800_0000
PROPERTY_HEIGHT_DOWN = 0x1000_0000
PROPERTY_HEIGHT_CENTER = 0x0


class Stone(block.Block):
    # Property:

    #     | Simple (1 bit) | Side (2 bit) | Height (2 bit)
    #
    #   Side -> 1 = left, 2 = right, 3 = mid, 0 = both
    #   Height -> 1 = top, 2 = down, 0 = center, 3 = both

    def __init__(self, x=None, y=None, property=None):
        super().__init__(x, y, "stone", property, 0)

        self.id = block.STONE_BLOCK

    def set_property(self, b_up, b_down, b_left, b_right, b_up_right, b_up_left):
        self.property = 0
        simple_pass = 0

        if b_up.type == self.type:
            if b_down.type == self.type:
                self.property |= PROPERTY_HEIGHT_CENTER
            else:
                self.property |= PROPERTY_HEIGHT_DOWN
        else:
            if b_down.type == self.type:
                self.property |= PROPERTY_HEIGHT_TOP
            else:
                self.property |= PROPERTY_BOTH_HEIGHT
                simple_pass += 1

        if b_left.type == self.type:
            if b_right.type == self.type:
                self.property |= PROPERTY_SIDE_MID
            else:
                self.property |= PROPERTY_SIDE_RIGHT
        else:
            if b_right.type == self.type:
                self.property |= PROPERTY_SIDE_LEFT
            else:
                self.property |= PROPERTY_BOTH_SIDE
                simple_pass += 1

        if simple_pass == 2:
            self.property = PROPERTY_SIMPLE

    def is_solid(self):
        return True
