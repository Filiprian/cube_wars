import pygame
import random
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

screen = pygame.display.set_mode((1200, 640))

# Power-ups images
shield_img = pygame.image.load("../img/shield.png").convert_alpha()
power_shield = pygame.transform.scale(shield_img, (50, 50))
move_speed_img = pygame.image.load("../img/move_speed.png").convert_alpha()
power_move_speed = pygame.transform.scale(move_speed_img, (50, 50))
quick_fire_img = pygame.image.load("../img/quick_fire.png").convert_alpha()
power_quick_fire = pygame.transform.scale(quick_fire_img, (50, 50))
# Power-ups rects
shield_rect = power_shield.get_rect()
move_speed_rect = power_move_speed.get_rect()
quick_fire_rect = power_quick_fire.get_rect()
# SFX and channel
power_up_sfx = pygame.mixer.Sound("../SFX/power_up.wav")
power_down_sfx = pygame.mixer.Sound("../SFX/power_down.mp3")
power_up_channel = pygame.mixer.Channel(9)


class Power_ups:
    def __init__(self):
        self.cooldown = 0
        self.active = False
        self.shield_active = False
        self.move_speed_active = False
        self.quick_fire_active = False
        self.power_ups = ["Shield", "Move speed", "Quick fire"]
        self.power_up = random.choice(self.power_ups)
        self.duration = 0
        self.shield = shield_rect
        self.move_speed = move_speed_rect
        self.quick_fire = quick_fire_rect
        self.shield_img = power_shield
        self.move_speed_img = power_move_speed
        self.quick_fire_img = power_quick_fire
        self.player_shield = None

    # Handles collisions with shield
    def shield_collision(self):
        power_up_channel.play(power_up_sfx)
        self.shield_active = False
        self.cooldown = 0
        self.duration = 0

    # When player picks up power-up
    def power_up_collision(self):
        self.active = False
        self.cooldown = 0
        power_up_channel.play(power_up_sfx)

    # When power-up ends
    def power_down(self):
        self.duration = 0
        self.cooldown = 0
        power_up_channel.play(power_down_sfx)

    # Power-ups function
    def update(self, rift_active, screen, player, shots, x, y, power_up_len, asteroid, asteroid_active, asteroid_death):
        # Creating power-ups
        self.cooldown += 1
        if self.cooldown >= 500 and not (self.active or rift_active):
            self.power_up = random.choice(self.power_ups)
            self.cooldown = 0
            self.active = True
            if self.power_up == "Shield":
                self.shield.topleft = (1250, random.randrange(50, 590))
            elif self.power_up == "Move speed":
                self.move_speed.topleft = (1250, random.randrange(50, 590))
            elif self.power_up == "Quick fire":
                self.quick_fire.topleft = (1250, random.randrange(50, 590))

        # Moving them
        if self.active:
            if self.power_up == "Shield":
                screen.blit(self.shield_img, self.shield.topleft)
                if self.shield.right >= 0:
                    self.shield.move_ip(-1.5, 0)
                if self.shield.right < 0:
                    self.active = False
                    self.cooldown = 0

                # Collisions
                if player.colliderect(shield_rect):
                    self.shield_active = True
                    self.power_up_collision()
                for shot in shots[:]:
                    if shot.colliderect(shield_rect):
                        self.shield_active = True
                        shots.remove(shot)
                        self.power_up_collision()

            # Moving power-up
            elif self.power_up == "Move speed":
                screen.blit(self.move_speed_img, self.move_speed.topleft)
                if self.move_speed.right >= 0:
                    self.move_speed.move_ip(-1.5, 0)
                if self.move_speed.right < 0:
                    self.active = False
                    self.cooldown = 0

                # Collisions
                if player.colliderect(self.move_speed):
                    self.move_speed_active = True
                    self.power_up_collision()
                for shot in shots[:]:
                    if shot.colliderect(self.move_speed):
                        self.move_speed_active = True
                        shots.remove(shot)
                        self.power_up_collision()

            # Moving power-up
            elif self.power_up == "Quick fire":
                screen.blit(self.quick_fire_img, self.quick_fire.topleft)
                if self.quick_fire.right >= 0:
                    self.quick_fire.move_ip(-1.5, 0)
                if self.quick_fire.right < 0:
                    self.active = False
                    self.cooldown = 0

                # Collisions
                if player.colliderect(self.quick_fire):
                    self.quick_fire_active = True
                    self.power_up_collision()
                for shot in shots[:]:
                    if shot.colliderect(self.quick_fire):
                        self.quick_fire_active = True
                        shots.remove(shot)
                        self.power_up_collision()

        # Shield power-up function
        if self.shield_active:
            self.duration += 1
            self.player_shield = pygame.Rect(x - 50, y - 50, 100, 100)
            if self.duration >= power_up_len:
                self.shield_collision()
            else:
                # Asteroid vs player shield
                pygame.draw.circle(screen, (0, 0, 220), self.player_shield.center, self.player_shield.width / 2, 5)
                if asteroid_active:
                    if asteroid.colliderect(self.player_shield):
                        asteroid_death()
                        self.shield_active = False
                        self.power_down()

        # Move_speed duration
        if self.move_speed_active:
            self.duration += 1
            if self.duration >= power_up_len:
                self.move_speed_active = False
                self.power_down()

        # Quick fire duration
        if self.quick_fire_active:
            self.duration += 1
            if self.duration >= power_up_len:
                self.quick_fire_active = False
                self.power_down()

    # For game reset:
    def reset(self):
        self.active = False
        self.cooldown = 0
        self.duration = 0
        self.shield_active = False
        self.move_speed_active = False
        self.quick_fire_active = False
