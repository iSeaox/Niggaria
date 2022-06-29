import block.block as block


class Air(block.Block):
    def __init__(self, x=None, y=None):
        super().__init__(x, y, "air", 0, 0)
        self.id = block.AIR_BLOCK

    def is_air(self):
        return True

    def is_solid(self):
        return False