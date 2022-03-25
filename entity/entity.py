import utils.serializable as serializable

class Entity(serializable.Serializable):
    def __init__(self):
        self.type = "abstract_entity"

        self.x = 0
        self.y = 0

        self.predicted_x = 0
        self.predicted_y = 0
