import utils.serializable as serializable
import utils.uid_generator as uid_generator

class Entity(serializable.Serializable):
    def __init__(self):
        self.type = "abstract_entity"
        self.instance_uid = uid_generator.gen_uid(8)

        self.x = 0
        self.y = 0

        self.predicted_x = 0
        self.predicted_y = 0

        self.velocity = [0, 0]

    def add_velocity(vector):
        self.velocity[0] += vector[0]
        self.velocity[1] += vector[1]
