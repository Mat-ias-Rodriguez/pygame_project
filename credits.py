import pygame 

import main_game.defs as defs
import main_game.variables as variables


clock = pygame.time.Clock()
def run_credits():
    pygame.display.set_caption(variables.GAME_TITLE + " | Creditos")
    pygame.display.set_icon(pygame.image.load(variables.ICON_PATH))
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    flag = False

        defs.screen.fill(variables.BACKGROUND_COLOR)

        credit_name_creator = defs.my_font.render("Hecho por: Matias Nicolas Rodriguez Herrera", True, (255, 255, 255))
        defs.screen.blit(credit_name_creator, (variables.SCREEN_WIDTH // 2 - credit_name_creator.get_width() // 2, variables.SCREEN_HEIGHT // 2))
        credit_name_music = defs.my_font.render("musica por: xDeviruchi", True, (255, 255, 255))
        defs.screen.blit(credit_name_music, (variables.SCREEN_WIDTH // 2 - credit_name_music.get_width() // 2, variables.SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(30)
