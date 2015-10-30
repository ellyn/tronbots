import pygame

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

CENTER_X = WINDOW_WIDTH / 2
CENTER_Y = WINDOW_HEIGHT / 2

# Game color scheme
WHITE = pygame.Color(255, 255, 255)
OFF_WHITE = pygame.Color(250, 250, 250)
LIGHT_GRAY = pygame.Color(195, 195, 195)
GRAY = pygame.Color(145, 145, 145)
DARK_GRAY = pygame.Color(78, 78, 78)
BLACK = pygame.Color(0, 0, 0)

BLUE = pygame.Color(134, 196, 204)
RED = pygame.Color(210, 87, 99)
ORANGE = pygame.Color(230, 128, 72)
GREEN = pygame.Color(165, 189, 89)

# Frames per second
FPS = 30

# Game states
START_SCREEN = 0
PLAYER_SETTINGS = 1
GAME_SCREEN = 2
TRY_AGAIN = 3
END_GAME = 4

# Player Settings constants
P1_SETTINGS_Y = 200 # y coordinate of Player 1 row in player settings
P2_SETTINGS_Y = 325 # y coordinate of Player 2 row in player settings
SQUARE_WIDTH = 30 # Width of the color square
SQUARE_INIT_PADDING = 185 # Initial x coordinate of the first color square
SQUARE_SEP = 45 # Horizontal separation between color squares
USER_COLORS = [BLUE, RED, ORANGE, GREEN] # Color squares that players can choose from 

# Game Screen constants
GAME_WIDTH = WINDOW_WIDTH
GAME_HEIGHT = WINDOW_HEIGHT - 60
CELL_WIDTH = 20 # Cell dimensions (each square of the grid)

STATS_PADDING = GAME_HEIGHT + (WINDOW_HEIGHT - GAME_HEIGHT) / 2 # y coordinate for stats

# Directions
UP, LEFT, DOWN, RIGHT = 0, 1, 2, 3