import block.block as block

PROPERTY_SIMPLE = 0x8000_0000

PROPERTY_SIDE_NUMBER_SH = 29
PROPERTY_SIDE_LEFT = 0x2000_0000
PROPERTY_SIDE_RIGHT = 0x4000_0000
PROPERTY_SIDE_MID = 0x6000_0000
PROPERTY_BOTH_SIDE = 0x0

PROPERTY_HEIGHT_MASK = 0x1800_0000
PROPERTY_HEIGHT_TOP = 0x800_0000
PROPERTY_HEIGHT_DOWN = 0x1000_0000
PROPERTY_HEIGHT_CENTER = 0x0

PROPERTY_GRASS = 0x400_0000

PROPERTY_CORNER_ADJUST_LEFT = 0x100_0000
PROPERTY_CORNER_ADJUST_RIGHT = 0x200_0000
PROPERTY_CORNER_ADJUST_BOTH = 0x300_0000


class Dirt(block.Block):
    # Property:

    #     | Simple (1 bit) | Side (2 bit) | Height (2 bit) |  Grass (1 bit) | Corner_adjust (2 bit) |
    #
    #   Side -> 1 = left, 2 = right, 3 = mid
    #   Height -> 1 = top, 2 = down, 0 = center
    #   Corner_adjust -> 1 = left, 2 = right, 3 = both
    def __init__(self, x=None, y=None, property=0):
        super().__init__(x, y, "dirt", property, 0)
        self.id = block.DIRT_BLOCK

    def set_property(self, b_up, b_down, b_left, b_right, b_up_right, b_up_left):
        self.property = 0

        if b_up.type == self.type:
            if b_down.type == self.type:
                self.property |= PROPERTY_HEIGHT_CENTER
            else:
                self.property |= PROPERTY_HEIGHT_DOWN

        else:
            if b_down.type == self.type:
                self.property |= PROPERTY_HEIGHT_TOP
                self.property |= PROPERTY_GRASS

            else:
                self.property |= PROPERTY_GRASS
                self.property |= PROPERTY_SIMPLE

        if b_right.type == self.type:
            if b_left.type == self.type:
                self.property |= PROPERTY_SIDE_MID
            else:
                self.property |= PROPERTY_SIDE_LEFT

        else:
            if b_left.type == self.type:
                self.property |= PROPERTY_SIDE_RIGHT
            else:
                self.property |= PROPERTY_BOTH_SIDE

        if self.property & PROPERTY_SIDE_MID == PROPERTY_SIDE_MID and self.property & PROPERTY_HEIGHT_MASK == 0:
            if b_up_right.type != self.type:
                if b_up_left.type != self.type:
                    self.property |= PROPERTY_CORNER_ADJUST_BOTH
                else:
                    self.property |= PROPERTY_CORNER_ADJUST_RIGHT
            else:
                if b_up_left.type != self.type:
                    self.property |= PROPERTY_CORNER_ADJUST_LEFT

    def is_solid(self):
        return True
