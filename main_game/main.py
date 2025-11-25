import pygame
import random

from . import variables
from . import defs


def run_game():
    pygame.display.set_caption(variables.GAME_TITLE)
    pygame.display.set_icon(pygame.image.load(variables.ICON_PATH))

    pygame.mixer.music.load("bgm_and_sfx/BGMs/xDeviruchi - And The Journey Begins .wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    flag = True
    clock = pygame.time.Clock()

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    flag = False
                    pygame.mixer.music.load("bgm_and_sfx/BGMs/xDeviruchi - Title Theme .wav")
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_TAB:
                    defs.points_popup()
                if event.key == pygame.K_SPACE and not variables.ball_launched:
                    variables.BALL_INITIAL_POS = False
                    variables.ang = random.randint(0, 1)
                    variables.ball_launched = True
                    if variables.ang == 0:
                        variables.ang = -1

        defs.screen.fill(variables.BACKGROUND_COLOR)

        lives_text_surface = defs.my_font.render(f"Lives: {variables.player_lives}", True, (255, 255, 255))
        ponts_text_surface = defs.my_font.render(f"Points: {variables.player_points}", True, (255, 255, 255))

        defs.screen.blit(ponts_text_surface, (variables.SCREEN_WIDTH - ponts_text_surface.get_width(), 0))
        defs.screen.blit(lives_text_surface, (0, 0))

        defs.bar_movement()
        defs.ball_movement()
        defs.create_and_destroy_rectangles()
        defs.update_power_ups()
        defs.check_win()
        defs.check_lose()

        pygame.display.flip()
        clock.tick(30)

