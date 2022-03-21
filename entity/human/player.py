import entity.entity as entity

class Player(entity.Entity):
    def __init__(self):
        super().__init__()
        self.x = 20
        self.y = 100
