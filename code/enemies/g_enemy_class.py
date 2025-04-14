import pygame, random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# SFX and volumes
g_enemy_sfx = pygame.mixer.Sound("../SFX/g_enemy_pew.wav")
explosion_sfx = pygame.mixer.Sound("../SFX/explosion_sfx.wav")
g_enemy_sfx.set_volume(0.5)
explosion_sfx.set_volume(0.5)
# Channel
g_enemy_channel = pygame.mixer.Channel(4)


class G_enemy:
    def __init__(self, screen):
        self.g_enemy = pygame.Rect((1300, random.randint(25, 610), 40, 40))
        self.alive = False
        self.move = 0
        self.move_value = 0
        self.reload = 0
        self.shots = []
        self.screen = screen
        self.sfx = g_enemy_sfx
        self.channel = g_enemy_channel
        self.particles = []
        self.particle = None

    # G-enemy function
    def update(self, enemy_killcount, g_enemy_size, g_wall_collision, player, player_death, y, g_enemy_reload):
        # Creating g-enemy
        if (enemy_killcount == 4 or enemy_killcount == 8) and not self.alive:
            self.alive = True
            self.g_enemy = pygame.Rect((1300, random.randint(30, 610), g_enemy_size, g_enemy_size))

        # Moving g-enemy
        if self.alive:
            pygame.draw.rect(self.screen, (225, 225, 0), self.g_enemy)
            self.move += 1
            if self.move >= 2:
                g_pos = self.g_enemy.center
                g_x, g_y = g_pos
                if self.move_value < 100 and not g_wall_collision:
                    self.g_enemy.move_ip(-5, 0)
                    self.move_value += 1
                    self.enemy_move = 0
                else:
                    if g_y > y:
                        self.g_enemy.move_ip(0, -3.5)
                        self.move = 0
                    else:
                        self.g_enemy.move_ip(0, 3.5)
                        self.move = 0

            # Collision with player
            if player.colliderect(self.g_enemy):
                player_death()

            # G-enemy shooting
            self.reload += 1
            if self.reload >= g_enemy_reload and len(self.shots) == 0 and self.alive:
                g_x, g_y = self.g_enemy.center
                self.channel.play(self.sfx)
                for angle in range(-1, 2):
                    g_shot = pygame.Rect((g_x, g_y, 15, 15))
                    self.shots.append((g_shot, angle))
                self.reload = 0

        # Updating particles
        if self.particles:
            self.update_particles()

    # When g-enemy dies:
    def g_enemy_death(self):
        self.alive = False
        explosion_sfx.play()
        self.g_enemy_particles()
        self.new_g_enemy()
        self.g_enemy.topleft = (-1000, -100)

    # Making another enemy
    def new_g_enemy(self):
        self.alive = True
        self.g_enemy = pygame.Rect((random.randint(1250, 1600), random.randint(140, 500), 60, 60))
        self.move_value = 0
        self.move = 0

    # Create particles
    def g_enemy_particles(self):
        for i in range(6):
            x, y = self.g_enemy.center
            self.particle = pygame.Rect((x, y, 25, 25))
            self.particles.append(self.particle)

    # Update particles
    def update_particles(self):
        for particle in self.particles[:]:
            pygame.draw.rect(self.screen, (225, 225, 0), particle)
            particle.move_ip(random.randint(-5, 5), random.randint(-5, 5))
            particle.inflate_ip(-1, -1)
            if particle.width == 0 or particle.height == 0:
                self.particles.remove(particle)

    # For game reset
    def reset(self):
        self.alive = False
        self.shots = []
        self.reload = 0
        self.move = 0
        self.move_value = 0
