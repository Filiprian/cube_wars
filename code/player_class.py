import pygame

def player_movement(key, move_speed, player, wall_collision):
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        player.move_ip(-move_speed, 0)
    elif key[pygame.K_w] or key[pygame.K_UP]:
        player.move_ip(0, -move_speed)
    elif (key[pygame.K_d] or key[pygame.K_RIGHT]) and not wall_collision:
        player.move_ip(move_speed, 0)
    elif key[pygame.K_s] or key[pygame.K_DOWN]:
        player.move_ip(0, move_speed)