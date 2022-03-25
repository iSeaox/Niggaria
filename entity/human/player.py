import entity.entity as entity

class Player(entity.Entity):
    def __init__(self, profile):
        super().__init__()
        self.x = 20
        self.y = 100

        self.profile = profile
