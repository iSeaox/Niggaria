from math import ceil

import client.render.entity_renderer as entity_renderer

from world.world import CHUNK_WIDTH


def render_world(screen, world, view, texture_handler):
    # RENDER OF BLOCKS and MAP
    displayed_chunk = []
    center_chunk_x = ceil(view.pos[0] / CHUNK_WIDTH)
    for i in range(center_chunk_x - view.render_distance, center_chunk_x + view.render_distance + 1):
        displayed_chunk.append(world.get_chunk(i))

    for chunk in displayed_chunk:
        for block in chunk.blocks:
            if block != 0 and __is_visible(block, world, view, view.convert_position((block.x, block.y))):
                screen.blit(
                    texture_handler.get_texture(block.__module__ + ":" + str(block.property), variant=block.variant),
                    view.convert_position((block.x, block.y)))

    # RENDER OF ENTITIES
    for entity in world.entities.values():
        temp = entity_renderer.render_entity(screen, entity, view, texture_handler)
        print(temp)
        if entity.instance_uid == view.followed_entity.instance_uid:
            view.last_pos_entity = temp


def __is_visible(block, world, view, converted_pos):
    sx, sy = converted_pos
    if (0 - view.block_width) <= sy <= view.screen_size[1]:
        if (0 - view.block_width) <= sx <= view.screen_size[0]:
            # adj_block = __get_adjacent_blocks(block, world)
            #
            # for b in adj_block:
            #     if b == 0 or not b.is_solid():
            #         return True
            return True

    return False


def __get_adjacent_blocks(block, world, radius=5):
    temp = []
    bx = block.x
    by = block.y
    it_range = [i for i in range(-radius, radius + 1) if i != 0]

    for x_off in it_range:
        for y_off in it_range:
            sbx = (bx + x_off) % (world.size * CHUNK_WIDTH)
            sby = by + y_off

            if (sbx - bx) ** 2 + (sby - by) ** 2 <= radius ** 2:
                temp.append(world.get_block_at((sbx, sby)))
    return temp
