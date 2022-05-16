import block.block as block


class Stone(block.Block):

    def __init__(self, x=None, y=None):
        super().__init__(x, y, "stone", 0)

        self.id = block.STONE_BLOCK
