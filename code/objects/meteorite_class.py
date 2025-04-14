import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# SFX, volume and channel
meteorite_sfx = pygame.mixer.Sound("../SFX/meteorite_swish.wav")
meteorite_sfx.set_volume(0.8)
meteorite_channel = pygame.mixer.Channel(8)


class Meteorite:
    def __init__(self):
        self.meteorite_channel = meteorite_channel
        self.m_shower = []
        self.active = False
        self.meteorite_sfx = meteorite_sfx
        self.meteorite = None
        self.move = 0
        self.timer = 0
        self.particles = []
        self.particle = None

    # Meteorite function
    def meteorite_spawn(self, enemy_killcount, meteorite_size, screen, HEIGHT, player_death, player, new_g_enemy):
        # Creating meteorite shower
        if enemy_killcount == 17 and len(self.m_shower) < 1:
            self.meteorite = pygame.Rect(random.randint(120, 1280), -100, meteorite_size, meteorite_size)
            self.m_shower.append(self.meteorite)
            self.meteorite_channel.play(self.meteorite_sfx)
            self.active = True

        # Moving it
        if self.active:
            self.move += 1
            for meteorite in self.m_shower[:]:
                pygame.draw.circle(screen, (150, 75, 0), meteorite.center, meteorite.width / 2)
                self.meteorite_follow_particles(screen)
                if self.move >= 1:
                    meteorite.move_ip(-10, random.randint(10, 14))
                    self.move = 0

                # Collisions and stop
                if meteorite.top > HEIGHT:
                    self.m_shower.remove(meteorite)
                    self.timer += 1
                elif player.colliderect(meteorite):
                    player_death()
                    self.active = False
                    self.m_shower.clear()
                elif self.timer >= 6:
                    self.active = False
                    enemy_killcount += 1
                    new_g_enemy()

        return enemy_killcount

    def meteorite_follow_particles(self, screen):
        if self.active:
            m_x, m_y = self.meteorite.center
            self.particle = pygame.Rect(m_x-8, m_y-12, 20, 20)
            self.particles.append(self.particle)

            for meteorite_particle in self.particles[:]:
                pygame.draw.circle(screen, (220, 5, 0), meteorite_particle.center, meteorite_particle.width / 2)
                meteorite_particle.move_ip(random.randint(-5, 5), random.randint(-5, 5))
                meteorite_particle.inflate_ip(-1, -1)
                if meteorite_particle.width == 0 or meteorite_particle.height == 0:
                    self.particles.remove(meteorite_particle)

    # For game reset:
    def reset(self):
        self.active = False
        self.m_shower.clear()
