import pygame
import random
import math

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# SFX, volume and channel
turret_load_sfx = pygame.mixer.Sound("../SFX/turret_load.wav")
turret_unload_sfx = pygame.mixer.Sound("../SFX/turret_unload.wav")
turret_shot = pygame.mixer.Sound("../SFX/turret_shot.mp3")
turret_shot.set_volume(0.8)
turret_channel = pygame.mixer.Channel(6)


class Turret:
    def __init__(self, screen):
        self.turret = pygame.Rect(1180, 0, 50, 50)
        self.switch = pygame.Rect(1160, 320, 30, 30)
        self.active = False
        self.move = 0
        self.reload = 0
        self.shots = []
        self.turret_enemy = 0
        self.screen = screen
        self.channel = turret_channel
        self.load = turret_load_sfx
        self.unload = turret_unload_sfx
        self.sfx = turret_shot
        self.t_particle = None
        self.s_particle = None
        self.t_particles = []
        self.s_particles = []

    # Turret function
    def update(self, enemy_killcount, switch_size, x, y, turret_reload):
        # Creating turret
        if (enemy_killcount == 12 or enemy_killcount == 16 or enemy_killcount == 18) and not self.active:
            self.turret = pygame.Rect(1180, 0, 50, 50)
            self.switch = pygame.Rect(1160, 320, switch_size, switch_size)
            self.active = True
            self.channel.play(self.load)

        # Moving switch
        if self.active:
            self.move += 1
            self.reload += 1
            pygame.draw.circle(self.screen, (100, 100, 100), self.turret.center, 50)
            pygame.draw.rect(self.screen, (100, 100, 100), self.switch)
            ts_x, ts_y = self.switch.center
            t_x, t_y = self.turret.center
            if self.move >= 2:
                if y > ts_y and ts_y >= 200:
                    self.switch.move_ip(0, -5)
                    self.move = 0
                elif y < ts_y and ts_y <= 440:
                    self.switch.move_ip(0, 5)
                    self.move = 0
                elif y == ts_y or ts_y == 440:
                    self.switch.move_ip(0, 10)
                    self.move = 0
                elif y == ts_y or ts_y == 200:
                    self.switch.move_ip(0, -10)
                    self.move = 0

            # Turret shooting
            if self.reload >= turret_reload and len(self.shots) < 5:
                t_shot = pygame.Rect(t_x, t_y, 12, 12)
                self.channel.play(self.sfx)
                self.reload = 0

                # Target shots calculation
                direction_x = x - t_x
                direction_y = y - t_y
                length = math.hypot(direction_x, direction_y)
                direction_x /= length
                direction_y /= length
                self.shots.append((t_shot, direction_x, direction_y))

        # Updating particles
        if self.t_particles or self.s_particles:
            self.update_particles()

    # Creating particles
    def turret_particles(self):
        for i in range(6):
            t_x, t_y = self.turret.center
            self.t_particle = pygame.Rect(t_x, t_y, 30, 30)
            self.t_particles.append(self.t_particle)

        for i in range(6):
            s_x, s_y = self.switch.center
            self.s_particle = pygame.Rect(s_x, s_y, 20, 20)
            self.s_particles.append(self.s_particle)

    # Updating particles
    def update_particles(self):
        for t_particle in self.t_particles[:]:
            pygame.draw.rect(self.screen, (100, 100, 100), t_particle)
            t_particle.move_ip(random.randint(-5, 5), random.randint(-5, 5))
            t_particle.inflate_ip(-1, -1)
            if t_particle.width == 0:
                self.t_particles.remove(t_particle)

        for s_particle in self.s_particles[:]:
            pygame.draw.rect(self.screen, (100, 100, 100), s_particle)
            s_particle.move_ip(random.randint(-5, 5), random.randint(-5, 5))
            s_particle.inflate_ip(-1, -1)
            if s_particle.width == 0:
                self.s_particles.remove(s_particle)

    # For game reset
    def reset(self):
        self.active = False
        self.move = 0
        self.reload = 0
        self.shots.clear()
        self.turret_enemy = 0
