import pygame

def render_entity(screen, entity):
    if(entity.type == "player"):
        s_player = pygame.Surface((50, 50))
        s_player.fill((0xA0, 0xA0, 0xA0))

        pseudo_font = pygame.font.Font(None, 20)
        s_text = pseudo_font.render(entity.name + " | "+ entity.instance_uid, True, (0xA0, 0xA0, 0xA0))

        screen.blit(s_text, (entity.predicted_x, entity.predicted_y - 25))
        screen.blit(s_player, (entity.predicted_x, entity.predicted_y))
