import action.action as action

KEY_RIGHT = 0
KEY_LEFT = 1
KEY_JUMP = 2

ACTION_UP = 0
ACTION_DOWN = 1


class KeyAction(action.Action):

    def __init__(self, key=None, action=None):
        super().__init__()
        self.type = "key_action"

        self.key = key
        self.action = action
