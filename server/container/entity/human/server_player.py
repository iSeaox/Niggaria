class ServerPlayer:
    def __init__(self, player, tcp_access, profile):

        self.player = player

        self.tcp_access = tcp_access
        self.udp_access = None
        self.profile = profile
