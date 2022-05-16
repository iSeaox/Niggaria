import entity.entity as entity


NAME_SIZE = 25


class Player(entity.Entity):
    def __init__(self, uuid=None, name=None):
        super().__init__()

        self.type = "player"
        self.id = entity.PLAYER_ENTITY
        self.uuid = uuid
        self.name = name  # max 25 caractère

    def to_bytes(self):

        # | entity_bytes... | uuid (36 bytes) | name (25 bytes)
        content = super().to_bytes()
        content += str.encode(self.uuid)
        content += str.encode(self.name) + b'\x00' * (NAME_SIZE - len(self.name))

        return content
