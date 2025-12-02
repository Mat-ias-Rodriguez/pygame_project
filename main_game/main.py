import random

import pygame
from PIL import Image, ImageFilter

from . import variables
from . import defs



def run_game():
    pygame.display.set_caption(variables.GAME_TITLE)
    pygame.display.set_icon(pygame.image.load(variables.ICON_PATH))

    pygame.mixer.music.load("bgm_and_sfx/BGMs/xDeviruchi - And The Journey Begins .wav")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    flag = True
    clock = pygame.time.Clock()

    # Preparar superficie desenfocada una sola vez y usarla constantemente
    orig_surface = defs.img_furnace_background.copy()
    orig_bytes = pygame.image.tostring(orig_surface, "RGBA")
    pil = Image.frombytes("RGBA", (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT), orig_bytes)
    pil_blurred = pil.filter(ImageFilter.GaussianBlur(radius=6))
    blur_bytes = pil_blurred.tobytes("raw", "RGBA")
    blurred_surface = pygame.image.fromstring(blur_bytes, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT), "RGBA")

    # Usar siempre la superficie desenfocada
    surf = blurred_surface

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    flag = False
                    pygame.mixer.music.load("bgm_and_sfx/BGMs/xDeviruchi - Title Theme .wav")
                    pygame.mixer.music.set_volume(0.05)
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_TAB:
                    defs.points_popup()
                if event.key == pygame.K_SPACE and not variables.ball_launched:
                    y_pos = variables.BALL.y
                    variables.BALL_INITIAL_POS = False
                    variables.ang = random.randint(0, 1)
                    variables.ball_launched = True
                    if variables.ang == 0:
                        variables.ang = -1
                if event.key == pygame.K_SPACE and variables.ball_launched and variables.BALL.y == y_pos:
                    variables.BALL_INITIAL_POS = False

        defs.screen.blit(surf, (0, 0))

        lives_text_surface = defs.my_font.render(f"Vidas: {variables.player_lives}", True, (255, 255, 255))
        ponts_text_surface = defs.my_font.render(f"Puntos: {variables.player_points}", True, (255, 255, 255))

        defs.screen.blit(ponts_text_surface, (variables.SCREEN_WIDTH - ponts_text_surface.get_width(), 0))
        defs.screen.blit(lives_text_surface, (0, 0))

        defs.bar_movement()
        defs.ball_movement()
        defs.create_and_destroy_rectangles()
        defs.fire_blur()
        defs.update_power_ups()
        defs.check_win()
        defs.check_lose()

        pygame.display.flip()
        clock.tick(60)

