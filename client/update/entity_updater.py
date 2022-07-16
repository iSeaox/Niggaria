import time

import action.client.key_action as key_action

from pygame import Vector2

import utils.clock as clock

from server.server import SERVER_TPS

from world.world import CHUNK_WIDTH

TPS_TIME = (1 / SERVER_TPS) * 1_000_000_000


class EntityUpdater:
    def __init__(self, client_fps):
        self.buffers = {}
        self.clock = clock.Clock()
        self.__fps = client_fps

        self.local_player = None
        self.last_timestamp = None

    def update(self, world):
        timestep = self.clock.time_step()
        # self.local_player.acceleration += Vector2(0, -0.001) * (timestep / (1_000_000_000 / SERVER_TPS))
        self.local_player.velocity += self.local_player.acceleration
        self.local_player.acceleration = Vector2(0, 0)
        self.local_player.position += self.local_player.velocity * (timestep / (1_000_000_000 / SERVER_TPS))

        self.local_player.position.x %= world.size * CHUNK_WIDTH

        for entity_uid in world.entities.keys():
            if entity_uid != self.local_player.instance_uid:

                concerned_entity = world.entities[entity_uid]

                if entity_uid in self.buffers.keys():
                    interpolate_timestamp = time.time_ns() - TPS_TIME
                    working_buffer = self.buffers[entity_uid]
                    delta_x_max = 10  # pour ne pas faire d'interpolation pendant les téléportations entre autre
                    previous_pos = ()
                    previous_timestamp = None
                    next_pos = ()
                    next_timestamp = None

                    i = 0
                    while i < len(working_buffer) and working_buffer[i][0] <= interpolate_timestamp:
                        previous_pos = (working_buffer[i][1].entity.position.x, working_buffer[i][1].entity.position.y)
                        previous_timestamp = working_buffer[i][0]
                        i += 1

                    i = len(working_buffer) - 1
                    while i >= 0 and working_buffer[i][0] >= interpolate_timestamp:
                        next_pos = (working_buffer[i][1].entity.position.x, working_buffer[i][1].entity.position.y)
                        next_timestamp = working_buffer[i][0]
                        i -= 1
                    if previous_pos != () and next_pos != ():
                        dist_x = (next_pos[0] - previous_pos[0])
                        delta_t = next_timestamp - previous_timestamp
                        if delta_t == 0:
                            print(f'ARRGHH HEIN ERREUR : delta_t dans entity_updater vaut 0 -> {next_timestamp}, {previous_timestamp}')
                            continue

                        delta_x = (interpolate_timestamp - previous_timestamp) * dist_x / delta_t
                        if delta_x < delta_x_max:
                            concerned_entity.position.x = previous_pos[0] + delta_x
                    elif previous_pos != () and next_pos == ():
                        concerned_entity.position.x = previous_pos[0]

                    while len(self.buffers[entity_uid]) > 0 and time.time_ns() - self.buffers[entity_uid][0][0] > TPS_TIME * 2:
                        self.buffers[entity_uid] = self.buffers[entity_uid][1:]

    def push_local_action(self, action):
        if action.type == "entity_move_action":
            if action.timestamp == self.last_timestamp:
                print(f'SELF : {self.local_player.position.x} {self.local_player.position.y}')
                print(f'ACTUAL : {action.entity.position.x} {action.entity.position.y}')
                self.local_player.position = action.entity.position
        else:
            if action.type == "key_action":
                if action.action == key_action.ACTION_DOWN:
                    if action.key == key_action.KEY_RIGHT:
                        self.local_player.acceleration += Vector2(1, 0)
                    elif action.key == key_action.KEY_LEFT:
                        self.local_player.acceleration += Vector2(-1, 0)
                    elif action.key == key_action.KEY_JUMP:
                        self.local_player.acceleration += Vector2(0, 0.01)
                elif action.action == key_action.ACTION_UP:
                    if action.key == key_action.KEY_RIGHT:
                        self.local_player.acceleration += Vector2(-1, 0)
                    elif action.key == key_action.KEY_LEFT:
                        self.local_player.acceleration += Vector2(1, 0)

    def push_action(self, entity, action):
        if not(entity.instance_uid in self.buffers.keys()):
            self.buffers[entity.instance_uid] = []
        self.buffers[entity.instance_uid].append((self.clock.get_time(), action))
        # print(f'OTHER : {action.entity.position.x} SELF : {self.local_player.position.x}')
