import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)


class Walls():
    def __init__(self):
        self.cooldown = 0
        self.move = 0
        self.wall_active = False
        self.walls_active = False
        self.walls = random.choice(["upper wall", "downwards wall", "others"])
        self.wall = None
        self.wall1 = None
        self.wall2 = None
        self.wall_collision = False
        self.e_wall_collision = False
        self.g_wall_collision = False

    # Walls function
    def update(self, player, enemy, g_enemy, enemy_killcount, turret_active, upwall_size, downwall_size, wall1_size,
               wall2_size, screen, asteroid, asteroid_active, asteroid_death, game_over_sfx, rock_active, rift_active):
        # Creating walls
        self.cooldown += 1
        if self.cooldown >= 1200 and not (self.wall_active or self.walls_active or rock_active or turret_active or
                                          enemy_killcount > 17 or rift_active):
            walls = random.choice(["upper wall", "downwards wall", "others"])
            self.cooldown = 0
            if walls == "upper wall":
                self.wall = pygame.Rect(1220, 0, 8, upwall_size)
                self.wall_active = True
            elif walls == "downwards wall":
                self.wall = pygame.Rect(1220, downwall_size, 8, 590)
                self.wall_active = True
            else:
                self.wall1 = pygame.Rect(1220, 0, 8, wall1_size)
                self.wall2 = pygame.Rect(1220, wall2_size, 8, 400)
                self.walls_active = True

        # Up wall ---
        # Moving it
        if self.wall_active:
            pygame.draw.rect(screen, (225, 225, 225), self.wall)
            self.move += 1
            if self.move >= 1:
                self.wall.move_ip(-1.2, 0)
                self.move = 0
            if self.wall.left < 0:
                self.wall_active = False

            # Asteroid collision
            elif asteroid_active:
                if self.wall.colliderect(asteroid):
                    asteroid_death()

            # PLayer collision
            elif player.colliderect(self.wall) and player.right <= self.wall.right + 20:
                self.wall_collision = True
                player.move_ip(-4, 0)
            elif player.colliderect(self.wall) and player.left >= self.wall.left - 14:
                self.wall_collision = True
                player.move_ip(10, 0)
            elif player.colliderect(self.wall):
                alive = False
                game_over_sfx.play()
            if not player.colliderect(self.wall):
                self.wall_collision = False

            # Enemy collision
            if enemy.colliderect(self.wall) and enemy.right <= self.wall.right:
                self.e_wall_collision = True
                enemy.move_ip(-4, 0)
            elif enemy.colliderect(self.wall) and enemy.left >= self.wall.left:
                self.e_wall_collision = True
                enemy.move_ip(1, 0)
            elif not enemy.colliderect(self.wall):
                self.e_wall_collision = False

            # G-enemy collision
            if g_enemy.colliderect(self.wall) and g_enemy.right <= self.wall.right:
                self.g_wall_collision = True
                g_enemy.move_ip(-4, 0)
            elif g_enemy.colliderect(self.wall) and g_enemy.left >= self.wall.left:
                self.g_wall_collision = True
                enemy.move_ip(1, 0)
            elif not g_enemy.colliderect(self.wall):
                self.g_wall_collision = False

        # Mid-wall ---
        # Moving it
        if self.walls_active:
            pygame.draw.rect(screen, (225, 225, 225), self.wall1)
            pygame.draw.rect(screen, (225, 225, 225), self.wall2)
            self.move += 1
            if self.move >= 1:
                self.wall1.move_ip(-1.2, 0)
                self.wall2.move_ip(-1.2, 0)
                self.move = 0
            if self.wall1.left < 0 or self.wall2.left < 0:
                self.walls_active = False

            # Asteroid collision
            elif asteroid_active:
                if self.wall1.colliderect(asteroid) or self.wall2.colliderect(asteroid):
                    asteroid_death()

            # Player collision
            if player.colliderect(self.wall1) or player.colliderect(self.wall2):
                if player.colliderect(self.wall1) and player.right <= self.wall1.right + 20:
                    self.wall_collision = True
                    player.move_ip(-4, 0)
                elif player.colliderect(self.wall1) and player.left >= self.wall1.left - 14:
                    self.wall_collision = True
                    player.move_ip(10, 0)
                elif player.colliderect(self.wall2) and player.right <= self.wall2.right + 20:
                    self.wall_collision = True
                    player.move_ip(-4, 0)
                elif player.colliderect(self.wall2) and player.left >= self.wall2.left - 14:
                    self.wall_collision = True
                    player.move_ip(10, 0)
                else:
                    alive = False
                    game_over_sfx.play()
            else:
                self.wall_collision = False

            # Enemy collision
            if enemy.colliderect(self.wall1) or enemy.colliderect(self.wall2):
                if enemy.colliderect(self.wall1) and enemy.right <= self.wall1.right:
                    self.e_wall_collision = True
                    enemy.move_ip(-4, 0)
                elif enemy.colliderect(self.wall1) and enemy.left >= self.wall1.left:
                    self.e_wall_collision = True
                    enemy.move_ip(1, 0)
                elif enemy.colliderect(self.wall2) and enemy.right <= self.wall2.right:
                    self.e_wall_collision = True
                    enemy.move_ip(-4, 0)
                elif enemy.colliderect(self.wall2) and enemy.left >= self.wall2.left:
                    self.e_wall_collision = True
                    enemy.move_ip(1, 0)
                else:
                    self.e_wall_collision = False
            else:
                self.e_wall_collision = False

            # G-enemy collision
            if g_enemy.colliderect(self.wall1) or g_enemy.colliderect(self.wall2):
                if g_enemy.colliderect(self.wall1) and g_enemy.right <= self.wall1.right:
                    self.g_wall_collision = True
                    g_enemy.move_ip(-4, 0)
                elif g_enemy.colliderect(self.wall1) and g_enemy.left >= self.wall1.left:
                    self.g_wall_collision = True
                    enemy.move_ip(1, 0)
                elif g_enemy.colliderect(self.wall2) and g_enemy.right <= self.wall2.right:
                    self.g_wall_collision = True
                    g_enemy.move_ip(-4, 0)
                elif g_enemy.colliderect(self.wall2) and g_enemy.left >= self.wall2.left:
                    self.g_wall_collision = True
                    enemy.move_ip(1, 0)
                else:
                    self.g_wall_collision = False
            else:
                self.g_wall_collision = False

        return self.wall_collision, self.e_wall_collision, self.g_wall_collision

    # For game reset:
    def reset(self):
        self.wall_active = False
        self.walls_active = False
        self.cooldown = 0
