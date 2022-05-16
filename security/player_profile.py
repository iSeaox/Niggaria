class PlayerProfile:
    def __init__(self, user = None, password = None, uuid = None):
        self.user = user
        self.uuid = uuid
        self.password = password

    def serialize(self):
        return self.__dict__

def deserialize(raw_profile):
    return PlayerProfile(raw_profile["user"], raw_profile["password"], raw_profile["uuid"])
