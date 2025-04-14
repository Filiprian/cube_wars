import pygame

# SFX and volume
click_sfx = pygame.mixer.Sound("../SFX/click.mp3")
click_sfx.set_volume(0.2)


class Arrows:
    def __init__(self):
        self.game_over_arrow = 100
        self.main_arrow = 0
        self.rift_arrow = 0

    # Game over screen arrows
    def game_over(self, key, reset_game, alive, run, score):
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.game_over_arrow == 0:
            self.game_over_arrow += 1
            click_sfx.play()
        elif (key[pygame.K_w] or key[pygame.K_UP]) and self.game_over_arrow == 1:
            self.game_over_arrow -= 1
            click_sfx.play()

        if self.game_over_arrow == 100:
            if key[pygame.K_RETURN]:
                reset_game()
                alive = True
                score = 0
        elif self.game_over_arrow == 100:
            if key[pygame.K_RETURN]:
                run = False

        return alive, run, score

    # Main menu screen arrows
    def main(self, key, main_menu, run):
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.main_arrow == 0:
            self.main_arrow += 1
            click_sfx.play()
        elif (key[pygame.K_w] or key[pygame.K_UP]) and self.main_arrow == 1:
            self.main_arrow -= 1
            click_sfx.play()

        if self.main_arrow == 0:
            if key[pygame.K_SPACE] or key[pygame.K_RETURN]:
                main_menu = False
        elif self.main_arrow == 1:
            if key[pygame.K_SPACE]:
                run = False

        return main_menu, run

    # Rift screen arrows
    def rift(self, key, rift_screen, run, reset_game, difficulty):
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rift_arrow == 0:
            self.rift_arrow += 1
            click_sfx.play()
        elif (key[pygame.K_w] or key[pygame.K_UP]) and self.rift_arrow == 1:
            self.rift_arrow -= 1
            click_sfx.play()

        if self.rift_arrow == 0:
            if key[pygame.K_SPACE] or key[pygame.K_RETURN]:
                rift_screen = False
                reset_game()
                difficulty += 1
        elif self.rift_arrow == 1:
            if key[pygame.K_SPACE]:
                run = False

        return rift_screen, run, difficulty
