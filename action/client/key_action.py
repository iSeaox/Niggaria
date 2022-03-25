import action.action as action

KEY_RIGHT = 0

class KeyAction(action.Action):

    def __init__(self, key = None):
        super().__init__()
        self.type = "key_action"

        self.key = key
