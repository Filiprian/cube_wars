import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# SFX and volume
enemy_pew_sfx = pygame.mixer.Sound("../SFX/enemy_pew.wav")
explosion_sfx = pygame.mixer.Sound("../SFX/explosion_sfx.wav")
explosion_sfx.set_volume(0.5)
# Channel
enemy_sounds = pygame.mixer.Channel(3)


class Enemy:
    def __init__(self, screen):
        self.enemy = pygame.Rect((random.randint(1250, 1600), random.randint(140, 500), 50, 50))
        self.alive = False
        self.move = 0
        self.move_value = 0
        self.reload = 0
        self.shots = []
        self.sfx = pygame.mixer.Sound("../SFX/enemy_pew.wav")
        self.channel = pygame.mixer.Channel(3)
        self.particle = None
        self.particles = []
        self.screen = screen

    # Enemy function
    def update(self, screen, y, player, player_death, enemy_shot_reload, e_wall_collision, enemy_killcount,
               turret_active, rift_active):
        e_x, e_y = self.enemy.center
        # Creating enemy
        if (enemy_killcount != 4 and enemy_killcount != 8 and enemy_killcount != 12 and enemy_killcount < 17
                and not turret_active and not rift_active):
            self.alive = True

        # Moving enemy
        # If enemy is alive, handle movement, shooting, and player collision
        if self.alive:
            self.move += 1
            pygame.draw.rect(screen, (0, 0, 225), self.enemy)

            # Enemy movement
            if self.move >= 2:
                e_x, e_y = self.enemy.center
                if self.move_value < 100 and not e_wall_collision:
                    self.enemy.move_ip(-5, 0)
                    self.move_value += 1
                else:
                    if e_y > y:
                        self.enemy.move_ip(0, -2)
                    else:
                        self.enemy.move_ip(0, 2)

            # Collision with player
            if player.colliderect(self.enemy):
                player_death()

            # Enemy shooting
            self.reload += 1
            if self.reload >= enemy_shot_reload and len(self.shots) <= 5 and self.enemy.left < 1200:
                enemy_shot = pygame.Rect(e_x, e_y, 18, 6)
                self.shots.append(enemy_shot)
                self.channel.play(self.sfx)
                self.reload = 0

        # Always update particles if they exist, even if the enemy is dead
        if self.particles:
            self.update_particles()

    def generate_particles(self):
        """Generate particles when the enemy dies."""
        for i in range(6):
            e_x, e_y = self.enemy.center
            self.particle = pygame.Rect((e_x, e_y, 25, 25))
            self.particles.append(self.particle)

    def update_particles(self):
        """Update and shrink particles."""
        for e_particle in self.particles[:]:
            pygame.draw.rect(self.screen, (0, 0, 225), e_particle)
            e_particle.move_ip(random.randint(-5, 5), random.randint(-5, 5))
            e_particle.inflate_ip(-1, -1)
            if e_particle.width <= 0 or e_particle.height <= 0:
                self.particles.remove(e_particle)

    # When enemy dies:
    def enemy_death(self):
        self.alive = False
        explosion_sfx.play()
        self.new_enemy()
        self.generate_particles()

    # Calling another enemy
    def new_enemy(self):
        self.alive = True
        self.enemy = pygame.Rect((random.randint(1250, 1600), random.randint(140, 500), 50, 50))
        self.move_value = 0

    # For game reset
    def reset(self):
        self.enemy = pygame.Rect((random.randint(1250, 1600), random.randint(140, 500), 50, 50))
        self.alive = False
        self.move = 0
        self.move_value = 0
        self.reload = 0
        self.shots.clear()
