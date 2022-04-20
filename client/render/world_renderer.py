import client.render.entity_renderer as entity_renderer


def render_world(screen, world, view, texture_handler):
    # RENDER OF ENTITIES
    for entity in world.entities.values():
        temp = entity_renderer.render_entity(screen, entity, view, texture_handler)
        if(entity.instance_uid == view.followed_entity.instance_uid):
            view.last_pos_entity = temp

    # RENDER OF BLOCKS and MAP
    for chunk in world.chunks:
        for block in chunk.blocks:
            screen.blit(texture_handler.get_texture(block.__module__), view.convert_postion((block.x, block.y)))
