import pygame


# Game screen text
def game_text(score, pause_text, score_game_txt):
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 12)
    pause_text("Click ESC for pause!", font, (255, 255, 255), 480, 600)
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 32)
    score_game_txt(f"Score: {int(score)}", font, (225, 225, 225), 470, 28)
    pygame.display.set_caption("Cube wars")


# Main menu screen text
def main_menu_text(screen, main_menu_bg, score_game_txt):
    screen.blit(main_menu_bg, (0, 0))
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 72)
    score_game_txt("Cube", font, (225, 0, 0), 300, 75)
    score_game_txt("Wars", font, (0, 0, 225), 600, 75)
    pygame.display.set_caption("Main menu")


# Paused screen text
def paused_text(screen, bg, i, bg_WIDTH, scroll, score_game_txt):
    screen.blit(bg, (i * bg_WIDTH + scroll, 0))
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 38)
    score_game_txt("The game is paused", font, (225, 225, 225), 265, 120)
    pygame.display.set_caption("Paused")


# Game over screen text
def game_over_text(screen, score_game_txt, score, best_score):
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Game over")
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 58)
    score_game_txt("Game over!", font, (225, 225, 225), 365, 40)
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 38)
    score_game_txt(f"Score: {int(score)}", font, (225, 225, 225), 472, 155)
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 38)
    score_game_txt(f"Best score: {int(best_score)}", font, (225, 225, 225), 368, 225)


# Rift screen text
def rift_text(screen, score_game_txt, score, best_score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 58)
    score_game_txt("You have won!", font, (225, 225, 225), 315, 40)
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 38)
    score_game_txt(f"Score: {int(score)}", font, (225, 225, 225), 472, 155)
    font = pygame.font.Font("../font/PressStart2P-Regular.ttf", 38)
    score_game_txt(f"Best score: {int(best_score)}", font, (225, 225, 225), 368, 225)
