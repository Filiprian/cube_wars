import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# SFX and channel
rock_collision_sfx = pygame.mixer.Sound("../SFX/rock_collision.wav")
rock_explosion_sfx = pygame.mixer.Sound("../SFX/rock_exposion.wav")
rock_channel = pygame.mixer.Channel(7)


class Space_rock():
    def __init__(self):
        self.cooldown = 0
        self.active = False
        self.move = 0
        self.rock = pygame.Rect(1250, random.randint(20, 620), 160, 160)
        self.collision_sfx = rock_collision_sfx
        self.channel = rock_channel
        self.particle = None
        self.particles = []

    # Rock function
    def update(self, screen, player, enemy, turret_active, enemy_killcount, player_death, rock_shot,
                enemy_particles, explosion_sfx, new_enemy_killcount, g_enemy, asteroid, asteroid_active
               , asteroid_death, g_enemy_death, asteroid_particles, rock_lifes):
        # Creating rock
        self.cooldown += 1
        if self.cooldown >= 800 and not (self.active or turret_active) and 0 < enemy_killcount < 17:
            self.rock = pygame.Rect(1250, random.randint(20, 620), 160, 160)
            self.active = True
            self.cooldown = 0

        # Rock move
        if self.active:
            self.move += 1
            pygame.draw.circle(screen, (175, 75, 0), self.rock.center, 80)
            if self.move >= 1:
                self.rock.move_ip(-1, 0)
                self.move = 0

            # Rock death
            if self.rock.right < 0:
                self.active = False
                self.cooldown = 0
            if rock_shot == rock_lifes:
                self.active = False
                self.cooldown = 0
                self.channel.play(rock_explosion_sfx)

            # Rock collisions
            if self.rock.colliderect(player):
                player_death()
            elif self.rock.colliderect(enemy) and self.rock.left < 1200:
                enemy_particles()
                explosion_sfx.play()
                new_enemy_killcount()
            elif self.rock.colliderect(g_enemy):
                g_enemy_death()
            if asteroid_active:
                if self.rock.colliderect(asteroid):
                    asteroid_death()
                    asteroid_particles()

    # Creating particles
    def rock_particles(self, screen, rock_lifes, rock_shot):
        if rock_shot == rock_lifes:
            for i in range(8):
                r_x, r_y = self.rock.center
                self.particle = pygame.Rect((r_x, r_y, 60, 60))
                self.particles.append(self.particle)

        # Updating particles
        for r_particle in self.particles[:]:
            pygame.draw.rect(screen, (150, 75, 0), r_particle)
            r_particle.move_ip(random.randint(-5, 5), random.randint(-5, 5))
            r_particle.inflate_ip(-1, -1)
            if r_particle.width == 0 or r_particle.height == 0:
                self.particles.remove(r_particle)

    # For game reset:
    def reset(self):
        self.active = False
        self.cooldown = 0
        self.move = 0
