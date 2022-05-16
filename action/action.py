import time

import utils.serializable as serializable


class Action(serializable.Serializable):
    def __init__(self):
        self.type = "abstract_action"
        self.timestamp = time.time_ns()
