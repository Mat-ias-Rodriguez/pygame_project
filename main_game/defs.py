import math
import random
import json

import pygame

from .variables import *
from . import variables

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()
my_font = pygame.font.SysFont("Arial", 20)
img_power_bigger_bar = pygame.image.load("./images/power_up_bigger_bar.png")
img_power_bigger_bar = pygame.transform.scale(img_power_bigger_bar, (64, 64))
img_power_more_balls = pygame.image.load("./images/power_up_more_balls.png")
img_power_more_balls = pygame.transform.scale(img_power_more_balls, (64, 64))
img_little_fire = pygame.image.load("./images/fueguito-player.png")
img_little_fire = pygame.transform.scale(img_little_fire, (32, 32))
img_little_fire_going = pygame.image.load("./images/fueguito-yendo.png")
img_little_fire_going = pygame.transform.scale(img_little_fire_going, (32, 32))

rectangle_height_separation = 1
delimitator = 10
rectangle = 1

for _ in range(variables.numbers_of_rectangles):
    if rectangle <= delimitator:
        if variables.numbers_of_rectangles >= delimitator:
            variables.RECT = pygame.Rect((SCREEN_WIDTH // delimitator) * rectangle - (SCREEN_WIDTH // delimitator) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // delimitator - 10, 20)
        else:
            variables.RECT = pygame.Rect((SCREEN_WIDTH // variables.numbers_of_rectangles) * rectangle - (SCREEN_WIDTH // variables.numbers_of_rectangles) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // variables.numbers_of_rectangles - 10, 20)
        rectangle += 1
    else:
        rectangle_height_separation += 1
        rectangle = rectangle - delimitator
        variables.numbers_of_rectangles = variables.numbers_of_rectangles - delimitator
        if variables.numbers_of_rectangles >= delimitator:
            variables.RECT = pygame.Rect((SCREEN_WIDTH // delimitator) * rectangle - (SCREEN_WIDTH // delimitator) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // delimitator - 10, 20)
        else:
            variables.RECT = pygame.Rect((SCREEN_WIDTH // variables.numbers_of_rectangles) * rectangle - (SCREEN_WIDTH // variables.numbers_of_rectangles) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // variables.numbers_of_rectangles - 10, 20)
        rectangle += 1
    variables.rectangles.append([variables.RECT, rarity := random.randint(1, 100), health := 1, power_up_droped := False])

for rect in variables.rectangles:
        if rect[1] <= 60:
            rect[2] = rect_health1
        elif 60 < rect[1] <= 90:
            rect[2] = rect_health2
        else:
            rect[2] = rect_health3

radius = 50
diameter = radius * 2

blur_surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
blur_surf.fill((0, 0, 0, 0))

blur_rgb = (255, 255, 255)
max_alpha = 50

center = radius
for x in range(diameter):
    for y in range(diameter):
        dx = x - center
        dy = y - center

        distance = math.hypot(dx, dy)

        if distance <= radius:
            alpha = int(max_alpha * (1 - (distance / radius)))

            blur_surf.set_at((x, y), (blur_rgb[0], blur_rgb[1], blur_rgb[2], alpha))


def mouse_blur(): 
    mouse_pos = pygame.mouse.get_pos()

    draw_pos = (mouse_pos[0] - radius, mouse_pos[1] - radius)
    screen.blit(blur_surf, draw_pos)


def bar_movement():
    pygame.draw.rect(screen, BAR_COLOR, BAR)
    if variables.BAR_INITIAL_POS:
        BAR.x = (SCREEN_WIDTH // 2 - bar_width // 2)

    if pygame.KEYDOWN:
        variables.BAR_INITIAL_POS = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and BAR.left > 0:
        BAR.x -= BAR_SPEED
    if keys[pygame.K_d] and BAR.right < SCREEN_WIDTH:
        BAR.x += BAR_SPEED


def ball_movement():
    collide = pygame.mixer.Sound("./bgm_and_sfx/Blip_collide.wav")
    collide.set_volume(0.3)

    if not hasattr(variables, 'balls') or variables.balls is None:
        variables.balls = []

    if len(variables.balls) == 0:
        variables.BALL.x = variables.BAR.x + (variables.BAR.width // 2) - (variables.BALL.width // 2)
        variables.BALL.y = variables.BAR.y - variables.BALL.height
        variables.balls.append([variables.BALL.copy(), variables.ang, variables.ball_state, variables.ball_launched])

    for i in range(len(variables.balls) - 1, -1, -1):
        ball = variables.balls[i]
        ball_rect = ball[0]
        ang = ball[1]
        state = ball[2]
        launched = ball[3]

        if variables.BALL_INITIAL_POS and not launched:
            ball_rect.x = variables.BAR.x + (variables.BAR.width // 2) - (ball_rect.width // 2)
            ball_rect.y = variables.BAR.y - ball_rect.height
            screen.blit(img_little_fire, (ball_rect.x - (ball_rect.width / 2), ball_rect.y - ball_rect.height / 2))

        else:
            if ang < 0 and state:
                screen.blit(img_little_fire_going, (ball_rect.x - (ball_rect.width / 2), ball_rect.y - ball_rect.height / 2))
            elif ang > 0 and state:
                screen.blit(pygame.transform.flip(img_little_fire_going, True, False), (ball_rect.x - (ball_rect.width / 2), ball_rect.y - ball_rect.height / 2))
            elif ang < 0 and not state:
                screen.blit(pygame.transform.flip(img_little_fire_going, False, True), (ball_rect.x - (ball_rect.width / 2), ball_rect.y - ball_rect.height / 2))
            elif ang > 0 and not state:
                screen.blit(pygame.transform.flip(img_little_fire_going, True, True), (ball_rect.x - (ball_rect.width / 2), ball_rect.y - ball_rect.height / 2))

            if ball_rect.bottom >= variables.BAR.top and ball_rect.colliderect(variables.BAR):
                ball_rect.y = variables.BAR.y - ball_rect.height
                ball[1] = ((ball_rect.centerx - variables.BAR.centerx) / (max(1, variables.BAR.width // 2)))
                ball[2] = True
                collide.play()

            if variables.ball_launched and not launched:
                ball[3] = True
                ball[1] = variables.ang
                launched = True

            if ball[3]:
                if ball[2]:
                    ball_rect.y -= variables.ball_speed
                    ball_rect.x -= ball[1] * variables.ball_speed
                else:
                    ball_rect.y += variables.ball_speed
                    ball_rect.x -= ball[1] * variables.ball_speed

            if ball_rect.y <= 0:
                ball[2] = False
                collide.play()

            if ball_rect.left <= 0 or ball_rect.right >= variables.SCREEN_WIDTH:
                ball[1] = -ball[1]
                collide.play()

            if ball_rect.y > variables.SCREEN_HEIGHT:
                variables.balls.pop(i)
                continue

        # pygame.draw.rect(screen, BALL_COLOR, ball_rect)


def create_and_destroy_rectangles():
    block_break = pygame.mixer.Sound("./bgm_and_sfx/Blip_destroy_block.wav")
    block_break.set_volume(0.3)
    collide = pygame.mixer.Sound("./bgm_and_sfx/Blip_collide.wav")
    collide.set_volume(0.3)
    # Dibujar rectangulos
    for rect in variables.rectangles:
        if rect[1] <= 60:
            pygame.draw.rect(screen, (255, 0, 0), rect[0])
        elif 60 < rect[1] <= 90:
            pygame.draw.rect(screen, (0, 255, 0), rect[0])
        else:
            pygame.draw.rect(screen, (0, 0, 255), rect[0])

    for rect in variables.rectangles[:]:
        hit = False
        for bi in range(len(variables.balls) - 1, -1, -1):
            b = variables.balls[bi]
            b_rect = b[0]
            if b_rect.colliderect(rect[0]):
                left_overlap = b_rect.right - rect[0].left
                right_overlap = rect[0].right - b_rect.left
                top_overlap = b_rect.bottom - rect[0].top
                bottom_overlap = rect[0].bottom - b_rect.top

                overlaps = {"left": left_overlap, "right": right_overlap, "top": top_overlap, "bottom": bottom_overlap}
                positive = {k: v for k, v in overlaps.items() if v > 0}

                if positive:
                    side = min(positive, key=positive.get)
                    if side in ("left", "right"):
                        collide.play()
                        b[1] = -b[1]
                        if side == "left":
                            b_rect.right = rect[0].left
                        else:
                            b_rect.left = rect[0].right
                    else:
                        collide.play()
                        b[2] = not b[2]
                        if side == "top":
                            b_rect.bottom = rect[0].top
                        else:
                            b_rect.top = rect[0].bottom

                drop = random.randint(1, 100)

                if rect[1] <= 60:
                    rect[2] -= 1
                    if rect[2] <= 0:
                        if drop <= 15:
                            power_up_rect = pygame.Rect(rect[0].centerx - variables.POWERUP_SIZE//2, rect[0].centery, variables.POWERUP_SIZE, variables.POWERUP_SIZE)
                            variables.power_ups.append([power_up_rect, random.randint(0,1), variables.POWERUP_SPEED])
                        variables.player_points += 100
                        try:
                            variables.rectangles.remove(rect)
                        except ValueError:
                            pass
                        block_break.play()

                elif 60 < rect[1] <= 90:
                    rect[2] -= 1
                    if rect[2] <= 0:
                        if drop <= 50:
                            power_up_rect = pygame.Rect(rect[0].centerx - variables.POWERUP_SIZE//2, rect[0].centery, variables.POWERUP_SIZE, variables.POWERUP_SIZE)
                            variables.power_ups.append([power_up_rect, random.randint(0,1), variables.POWERUP_SPEED])
                        variables.player_points += 300
                        try:
                            variables.rectangles.remove(rect)
                        except ValueError:
                            pass
                        block_break.play()

                else:
                    rect[2] -= 1
                    if rect[2] <= 0:
                        if drop <= 70:
                            power_up_rect = pygame.Rect(rect[0].centerx - variables.POWERUP_SIZE//2, rect[0].centery, variables.POWERUP_SIZE, variables.POWERUP_SIZE)
                            variables.power_ups.append([power_up_rect, random.randint(0,1), variables.POWERUP_SPEED])
                        variables.player_points += 500
                        try:
                            variables.rectangles.remove(rect)
                        except ValueError:
                            pass
                        block_break.play()

                hit = True
                break

        if hit:
            continue


def update_power_ups():
    for i in range(len(variables.power_ups) - 1, -1, -1):
        power_up = variables.power_ups[i]
        power_up_rect = power_up[0]
        power_up_speed = power_up[2]

        power_up_rect.y += power_up_speed
        
        if power_up[1] == 0:
            screen.blit(img_power_bigger_bar, (power_up_rect.left, power_up_rect.top))
        elif power_up[1] == 1:
            screen.blit(img_power_more_balls, (power_up_rect.left, power_up_rect.top))

        if power_up_rect.colliderect(variables.BAR):
            if power_up[1] == 0:
                centerx = variables.BAR.centerx
                variables.BAR.width = 200
                variables.BAR.x = max(0, min(variables.SCREEN_WIDTH - variables.BAR.width, centerx - variables.BAR.width // 2))
                variables.power_up_active = True
                variables.powerup_end_ticks = pygame.time.get_ticks() + variables.POWERUP_DURATION

            if power_up[1] == 1:
                cx = variables.BAR.centerx
                y = variables.BAR.y - variables.BALL.height
                b1 = pygame.Rect(cx - variables.BALL.width // 2, y, variables.BALL.width, variables.BALL.height)
                b2 = pygame.Rect(cx - variables.BALL.width // 2, y, variables.BALL.width, variables.BALL.height)
                variables.balls.append([b1, 1, True, True])
                variables.balls.append([b2, -1, True, True])
                variables.ball_launched = True
            variables.power_ups.pop(i)

        if power_up_rect.y > variables.SCREEN_HEIGHT:
            variables.power_ups.pop(i)

    if getattr(variables, 'power_up_active', False):
        if pygame.time.get_ticks() >= variables.powerup_end_ticks:
            centerx = variables.BAR.centerx
            variables.BAR.width = variables.bar_width
            variables.BAR.x = max(0, min(variables.SCREEN_WIDTH - variables.BAR.width, centerx - variables.BAR.width // 2))
            variables.power_up_active = False
            variables.powerup_end_ticks = 0


def reset_game():
    reset = pygame.mixer.Sound("./bgm_and_sfx/Blip_reset.wav")
    reset.set_volume(0.3)
    reset.play()

    if variables.player_lives == 0:
        variables.player_points = 0

    variables.BALL_INITIAL_POS = True
    variables.ball_launched = False
    variables.ball_state = True
    variables.power_up_active = False
    variables.RECT = 0
    variables.numbers_of_rectangles = 100
    variables.rect_health1 = 1
    variables.rect_health2 = 2
    variables.rect_health3 = 3
    variables.rectangles = []
    variables.power_ups = []
    variables.balls = []
    
    variables.BALL.x = variables.BAR.x + (variables.BAR.width // 2) - (variables.BALL.width // 2)
    variables.BALL.y = variables.BAR.y - variables.BALL.height
    variables.balls.append([variables.BALL.copy(), 0, True, False])
    
    rectangle_height_separation = 1
    delimitator = 10
    rectangle = 1

    for _ in range(variables.numbers_of_rectangles):
        if rectangle <= delimitator:
            if variables.numbers_of_rectangles >= delimitator:
                variables.RECT = pygame.Rect((SCREEN_WIDTH // delimitator) * rectangle - (SCREEN_WIDTH // delimitator) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // delimitator - 10, 20)
            else:
                variables.RECT = pygame.Rect((SCREEN_WIDTH // variables.numbers_of_rectangles) * rectangle - (SCREEN_WIDTH // variables.numbers_of_rectangles) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // variables.numbers_of_rectangles - 10, 20)
            rectangle += 1
        else:
            rectangle_height_separation += 1
            rectangle = rectangle - delimitator
            variables.numbers_of_rectangles = variables.numbers_of_rectangles - delimitator
            if variables.numbers_of_rectangles >= delimitator:
                variables.RECT = pygame.Rect((SCREEN_WIDTH // delimitator) * rectangle - (SCREEN_WIDTH // delimitator) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // delimitator - 10, 20)
            else:
                variables.RECT = pygame.Rect((SCREEN_WIDTH // variables.numbers_of_rectangles) * rectangle - (SCREEN_WIDTH // variables.numbers_of_rectangles) + 5, 30 * rectangle_height_separation, SCREEN_WIDTH // variables.numbers_of_rectangles - 10, 20)
            rectangle += 1
        variables.rectangles.append([variables.RECT, rarity := random.randint(1, 100), health := 1])

    for rect in variables.rectangles:
        if rect[1] <= 60:
            rect[2] = variables.rect_health1
        elif 60 < rect[1] <= 90:
            rect[2] = variables.rect_health2
        else:
            rect[2] = variables.rect_health3


def check_win():
    if variables.rectangles == []:
        reset_game()


def check_lose():
    if not variables.balls:
        variables.player_lives -= 1
        death = pygame.mixer.Sound("./bgm_and_sfx/Blip_death.wav")
        death.set_volume(0.05)
        death.play()

        variables.BALL_INITIAL_POS = True
        variables.ball_launched = False
        variables.ball_state = True

        variables.BALL.x = variables.BAR.x + (variables.BAR.width // 2) - (variables.BALL.width // 2)
        variables.BALL.y = variables.BAR.y - variables.BALL.height
        variables.balls.append([variables.BALL.copy(), 0, True, False])

    if variables.player_lives <= 0 and not variables.show_game_over:
        points_system()
        variables.show_game_over = True
        reset_game()
        variables.player_lives = 3
        variables.show_game_over = False
        variables.BAR_INITIAL_POS = True


def points_popup():
    viewing_scoreboard = True
    clock = pygame.time.Clock()
    
    while viewing_scoreboard:
        screen.fill(BACKGROUND_COLOR)
        
        title_font = pygame.font.SysFont("Arial", 40, bold=True)
        title_surface = title_font.render("TABLA DE PUNTUACIONES", True, (255, 0, 0))
        screen.blit(title_surface, (variables.SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 50))
        
        y_offset = 150
        header_font = pygame.font.SysFont("Arial", 24, bold=True)
        header_surface = header_font.render(f"{"Posición":<15} {"Nombre":<20} {"Puntos":<10}", True, (255, 255, 255))
        screen.blit(header_surface, (50, y_offset))
        y_offset += 40
        
        sorted_users = sorted(variables.users.items(), key=lambda x: x[1], reverse=True)
        for idx, (name, points) in enumerate(sorted_users, 1):
            if idx <= 5:
                rank_text = f"{idx:<5}      {name:<20}         {points:<10}"
                rank_surface = my_font.render(rank_text, True, (255, 255, 255))
                screen.blit(rank_surface, (100, y_offset))
                y_offset += 35
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                    viewing_scoreboard = False
            
        pygame.display.flip()
        clock.tick(30)


def points_system():
    pygame.mixer.music.load("bgm_and_sfx/BGMs/xDeviruchi - Take some rest and eat some food!.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    reset = pygame.mixer.Sound("./bgm_and_sfx/Blip_reset.wav")
    reset.set_volume(0.3)
    reset.play()

    text = ""
    name_entered = False
    show_scoreboard_flag = False
    
    clock = pygame.time.Clock()
    
    while not show_scoreboard_flag:
        screen.fill(variables.BACKGROUND_COLOR)
        
        title_font = pygame.font.SysFont('Arial', 40, bold=True)
        title_surface = title_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(title_surface, (variables.SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))
        
        points_surface = my_font.render(f"Puntos: {variables.player_points}", True, (255, 255, 255))
        screen.blit(points_surface, (variables.SCREEN_WIDTH // 2 - points_surface.get_width() // 2, 200))
        
        if not name_entered:
            instruction_surface = my_font.render("Ingresa tu nombre (ENTER para confirmar):", True, (255, 255, 255))
            screen.blit(instruction_surface, (variables.SCREEN_WIDTH // 2 - instruction_surface.get_width() // 2, 300))
            
            pygame.draw.rect(screen, (200, 200, 200), variables.input_box)
            pygame.draw.rect(screen, (0, 0, 0), variables.input_box, 3)
            
            txt_surface = my_font.render(text, True, (0, 0, 0))
            screen.blit(txt_surface, (variables.input_box.x + 10, variables.input_box.y + 15))
        else:
            name_saved_surface = my_font.render(f"Nombre: {variables.input_name}", True, (255, 255, 255))
            screen.blit(name_saved_surface, (variables.SCREEN_WIDTH // 2 - name_saved_surface.get_width() // 2, 350))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not name_entered:
                    if text != "":
                        variables.input_name = text
                        variables.users[variables.input_name] = variables.player_points

                        save_users()
                        
                        name_entered = True
                        return
                
                elif event.key == pygame.K_BACKSPACE and not name_entered:
                    text = text[:-1]
                
                elif not name_entered and len(text) < 15:
                    if event.unicode.isalnum() or event.unicode == " ":
                        text += event.unicode
        
        pygame.display.flip()
        clock.tick(30)


def load_users():
    try:
        if not os.path.exists(variables.USERS_FILE):
            with open(variables.USERS_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            return {}
        with open(variables.USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except Exception:
        return {}


def save_users():
    try:
        with open(variables.USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(variables.users, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


variables.users = load_users()