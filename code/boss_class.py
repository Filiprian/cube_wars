import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# SFX and volume
boss_shot_sfx = pygame.mixer.Sound("../SFX/boss_shot.wav")
shrapnel_sfx = pygame.mixer.Sound("../SFX/shrapnel.wav")
boss_explosion_sfx = pygame.mixer.Sound("../SFX/boss_explosion.wav")
boss_music = pygame.mixer.Sound("../SFX/boss_music.wav")
boss_music.set_volume(0.35)
# Channels
boss_channel = pygame.mixer.Channel(10)
boss_music_channel = pygame.mixer.Channel(11)


class Boss:
    def __init__(self, screen):
        self.boss = pygame.Rect((1300, 250, 140, 140))
        self.boss_shot = pygame.Rect(self.boss.centerx-10, self.boss.centery-10, 20, 20)
        self.alive = False
        self.shot_active = False
        self.reload = 0
        self.position = 0
        self.move = 0
        self.life = 0
        self.shield_active = False
        self.shield = pygame.Rect((self.boss.centerx - 150, self.boss.centery - 150, 300, 300))
        self.shield_duration = 0
        self.granates = []
        self.screen = screen
        self.channel = boss_channel
        self.music_channel = boss_music_channel
        self.music = boss_music
        self.shot_sfx = boss_shot_sfx
        self.shrapnel_sfx = shrapnel_sfx
        self.explosion_sfx = boss_explosion_sfx
        self.particle = None
        self.particles = []

    # Boss function
    def update(self, enemy_killcount, turret_active, g_enemy_alive, boss_shot_reload, player, boss_lifes, x,
               rift_channel, rift_sfx):
        # Creating boss
        if enemy_killcount >= 20 and not (self.alive or turret_active or g_enemy_alive):
            self.alive = True
            self.boss = pygame.Rect((1300, 250, 140, 140))
            self.music_channel.play(self.music)

        # Moving boss
        if self.alive:
            b_x, b_y = self.boss.center
            pygame.draw.rect(self.screen, (225, 165, 0), self.boss)
            self.reload += 1
            self.move += 1
            if self.position < 10:
                if self.move >= 10:
                    self.move = 0
                    self.boss.move_ip(-20, 0)
                    self.position += 1

            # Boss shooting
            if self.reload >= boss_shot_reload and not self.shot_active:
                self.reload = 0
                self.boss_shot = pygame.Rect(b_x - 10, b_y - 10, 20, 20)  # Centered shot
                self.shot_active = True
                self.channel.play(self.shot_sfx)

            # Targeting shots calculation
            player_x, player_y = player.center  # Get the player's position
            direction_x = player_x - b_x  # Calculate the difference in x
            direction_y = player_y - b_y  # Calculate the difference in y
            length = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if length != 0:
                direction_x /= length
                direction_y /= length

            if self.shot_active:
                bs_x, bs_y = self.boss_shot.center
                if self.boss_shot.left > 1200 / 2:
                    pygame.draw.rect(self.screen, (225, 165, 0), self.boss_shot)
                    self.boss_shot.move_ip(direction_x * 12, direction_y * 12)
                # Creating shrapnel
                elif self.boss_shot.left <= 1200 / 2:
                    self.channel.play(self.shrapnel_sfx)

                    directions1 = [
                        (0, -12),  # Up
                        (0, 12),  # Down
                        (-8, -8),  # Up-left
                        (-12, 0),  # Left
                        (-8, 8),  # Down-left
                        (8, -8),  # Up-right
                        (12, 0),  # Right
                        (8, 8),  # Down-right
                    ]
                    directions2 = [
                        (-4, -10),  # Up
                        (-10, -4),  # Down
                        (-10, 4),  # Up-left
                        (-4, 10),  # Left
                        (4, 10),  # Down-left
                        (10, 4),  # Up-right
                        (10, -4),  # Right
                        (4, -10),  # Down-right
                    ]
                    directions_list = ["directions1", "directions2"]
                    directions_choice = random.choice(directions_list)
                    if directions_choice == "directions1":
                        directions = directions1
                    elif directions_choice == "directions2":
                        directions = directions2
                    for direction in directions:
                        shrapnel_shot = pygame.Rect(bs_x - 7, bs_y - 7, 15, 15)
                        self.granates.append((shrapnel_shot, direction))

                    self.shot_active = False

            # Boss shield
            if self.shield_active:
                self.shield_duration += 1
                if self.shield_duration < 300 and x >= 350:
                    self.shield = pygame.Rect((b_x - 150, b_y - 150, 300, 300))
                    pygame.draw.circle(self.screen, (0, 0, 220), self.shield.center, self.shield.width / 2, 5)
                elif x < 350:
                    self.shield = pygame.Rect((b_x - 150, b_y - 150, 300, 300))
                    pygame.draw.circle(self.screen, (0, 0, 220), self.shield.center, self.shield.width / 2, 5)
                else:
                    self.shield_duration = 0
                    self.shield_active = False

        # Collisions, deaths
        if self.life == boss_lifes and self.alive:
            rift_channel.play(rift_sfx)
            self.channel.play(self.explosion_sfx)
            self.boss_particles()
            self.alive = False

        if not self.alive:
            boss_music_channel.stop()

        if len(self.particles) > 0:
            self.update_particles()

    # Create particles
    def boss_particles(self):
        for i in range(12):
            b_x, b_y = self.boss.center
            self.particle = pygame.Rect((b_x, b_y, 80, 80))
            self.particles.append(self.particle)

    # Draw particles
    def update_particles(self):
        for b_particle in self.particles[:]:
            pygame.draw.rect(self.screen, (225, 165, 0), b_particle)
            b_particle.move_ip(random.randint(-5, 5), random.randint(-5, 5))
            b_particle.inflate_ip(-1, -1)
            if b_particle.width == 0 or b_particle.height == 0:
                self.particles.remove(b_particle)

    # For game reset:
    def reset(self):
        self.alive = False
        self.shot_active = False
        self.reload = 0
        self.position = 0
        self.move = 0
        self.life = 0
        self.shield_active = False
        self.shield_duration = 0
        self.granates = []
