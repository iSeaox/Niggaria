import action.action as action

JOIN_SERVER = 0
QUIT_SERVER = 1

class ConnectionAction(action.Action):

    def __init__(self, player = None, connection_type = None):
        self.type = "connection_action"

        self.player = player
        self.connection_type = connection_type
