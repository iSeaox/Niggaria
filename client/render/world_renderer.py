import client.render.entity_renderer as entity_renderer

BLOCK_WIDTH = 32

def render_world(screen, world, view, texture_handler):
    screen_size = screen.get_size()
    # RENDER OF ENTITIES
    for entity in world.entities.values():
        entity_renderer.render_entity(screen, entity, view, texture_handler)

    # RENDER OF BLOCKS and MAP
    for chunk in world.chunks:
        for block in chunk.blocks:
            real_x = (block.x - view[0]) * BLOCK_WIDTH
            real_y = screen_size[1] - (block.y - view[1]) * BLOCK_WIDTH

            screen.blit(texture_handler.get_texture(block.__module__), (real_x, real_y))
