import client.render.entity_renderer as entity_renderer

def render_world(screen, world):
    # RENDER OF ENTITIES
    for entity in world.entities.values():
        entity_renderer.render_entity(screen, entity)

    # RENDER OF BLOCKS and MAP
    for chunk in world.chunks:
        for block in chunk.blocks:
            pass
