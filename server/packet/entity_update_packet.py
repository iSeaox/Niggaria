import network.packet.packet as packet

class EntityPositionUpdatePacket(packet.Packet):

    def __init__(self, entity, action_timestamp = None):
        super().__init__()
        self.side = packet.PACKET_SERVER
        self.type = "entity_position_update_packet"

        self.action_timestamp = action_timestamp
        self.entity_uid = entity.instance_uid
        self.entity_type = entity.type
        self.new_x = entity.x
        self.new_y = entity.y
