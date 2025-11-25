import pygame
import os

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900

BACKGROUND_COLOR = (0, 0, 0)


GAME_TITLE = "little fire"

ICON_PATH = "./Images/fire_logo.png"

bar_width = 100
BAR_HEIGHT = 15
BAR = pygame.Rect((SCREEN_WIDTH // 2 - bar_width // 2), (int(SCREEN_HEIGHT * 0.8) - BAR_HEIGHT // 2), bar_width, BAR_HEIGHT)
BAR_COLOR = (255, 0, 0)
BAR_SPEED = 15
BAR_INITIAL_POS = True

BALL_HEIGHT = 20
BALL_WIDTH = 20
BALL = pygame.Rect(0, 0, BALL_WIDTH, BALL_HEIGHT)
BALL_COLOR = (0, 255, 0)
BALL_INITIAL_POS = True
ball_speed = 15
ball_launched = False
ball_state = True

rectangles = []
RECT = 0
numbers_of_rectangles = 80
rect_health1 = 1
rect_health2 = 2
rect_health3 = 3

player_lives = 3
player_points = 0

users = {}
input_background_color = (255, 255, 255, 128)
input_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 32, 200, 64)
input_name = ""
show_game_over = False

start_ticks_bar_power_up = pygame.time.get_ticks()
ang = 0

power_up_droped = False

power_ups = []
POWERUP_SIZE = 60
POWERUP_SPEED = 3

balls = []

POWERUP_DURATION = 15000
power_up_active = False
powerup_end_ticks = 0

button_start_color = (100, 149, 237)
button_score_color = (100, 149, 237)
button_credits_color = (100, 149, 237)
button_exit_color = (100, 149, 237)

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
