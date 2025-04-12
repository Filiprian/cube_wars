import pygame
import math
from cubewars.code import buttons
from player_class import player_movement
from ui.ui_text import rift_text, game_over_text, paused_text, main_menu_text, game_text
from ui.arrows import Arrows
from cubewars.code.power_ups_class import Power_ups
# Enemies
from enemy_class import Enemy
from g_enemy_class import G_enemy
from turret_class import Turret
from boss_class import Boss
# Obsticles
from asteroid_class import Asteroid
from cubewars.code.meteorite_class import Meteorite
from cubewars.code.rock_class import Space_rock
from walls_class import Walls

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# Screen setup
WIDTH, HEIGHT = 1200, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cube wars")

# Background
main_menu_bg = pygame.image.load("../img/mian_menu_screen.png").convert()
bg = pygame.image.load("../img/game_bg.jpg").convert()
bg_WIDTH = bg.get_width()


# Reset
def reset_game():
    global scroll, player, shots, diff_text_duration
    global rift_active, rift_screen, rock_shot, wall_collision, enemy_killcount
    # Game
    scroll = 0
    diff_text_duration = 0
    rift_active = False
    rift_screen = False
    # Player
    player = pygame.Rect((400, 320, 50, 50))
    shots = []
    enemy_killcount = 0
    # Moving walls
    wall_collision = False
    # Rock
    rock_shot = 0
    # Class reset
    power_ups.reset()
    enemy.reset()
    g_enemy.reset()
    turret.reset()
    asteroid.reset()
    boss.reset()
    meteorite.reset()
    rock.reset()
    walls.reset()


# To pause text
def pause_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Score text
def score_game_txt(text, fond, color_txt, x, y):
    img = fond.render(text, True, color_txt)
    screen.blit(img, (x, y))


# FPS setting
clock = pygame.time.Clock()
FPS = 60

# Rift image
rift_img = pygame.image.load("../img/rift.png").convert_alpha()
rift = pygame.transform.scale(rift_img, (160, 210))
# Creating player
player = pygame.Rect((400, 320, 50, 50))
x, y = player.center
# Rift rect
rift_rect = rift.get_rect()
rift_rect.center = (1150, 305)

# Paused button images
resume_img = pygame.image.load("../img/resume.png").convert_alpha()
quit_img = pygame.image.load("../img/quit.png").convert_alpha()
# Main menu button images
start_img = pygame.image.load("../img/start.png").convert_alpha()
exit_img = pygame.image.load("../img/exit.png").convert_alpha()
g_start_img = pygame.image.load("../img/g_start.png").convert_alpha()
g_exit_img = pygame.image.load("../img/g_exit.png").convert_alpha()
# Game over buttons images
play_again_img = pygame.image.load("../img/again.png").convert_alpha()
over_exit_img = pygame.image.load("../img/exit.png").convert_alpha()
g_again_img = pygame.image.load("../img/g_again.png").convert_alpha()
g_over_exit_img = pygame.image.load("../img/g_quit.png").convert_alpha()
# Rift buttons
level_up_img = pygame.image.load("../img/level_up.png").convert_alpha()
g_level_up_img = pygame.image.load("../img/g_level_up.png").convert_alpha()

# Pause menu buttons
resume_button = buttons.Buttons(455, 250, resume_img, 0.7)
quit_button = buttons.Buttons(475, 450, quit_img, 0.6)
# Main menu buttons
start_button = buttons.Buttons(425, 250, start_img, 0.8)
exit_button = buttons.Buttons(445, 455, exit_img, 0.7)
g_start_button = buttons.Buttons(425, 250, g_start_img, 0.82)
g_exit_button = buttons.Buttons(445, 455, g_exit_img, 0.72)
# Game over buttons
play_again_button = buttons.Buttons(470, 325, play_again_img, 0.7)
over_exit_button = buttons.Buttons(490, 480, over_exit_img, 0.6)
g_again_button = buttons.Buttons(470, 325, g_again_img, 0.72)
g_over_exit_button = buttons.Buttons(490, 480, g_exit_img, 0.62)
# Rift button
level_up_button = buttons.Buttons(470, 325, level_up_img, 0.7)
g_level_up_button = buttons.Buttons(470, 325, g_level_up_img, 0.72)

# Soundtrack
pygame.mixer.music.load("../SFX/soundtrack.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)
# SFX
# Player
pewpew_sfx = pygame.mixer.Sound("../SFX/pewpew_sfx.wav")
# Game
explosion_sfx = pygame.mixer.Sound("../SFX/explosion_sfx.wav")
game_over_sfx = pygame.mixer.Sound("../SFX/game_over_sfx (2).wav")
shot_collision_sfx = pygame.mixer.Sound("../SFX/shot_collision.wav")
# Power-ups
power_up_sfx = pygame.mixer.Sound("../SFX/power_up.wav")
power_down_sfx = pygame.mixer.Sound("../SFX/power_down.mp3")
# Rift
rift_sfx = pygame.mixer.Sound("../SFX/rift_sfx.wav")
rift_end_sfx = pygame.mixer.Sound("../SFX/rift_end.wav")

# Setting volume
pewpew_sfx.set_volume(0.75)
explosion_sfx.set_volume(0.5)
shot_collision_sfx.set_volume(0.6)
rift_sfx.set_volume(0.6)

# Setting channels
shot_collision = pygame.mixer.Channel(5)
rift_channel = pygame.mixer.Channel(12)

# Variables
# Game variables
main_menu = True
paused = False
run = True
difficulty = 0
diff_text_duration = 0
titles = math.ceil(WIDTH / bg_WIDTH) + 1
scroll = 0
# Player variables
alive = True
score = 0
best_score = 0
shot = None
shots = []
shot_reload = 0
# Enemy variables
enemy_killcount = 0
# Moving walls
wall_collision = False
e_wall_collision = False
g_wall_collision = False
# Rock
rock_shot = 0
# Rift
rift_active = False
rift_screen = False
# Font
font = pygame.font.SysFont("arial", 16)
# Enemies classes
enemy = Enemy(screen)
g_enemy = G_enemy(screen)
turret = Turret(screen)
boss = Boss(screen)
# Objects classes
asteroid = Asteroid(screen)
meteorite = Meteorite()
power_ups = Power_ups()
rock = Space_rock()
walls = Walls()
# Game class
arrows = Arrows()

# Game loop ---------------------
while run:

    # Event handling
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            run = False
        # Pause
        if key[pygame.K_ESCAPE] and not main_menu:
            paused = True

    # When player dies:
    def player_death():
        global alive
        alive = False
        game_over_sfx.play()


    # When to and not to spawn enemy
    def new_enemy_killcount():
        global enemy_killcount
        if (enemy_killcount != 4 and enemy_killcount != 8 and enemy_killcount != 12 and enemy_killcount < 17
                and not turret.active and not meteorite.active):
            enemy.new_enemy()


    # Main menu ----------
    if main_menu:

        # Mouse cursor on
        pygame.mouse.set_visible(True)

        # Screen text
        main_menu_text(screen, main_menu_bg, score_game_txt)

        # Arrows
        main_menu, run = arrows.main(key, main_menu, run)

        # buttons
        if arrows.main_arrow == 0:
            if g_start_button.draw(screen):
                main_menu = False
        else:
            if start_button.draw(screen):
                main_menu = False
        if arrows.main_arrow == 1:
            if g_exit_button.draw(screen):
                run = False
        else:
            if exit_button.draw(screen):
                run = False

    else:
        # Game/Easy mode ----------
        if not paused and alive:

            # No mouse cursor
            pygame.mouse.set_visible(False)

            # Score maker
            if not rift_active:
                score += 0.015

            # infinite background
            for i in range(0, titles):
                screen.blit(bg, (i * bg_WIDTH + scroll, 0))
            scroll -= 4
            if abs(scroll) > bg_WIDTH:
                scroll = 0

            # FPS
            clock.tick(FPS)

            # Game text (score and how to pause)
            game_text(score, pause_text, score_game_txt)

            # Map border
            if enemy.alive:
                if enemy.enemy.right < 0:
                    enemy.enemy_death()
            if g_enemy.g_enemy.right < 0 and g_enemy.alive:
                g_enemy.g_enemy_death()
            if player.right < 0 or player.top >= HEIGHT or player.bottom <= 0 or player.left >= WIDTH:
                player_death()

            # Difficulty settings
            diff_text_duration += 1
            if difficulty == 0:
                diff_text = "Easy mode"
                diff_x = 320
                # PLayer, power-ups
                len_shots = 6
                reload = 18
                power_up_len = 500
                # Enemies
                enemy_shot_speed = -9
                enemy_shot_reload = 90
                switch_size = 45
                g_enemy_size = 55
                g_enemy_shot_speed = -10
                g_enemy_reload = 110
                turret_reload = 95
                boss_shot_reload = 200
                boss_lifes = 4
                # Objects
                asteroid_speed = -12
                asteroid_reload = 360
                rock_lifes = 4
                meteorite_size = 60
                upwall_size = HEIGHT-150
                downwall_size = 150
                wall1_size = 240
                wall2_size = 400
            if difficulty == 1:
                diff_text = "Normal mode"
                diff_x = 280
                # PLayer, power-ups
                len_shots = 5
                reload = 20
                power_up_len = 450
                # Enemies
                enemy_shot_speed = -12
                enemy_shot_reload = 80
                switch_size = 40
                g_enemy_size = 50
                g_enemy_shot_speed = -12
                g_enemy_reload = 95
                turret_reload = 85
                boss_shot_reload = 175
                boss_lifes = 6
                # Objects
                asteroid_speed = -15
                asteroid_reload = 340
                rock_lifes = 6
                meteorite_size = 65
                upwall_size = HEIGHT-100
                downwall_size = 100
                wall1_size = 260
                wall2_size = 380
            if difficulty == 2:
                diff_text = "Hard mode"
                diff_x = 335
                # PLayer, power-ups
                len_shots = 5
                reload = 22
                power_up_len = 400
                # Enemies
                enemy_shot_speed = -14
                enemy_shot_reload = 60
                switch_size = 35
                g_enemy_size = 45
                g_enemy_shot_speed = -14
                g_enemy_reload = 75
                turret_reload = 70
                boss_shot_reload = 150
                boss_lifes = 8
                # Objects
                asteroid_speed = -20
                asteroid_reload = 320
                rock_lifes = 8
                meteorite_size = 70
                upwall_size = HEIGHT-85
                downwall_size = 85
                wall1_size = 280
                wall2_size = 360
            if difficulty > 2:
                diff_text = "Extreme mode"
                diff_x = 265
                # PLayer, power-ups
                len_shots = 4
                reload = 24
                power_up_len = 300
                # Enemies
                enemy_shot_speed = -16
                enemy_shot_reload = 50
                switch_size = 32
                g_enemy_size = 40
                g_enemy_shot_speed = -16
                g_enemy_reload = 60
                turret_reload = 50
                boss_shot_reload = 120
                boss_lifes = 8
                # Objects
                asteroid_speed = -28
                asteroid_reload = 300
                rock_lifes = 8
                meteorite_size = 78
                upwall_size = HEIGHT - 65
                downwall_size = 65
                wall1_size = 285
                wall2_size = 355

            # Text on the start
            if diff_text_duration < 100:
                font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 64)
                score_game_txt(diff_text, font, (225, 225, 225), diff_x, 200)

            # Player -----
            # Displaying player
            pygame.draw.rect(screen, (255, 0, 0), player)
            x, y = player.center

            # Player movement
            if not power_ups.move_speed_active:
                move_speed = 10
            elif power_ups.move_speed_active:
                move_speed = 20
            player_movement(key, move_speed, player, wall_collision)

            # Player shooting
            shot_reload += 1
            if power_ups.quick_fire_active:
                len_shots = 8
                reload = 12
            if key[pygame.K_SPACE] and len(shots) <= len_shots and shot_reload > reload:
                shot = pygame.Rect((x, y, 18, 6))
                shots.append(shot)
                shot_reload = 0
                pewpew_sfx.play()

            # Shots being created
            for shot in shots[:]:
                pygame.draw.rect(screen, (255, 0, 0), shot)
                shot.move_ip(12, 0)
                s_x, s_y = shot.center

                # Shots collisions
                if shot.right > WIDTH:
                    shots.remove(shot)
                elif enemy.alive and shot.colliderect(enemy.enemy) and not (turret.active or g_enemy.alive):
                    enemy.alive = False
                    explosion_sfx.play()
                    score += 10
                    shots.remove(shot)
                    enemy.generate_particles()
                    enemy.enemy = pygame.Rect(200, 0, 50, 50)
                    if not meteorite.active:
                        enemy_killcount += 1
                    new_enemy_killcount()
                elif asteroid.active and shot.colliderect(asteroid.asteroid):
                    score += 5
                    shots.remove(shot)
                    asteroid.asteroid_death()
                elif rock.active and rock.rock.colliderect(shot):
                    rock_shot += 1
                    shots.remove(shot)
                    rock.channel.play(rock.collision_sfx)
                elif g_enemy.alive and g_enemy.g_enemy.colliderect(shot):
                    g_enemy.alive = False
                    g_enemy.move_value = 0
                    enemy_killcount += 1
                    g_enemy.g_enemy_particles()
                    explosion_sfx.play()
                    shots.remove(shot)
                    score += 25
                    if enemy_killcount < 17:
                        enemy.new_enemy()
                elif turret.active:
                    if shot.colliderect(turret.switch):
                        turret.active = False
                        enemy_killcount += 1
                        score += 20
                        turret.turret_particles()
                        if enemy_killcount != 17:
                            enemy.new_enemy()
                        turret.channel.play(turret.unload)
                    elif shot.colliderect(turret.turret):
                        shot_collision.play(shot_collision_sfx)
                    elif enemy.alive and shot.colliderect(enemy.enemy):
                        enemy.alive = False
                        explosion_sfx.play()
                        score += 10
                        shots.remove(shot)
                        enemy.generate_particles()
                        turret.turret_enemy += 1
                        if turret.turret_enemy < 2:
                            enemy.new_enemy()
                elif boss.alive and boss.boss.colliderect(shot):
                    boss.life += 1
                    shots.remove(shot)
                    shot_collision.play(shot_collision_sfx)
                    boss.shield_active = True
                elif boss.shield_active:
                    if boss.shield.colliderect(shot):
                        shots.remove(shot)
                        shot_collision.play(shot_collision_sfx)
                elif walls.wall_active and walls.wall.colliderect(shot):
                    shots.remove(shot)
                    shot_collision.play(shot_collision_sfx)
                elif walls.walls_active and (walls.wall1.colliderect(shot) or walls.wall2.colliderect(shot)):
                    shots.remove(shot)
                    shot_collision.play(shot_collision_sfx)

            # Power-ups -----
            power_ups.update(rift_active, screen, player, shots, x, y, power_up_len, asteroid.asteroid, asteroid.active,
                             asteroid.asteroid_death)

            # Enemy -----
            enemy.update(screen, y, player, player_death, enemy_shot_reload, e_wall_collision, enemy_killcount,
                         turret.active, rift_active)

            # Enemy shots created
            for enemy_shot in enemy.shots[:]:
                pygame.draw.rect(screen, (0, 0, 225), enemy_shot)
                enemy_shot.move_ip(enemy_shot_speed, 0)

                # Enemy shot collisions
                if enemy_shot.colliderect(player):
                    player_death()
                    enemy.shots.remove(enemy_shot)
                elif enemy_shot.left <= 0:
                    enemy.shots.remove(enemy_shot)
                elif rock.active and rock.rock.colliderect(enemy_shot):
                    rock_shot += 1
                    enemy.shots.remove(enemy_shot)
                    rock.channel.play(rock.collision_sfx)
                elif power_ups.shield_active and enemy_shot.colliderect(power_ups.player_shield):
                    enemy.shots.remove(enemy_shot)
                    power_ups.shield_collision()
                elif walls.wall_active and walls.wall.colliderect(enemy_shot):
                    enemy.shots.remove(enemy_shot)
                    shot_collision.play(shot_collision_sfx)
                elif walls.walls_active and (walls.wall1.colliderect(enemy_shot) or walls.wall2.colliderect(enemy_shot)):
                    enemy.shots.remove(enemy_shot)
                    shot_collision.play(shot_collision_sfx)

            # G enemy -----
            g_enemy.update(enemy_killcount, g_enemy_size, g_wall_collision, player, player_death, y, g_enemy_reload)

            # G-shots created
            for g_shot, angle in g_enemy.shots[:]:
                pygame.draw.rect(screen, (225, 225, 0), g_shot)
                g_shot.move_ip(g_enemy_shot_speed, angle * 4)

                # G-shots collisions
                if g_shot.right < 0:
                    g_enemy.shots.remove((g_shot, angle))
                elif g_shot.colliderect(player):
                    g_enemy.shots.remove((g_shot, angle))
                    player_death()
                elif asteroid.active and g_enemy.g_enemy.colliderect(asteroid.asteroid):
                    asteroid.asteroid_death()
                elif rock.active and g_shot.colliderect(rock.rock):
                    g_enemy.shots.remove((g_shot, angle))
                    rock.channel.play(rock.collision_sfx)
                    rock_shot += 1
                elif power_ups.shield_active and power_ups.player_shield.colliderect(g_shot):
                    g_enemy.shots.remove((g_shot, angle))
                    power_ups.shield_collision()
                elif walls.wall_active and walls.wall.colliderect(g_shot):
                    g_enemy.shots.remove((g_shot, angle))
                    shot_collision.play(shot_collision_sfx)
                elif walls.walls_active and (walls.wall1.colliderect(g_shot) or walls.wall2.colliderect(g_shot)):
                    g_enemy.shots.remove((g_shot, angle))
                    shot_collision.play(shot_collision_sfx)

            # Turret -----
            turret.update(enemy_killcount, switch_size, x, y, turret_reload)

            # Turret shots created
            for t_shot, direction_x, direction_y in turret.shots[:]:
                pygame.draw.rect(screen, (100, 100, 100), t_shot)
                t_shot.move_ip(direction_x * 10, direction_y * 10)

                # Turret shots collisions
                if t_shot.left <= 0 or t_shot.right >= WIDTH + 50 or t_shot.top <= -20 or t_shot.bottom >= HEIGHT:
                    turret.shots.remove((t_shot, direction_x, direction_y))

                elif t_shot.colliderect(player):
                    player_death()
                    turret.shots.remove((t_shot, direction_x, direction_y))
                elif walls.wall_active and walls.wall.colliderect(t_shot):
                    turret.shots.remove((t_shot, direction_x, direction_y))
                    shot_collision.play(shot_collision_sfx)
                elif walls.walls_active and (walls.wall1.colliderect(t_shot) or walls.wall2.colliderect(t_shot)):
                    turret.shots.remove((t_shot, direction_x, direction_y))
                    shot_collision.play(shot_collision_sfx)
                elif power_ups.shield_active and t_shot.colliderect(power_ups.player_shield):
                    turret.shots.remove((t_shot, direction_x, direction_y))
                    power_ups.shield_collision()
                elif rock.active and t_shot.colliderect(rock.rock):
                    rock_shot += 1
                    rock.channel.play(rock.collision_sfx)
                    turret.shots.remove((t_shot, direction_x, direction_y))

            # Boss -----
            # Making sure that boss is killed
            if boss.life == boss_lifes and boss.alive:
                enemy_killcount = 0

            boss.update(enemy_killcount, turret.active, g_enemy.alive, boss_shot_reload, player,
                        boss_lifes, x, rift_channel, rift_sfx)

            # Boss shots created
            if boss.shot_active and player.colliderect(boss.boss_shot):
                alive = False
                game_over_sfx.play()

            # Boss shots collisions
            for shrapnel_shot, direction in boss.granates[:]:
                pygame.draw.rect(screen, (225, 165, 0), shrapnel_shot)
                shrapnel_shot.move_ip(direction[0], direction[1])

                if (shrapnel_shot.right < 0 or shrapnel_shot.left > WIDTH or shrapnel_shot.bottom < 0 or
                        shrapnel_shot.top > HEIGHT):
                    boss.granates.remove((shrapnel_shot, direction))
                elif shrapnel_shot.colliderect(player):
                    player_death()
                elif power_ups.shield_active:
                    if shrapnel_shot.colliderect(power_ups.player_shield):
                        boss.granates.remove((shrapnel_shot, direction))
                        power_ups.shield_collision()

            # Rift
            if boss.life == boss_lifes and not boss.alive:
                rift_active = True

            if rift_active:
                screen.blit(rift, rift_rect.topleft)
                if player.colliderect(rift_rect):
                    rift_channel.stop()
                    rift_channel.play(rift_end_sfx)
                    rift_screen = True

            # Asteroid -----
            asteroid.update(enemy_killcount, rift_active, asteroid_reload, asteroid_speed, player, player_death)

            # Asteroid vs enemy
            if enemy.enemy.colliderect(asteroid.asteroid) and enemy.alive and asteroid.asteroid.left < 1200:
                enemy.alive = False
                enemy.generate_particles()
                asteroid.asteroid_death()
                enemy.enemy = pygame.Rect(0, 0, 50, 50)
                new_enemy_killcount()

            # Space rock -----
            rock.update(screen, player, enemy.enemy, turret.active, enemy_killcount, player_death,
                        rock_shot, enemy.generate_particles, explosion_sfx, new_enemy_killcount, g_enemy.g_enemy,
                        asteroid.asteroid, asteroid.active, asteroid.asteroid_death, g_enemy.g_enemy_death,
                        asteroid.asteroid_particles, rock_lifes)
            rock.rock_particles(screen, rock_lifes, rock_shot)

            # Reset rock shots
            if rock_shot == 4:
                rock_shot = 0

            rock_active = rock.active
            # Meteorite shower -----
            enemy_killcount = meteorite.meteorite_spawn(enemy_killcount, meteorite_size, screen, HEIGHT, player_death,
                                                        player, g_enemy.new_g_enemy)
            meteorite.meteorite_follow_particles(screen)

            # Disabling walls when meteorite shower is active
            if meteorite.active:
                walls.wall_active = False
                walls.walls_active = False

            if power_ups.shield_active and meteorite.active:
                if meteorite.meteorite.colliderect(power_ups.player_shield):
                    meteorite.m_shower.remove(meteorite.meteorite)
                    power_ups.shield_collision()

            # Moving walls -----
            wall_collision, e_wall_collision, g_wall_collision = (
                walls.update(player, enemy.enemy, g_enemy.g_enemy, enemy_killcount, turret.active, upwall_size,
                             downwall_size, wall1_size, wall2_size, screen, asteroid.asteroid, asteroid.active,
                             asteroid.asteroid_death, game_over_sfx, rock_active, rift_active))

        # Paused screen ----------
        elif paused:

            # Mouse cursor on
            pygame.mouse.set_visible(True)

            # Screen text
            paused_text(screen, bg, i, bg_WIDTH, scroll, score_game_txt)

            # Buttons
            if resume_button.draw(screen):
                paused = False
            if quit_button.draw(screen):
                run = False

        # Game over screen ----------
        elif not alive:

            # Mouse cursor on
            pygame.mouse.set_visible(True)

            # Making best score
            if score > best_score:
                best_score = score

            # Screen text
            game_over_text(screen, score_game_txt, score, best_score)

            # Arrows
            alive, run, score = arrows.game_over(key, reset_game, alive, run, score)

            # Buttons
            if arrows.game_over_arrow == 0:
                if g_again_button.draw(screen):
                    reset_game()
                    alive = True
                    score = 0
            else:
                if play_again_button.draw(screen):
                    reset_game()
                    alive = True
                    score = 0
            if arrows.game_over_arrow == 1:
                if g_over_exit_button.draw(screen):
                    run = False
            else:
                if over_exit_button.draw(screen):
                    run = False

        # Rift screen ----------
        if rift_screen:

            # Mouse cursor on
            pygame.mouse.set_visible(True)

            # Making best score
            if score > best_score:
                best_score = score

            # Screen text
            rift_text(screen, score_game_txt, score, best_score)

            # Arrows
            rift_screen, run, difficulty = arrows.rift(key, rift_screen, run, reset_game, difficulty)

            # Buttons
            if arrows.rift_arrow == 0:
                if g_level_up_button.draw(screen):
                    reset_game()
                    rift_screen = False
                    difficulty += 1
            else:
                if level_up_button.draw(screen):
                    reset_game()
                    rift_screen = False
                    difficulty += 1
            if arrows.rift_arrow == 1:
                if g_over_exit_button.draw(screen):
                    run = False
            else:
                if over_exit_button.draw(screen):
                    run = False

    # Update the screen
    pygame.display.update()
    pygame.display.flip()

# The END
pygame.quit()
