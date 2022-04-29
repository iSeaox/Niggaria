import block.block as block

MULTI_TOP = "multi_top_?"
MULTI_DOWN = "multi_down_?"
MULTI_RIGHT_CORNER_TOP = "multi_right_corner_top"
MULTI_RIGHT_CORNER_DOWN = "multi_right_corner_down"
MULTI_LEFT_CORNER_TOP = "multi_left_corner_top"
MULTI_LEFT_CORNER_DOWN = "multi_right_corner_top"

SIMPLE = "simple"
SIMPLE_GRASS = "simple_grass"
SIMPLE_MID = "simple_mid_?"
SIMPLE_RIGHT_CORNER = "simple_right_corner"
SIMPLE_LEFT_CORNER = "simple_left_corner"

CENTER = "center"

class Dirt(block.Block):

    def __init__(self, x = None, y = None, property = SIMPLE_GRASS):
        super().__init__(x, y, "dirt")

        self.id = block.DIRT_BLOCK
        self.property = property

    def set_property(self, type, value = 0):
        if("?" in type):
            self.property = type.replace("?", str(value))
        else:
            self.property = type
