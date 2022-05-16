import client.render.entity_renderer as entity_renderer

from world.world import CHUNK_WIDTH


def render_world(screen, world, view, texture_handler):
    # RENDER OF ENTITIES
    for entity in world.entities.values():
        temp = entity_renderer.render_entity(screen, entity, view, texture_handler)
        if entity.instance_uid == view.followed_entity.instance_uid:
            view.last_pos_entity = temp

    # RENDER OF BLOCKS and MAP
    displayed_chunk = []
    center_chunk_x = round(view.pos[0] / CHUNK_WIDTH)
    for i in range(center_chunk_x - view.render_distance, center_chunk_x + view.render_distance + 1):
        displayed_chunk.append(world.get_chunk(i))

    for chunk in displayed_chunk:
        for block in chunk.blocks:
            if block != 0 and __is_visible(block, chunk, view, view.convert_position((block.x, block.y))):
                screen.blit(texture_handler.get_texture(block.__module__ + ":" + str(block.property), variant=block.variant), view.convert_position((block.x, block.y)))

def __is_visible(block, chunk, view, converted_pos):
    sx, sy = converted_pos
    if (0 - view.block_width) <= sy <= view.screen_size[1]:
        if (0 - view.block_width) <= sx <= view.screen_size[0]:

            return True

    return False
