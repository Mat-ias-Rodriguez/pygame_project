import pygame
import main_game.defs as defs
import main_game.variables as variables
from main_game.main import run_game
import credits  

pygame.init()
pygame.display.set_caption(variables.GAME_TITLE + " | MENU")
pygame.display.set_icon(pygame.image.load(variables.ICON_PATH))

RECT_main_game = pygame.Rect(variables.SCREEN_WIDTH // 2 - 125, variables.SCREEN_HEIGHT // 2 - 25, 250, 50)
RECT_scoreboard = pygame.Rect(variables.SCREEN_WIDTH // 2 - 125, variables.SCREEN_HEIGHT // 2 + 50, 250, 50)
RECT_credits = pygame.Rect(variables.SCREEN_WIDTH // 2 - 125, variables.SCREEN_HEIGHT // 2 + 125, 250, 50)
RECT_exit = pygame.Rect(variables.SCREEN_WIDTH // 2 - 125, variables.SCREEN_HEIGHT // 2 + 200, 250, 50)

pygame.mixer.music.load("bgm_and_sfx/BGMs/xDeviruchi - Title Theme .wav")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(1000)

hover = pygame.mixer.Sound("./bgm_and_sfx/Blip_button_hover.wav")
hover.set_volume(0.1)
play_hover_sound = 0

select = pygame.mixer.Sound("./bgm_and_sfx/Blip_select_button.wav")
select.set_volume(0.5)


flag = True
while flag:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                flag = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and RECT_main_game.collidepoint(mouse_pos):
                select.play()
                run_game()
            elif event.button == 1 and RECT_scoreboard.collidepoint(mouse_pos):
                select.play()
                defs.points_popup()
            elif event.button == 1 and RECT_credits.collidepoint(mouse_pos):
                select.play()
                credits.run_credits()
            elif event.button == 1 and RECT_exit.collidepoint(mouse_pos):
                select.play()
                flag = False
    defs.screen.blit(defs.img_furnace_background, (0, 0))

    tittle_text = pygame.font.SysFont("Cinzel regular", 50, True)
    tittle_surface = tittle_text.render("Little Fire", True, (0, 0, 0), (100, 100, 100))
    defs.screen.blit(tittle_surface, (variables.SCREEN_WIDTH // 2 - tittle_surface.get_width() // 2, variables.SCREEN_HEIGHT // 2 - 250))

    pygame.display.set_caption(variables.GAME_TITLE + " | MENU")

    if RECT_main_game.collidepoint(mouse_pos):
        variables.button_start_color = (65, 105, 225)
        play_hover_sound += 1
    elif RECT_scoreboard.collidepoint(mouse_pos):
        variables.button_score_color = (65, 105, 225)
        play_hover_sound += 1
    elif RECT_credits.collidepoint(mouse_pos):
        variables.button_credits_color = (65, 105, 225)
        play_hover_sound += 1
    elif RECT_exit.collidepoint(mouse_pos):
        variables.button_exit_color = (65, 105, 225)
        play_hover_sound += 1
    else:
        variables.button_start_color = (100, 149, 237)
        variables.button_score_color = (100, 149, 237)
        variables.button_credits_color = (100, 149, 237)
        variables.button_exit_color = (100, 149, 237)
        play_hover_sound = 0

    if play_hover_sound == 1:
        hover.play()

    pygame.draw.rect(defs.screen, variables.button_start_color, RECT_main_game)
    pygame.draw.rect(defs.screen, variables.button_score_color, RECT_scoreboard)
    pygame.draw.rect(defs.screen, variables.button_credits_color, RECT_credits)
    pygame.draw.rect(defs.screen, variables.button_exit_color, RECT_exit)
    
    text = pygame.font.SysFont("Cinzel regular", 20)
    text_surface = text.render("Empezar juego", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=RECT_main_game.center)
    defs.screen.blit(text_surface, text_rect)
    text_surface = text.render("Tabla de puntuaciones", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=RECT_scoreboard.center)
    defs.screen.blit(text_surface, text_rect)
    text_surface = text.render("Creditos", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=RECT_credits.center)
    defs.screen.blit(text_surface, text_rect)
    text_surface = text.render("Salir", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=RECT_exit.center)
    defs.screen.blit(text_surface, text_rect)
    
    defs.mouse_blur()

    pygame.display.flip()

pygame.quit()