import time

import action.client.key_action as key_action

from server.server import SERVER_TPS

TPS_TIME = (1 / SERVER_TPS) * 1_000_000_000

class EntityUpdater:

    def __init__(self):
        self.buffers = {}
        self.local_buffer = []
        self.local_player = None

    def update(self, entities):
        # ------- PLAYER WHO PLAY ON CLIENT --------
        self.local_player.predicted_x = self.local_player.x
        self.local_player.predicted_y = self.local_player.y

        for action in self.local_buffer:
            if(action.type == "key_action"):
                if(action.key == key_action.KEY_RIGHT):
                    self.local_player.predicted_x += 5
                elif(action.key == key_action.KEY_LEFT):
                    self.local_player.predicted_x -= 5
        # -------------------------------------------
        for entity_uid in entities.keys():
            if(entity_uid != self.local_player.instance_uid):

                concerned_entity = entities[entity_uid]

                if(entity_uid in self.buffers.keys()):
                    interpolate_timestamp = time.time_ns() - TPS_TIME
                    working_buffer = self.buffers[entity_uid]
                    previous_pos = ()
                    previous_timestamp = None
                    next_pos = ()
                    next_timestamp = None

                    i = 0
                    while(i < len(working_buffer) and working_buffer[i][0] <= interpolate_timestamp):
                        previous_pos = (working_buffer[i][1].new_x, working_buffer[i][1].new_y)
                        previous_timestamp = working_buffer[i][0]
                        i += 1

                    i = len(working_buffer) - 1
                    while(i >= 0 and working_buffer[i][0] >= interpolate_timestamp):
                        next_pos = (working_buffer[i][1].new_x, working_buffer[i][1].new_y)
                        next_timestamp = working_buffer[i][0]
                        i -= 1

                    if(previous_pos != () and next_pos != ()):
                        dist_x = (next_pos[0] - previous_pos[0])
                        delta_t = next_timestamp - previous_timestamp

                        # delta_x = (interpolate_timestamp - previous_timestamp) * dist_x / delta_t
                        delta_x = (next_pos[0] + previous_pos[0]) / 2
                        concerned_entity.x = round(delta_x)
                    elif(previous_pos != () and next_pos == ()):
                        concerned_entity.x = previous_pos[0]

                    print(previous_pos, next_pos)

                    while(len(self.buffers[entity_uid]) > 0 and time.time_ns() - self.buffers[entity_uid][0][0] > TPS_TIME * 4):
                        self.buffers[entity_uid] = self.buffers[entity_uid][1:]

                concerned_entity.predicted_x = concerned_entity.x
                concerned_entity.predicted_y = concerned_entity.y

    def push_local_action(self, action):
        if(action.type == "entity_move_action"):
            self.local_player.x = action.new_x
            self.local_player.y = action.new_y

            i = 0
            temp = []
            while(i < len(self.local_buffer)):
                if(self.local_buffer[i].type != "key_action" and self.local_buffer[i].timestamp > action.timestamp):
                    temp.append(self.local_buffer[i])
                i += 1
            self.local_buffer = temp
        else:
            self.local_buffer.append(action)


    def push_action(self, entity, action):
        if(not(entity.instance_uid in self.buffers.keys())):
            self.buffers[entity.instance_uid] = []
        self.buffers[entity.instance_uid].append((time.time_ns(), action))