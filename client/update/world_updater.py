class WorldUpdater:
    def __init__(self, entity_updater):
        self.entity_updater = entity_updater
        self.local_player = None

        self.buffers = {}

    def update(self, world, tick, fpt):
        self.entity_updater.update(world.entities, tick, fpt)
