import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# SFX and volume
explosion_sfx = pygame.mixer.Sound("../SFX/explosion_sfx.wav")
swish_sfx = pygame.mixer.Sound("../SFX/swish_sfx (2).wav")
swish_channel = pygame.mixer.Channel(2)


class Asteroid:
    def __init__(self, screen):
        self.asteroid = pygame.Rect((1300, random.randint(40, 600), 80, 80))
        self.cooldown = 0
        self.move = 0
        self.active = False
        self.particle = None
        self.particles = []
        self.ap = None
        self.aps = []
        self.screen = screen
        self.sfx = swish_sfx
        self.channel = swish_channel

    # Asteroid function
    def update(self, enemy_killcount, rift_active, asteroid_reload, asteroid_speed, player, player_death):
        self.cooldown += 1
        # Creating asteroid
        if self.cooldown >= asteroid_reload and not (self.active or enemy_killcount >= 17 or rift_active):
            self.asteroid = pygame.Rect((1240, random.randint(40, 600), 80, 80))
            self.active = True
            self.cooldown = 0
            self.channel.play(self.sfx)

        # Draw and move
        if self.active:
            self.move += 1
            pygame.draw.circle(self.screen, (120, 120, 120), self.asteroid.center, self.asteroid.width // 2)
            self.asteroid_follow_particles()
            if self.move >= 65:
                self.asteroid.move_ip(asteroid_speed, 0)

            # Collisions
            if player.colliderect(self.asteroid):
                player_death()
                self.active = False
            elif self.asteroid.right <= 0:
                self.active = False

        # using the particles
        if len(self.particles) > 0:
            self.update_particles()

        self.update_follow_particles()

    # When asteroid dies:
    def asteroid_death(self):
        explosion_sfx.play()
        self.active = False
        self.asteroid_particles()
        self.asteroid.center = (-100, -100)

    # Create particles
    def asteroid_particles(self):
        for i in range(8):
            a_x, a_y = self.asteroid.center
            self.particle = pygame.Rect((a_x, a_y, 30, 30))
            self.particles.append(self.particle)

    # Update particles
    def update_particles(self):
        for a_particle in self.particles[:]:
            pygame.draw.rect(self.screen, (120, 120, 120), a_particle)
            a_particle.move_ip(random.randint(-8, 8), random.randint(-8, 8))
            a_particle.inflate_ip(-1, -1)
            if a_particle.width == 0 or a_particle.height == 0:
                self.particles.remove(a_particle)

    # Create follow particles
    def asteroid_follow_particles(self):
        if self.active:
            a_x, a_y = self.asteroid.center
            self.ap = pygame.Rect(a_x+20, a_y-4, 32, 32)
            self.aps.append(self.ap)

    # Update follow particles
    def update_follow_particles(self):
        for a_p in self.aps[:]:
            pygame.draw.circle(self.screen, (225, 225, 225), a_p.center, a_p.width / 2)
            a_p.move_ip(random.randint(-25, 25), random.randint(-12, 12))
            a_p.inflate_ip(-1, -1)
            if a_p.width == 0 or a_p.height == 0:
                self.aps.remove(a_p)

    # For game reset:
    def reset(self):
        self.cooldown = 0
        self.active = False
        self.aps.clear()
