import block.block as block

class Stone(block.Block):

    def __init__(self, x = None, y = None, nbt = None):
        super().__init__(x, y , "stone", nbt)
