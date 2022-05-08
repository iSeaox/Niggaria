import block.block as block


class Plant(block.Block):
    def __init__(self, x=None, y=None, property=0, variant=0):
        super().__init__(x, y, "plant", property, variant)

    def is_solid(self):
        return False
