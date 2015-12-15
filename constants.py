import pygame
from pygame.locals import *

# Window dimensions
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600

CENTER_X = WINDOW_WIDTH / 2
CENTER_Y = WINDOW_HEIGHT / 2

# Game color scheme
WHITE       = pygame.Color(255, 255, 255)
OFF_WHITE   = pygame.Color(250, 250, 250)
LIGHT_GRAY  = pygame.Color(195, 195, 195)
GRAY        = pygame.Color(145, 145, 145)
DARK_GRAY   = pygame.Color(78,  78,  78)
BLACK       = pygame.Color(0,   0,   0)
BLUE        = pygame.Color(134, 196, 204)
RED         = pygame.Color(210, 87,  99)
ORANGE      = pygame.Color(230, 128, 72)
GREEN       = pygame.Color(165, 189, 89)
PURPLE 		= pygame.Color(171, 139, 182)

# Frames per second
FPS = 24

# Game states
START_SCREEN    = 0
PLAYER_SETTINGS = 1
GAME_SCREEN     = 2
REMATCH       	= 3
END_GAME        = 4

MODE_SELECT 	= 5
TEST_MODE 		= 6
TEST_RESULTS 	= 7

# Game outcomes
IN_PROGRESS = 0
P1_WIN 		= 1
P2_WIN 		= 2
TIE 		= 3

# Player Settings constants
P1_SETTINGS_Y = 200 # y coordinate of Player 1 row in player settings
P2_SETTINGS_Y = 325 # y coordinate of Player 2 row in player settings

SQUARE_WIDTH        = 30 # Width of the color square
SQUARE_INIT_PADDING = 185 # Initial x coordinate of the first color square
SQUARE_SEP          = 45 # Horizontal separation between color squares

USER_COLORS = [BLUE, RED, ORANGE, GREEN] # Color squares that players can choose from

# Game Screen constants
GAME_WIDTH  = WINDOW_WIDTH
GAME_HEIGHT = WINDOW_HEIGHT - 60
CELL_WIDTH  = 20 # Cell dimensions (each square of the grid)

STATS_PADDING = GAME_HEIGHT + (WINDOW_HEIGHT - GAME_HEIGHT) / 2 # y coordinate for stats

PLAYER_GROWTH_RATE = 3 # Number of units moved by player before tail moves one unit

# Default player starting locations
P1_LOC = (GAME_WIDTH / CELL_WIDTH / 4 * CELL_WIDTH,
		  GAME_HEIGHT / CELL_WIDTH / 2 * CELL_WIDTH)

P2_LOC = (GAME_WIDTH / CELL_WIDTH * 0.75 * CELL_WIDTH,
		  GAME_HEIGHT / CELL_WIDTH / 2 * CELL_WIDTH)

# Directions
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
DELTA_UP    = {'x':  0, 'y': -1}
DELTA_DOWN  = {'x':  0, 'y':  1}
DELTA_LEFT  = {'x': -1, 'y':  0}
DELTA_RIGHT = {'x':  1, 'y':  0}
DIRECTION_DELTAS = [DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT]

KEY_DIRECTION = {
    K_w: UP,    K_UP:    UP,
    K_s: DOWN,  K_DOWN:  DOWN,
    K_a: LEFT,  K_LEFT:  LEFT,
    K_d: RIGHT, K_RIGHT: RIGHT,
}

# Square Labels
FRIENDLY = 1
OPPONENT = 2

WIN = 1
LOSE = -1

#Heuristics
SIMPLE_RATIO = 0
