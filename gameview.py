import pygame, sys, os
from pygame.locals import *
from constants import *
import player

PLAYER_1_COLOR = USER_COLORS[0]
PLAYER_2_COLOR = USER_COLORS[1]

DISPLAYSURF = None

def add_text(text, size, color, x, y, center=True, bold=True):
    font = 'fonts' + os.sep
    font += 'Montserrat-SemiBold.otf' if bold else 'Montserrat-UltraLight.otf'
    surface = pygame.font.Font(font, size)
    text_obj = surface.render(text, True, color)
    position = text_obj.get_rect()
    if center:
        position.center = (x,y)
    else:
        position.topleft = (x,y)
    DISPLAYSURF.blit(text_obj, position)


class GameView(object):
    """An instance of this is used to handle all updating of the game view 
    during an instance of TRONBOTS for all game states."""

    def __init__(self):
        global DISPLAYSURF
        DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('TRONBOTS')
        self.player_settings = PlayerSettings()
        self.game_screen = GameScreen()

    def draw_start_screen(self):
        DISPLAYSURF.fill(OFF_WHITE)
        add_text('TRONBOTS', 90, BLUE, CENTER_X, CENTER_Y - 30)
        add_text('Press any key to start.', 28, GRAY, CENTER_X, CENTER_Y + 40, bold=False)
        pygame.display.update()

    def draw_player_settings(self):
        DISPLAYSURF.fill(OFF_WHITE)
        self.player_settings.draw()
        pygame.display.update()

    def draw_game_screen(self):
        DISPLAYSURF.fill(OFF_WHITE)
        self.game_screen.draw()
        pygame.display.update()


class PlayerSettings(object):
    """An instance represents the player settings screen of the game. 
    Draws all objects shown on the screen and also handles all user events 
    for this game state.

    A GameView object must be initialized before this class can be used.
    """

    def __init__(self):
        self.colors_x = [SQUARE_INIT_PADDING + i*SQUARE_SEP for i in range(len(USER_COLORS))]
        
        self.p1_rects = [Rect(x, P1_SETTINGS_Y + 2, SQUARE_WIDTH, SQUARE_WIDTH) 
                            for x in self.colors_x]
        self.p2_rects = [Rect(x, P2_SETTINGS_Y + 2, SQUARE_WIDTH, SQUARE_WIDTH) 
                            for x in self.colors_x]

        self.start_button = Rect(0, 0, 320, 70)
        self.start_button.center = (CENTER_X, WINDOW_HEIGHT - 100)

        self.p1_color_select = self.p1_rects[0].inflate(2,2)
        self.p2_color_select = self.p2_rects[1].inflate(2,2)


    def draw(self):
        add_text('Choose your player settings:', 40, DARK_GRAY, CENTER_X, 100)
        add_text('PLAYER 1:', 25, DARK_GRAY, 30, P1_SETTINGS_Y, center=False)
        add_text('HUMAN', 30, DARK_GRAY, 450, P1_SETTINGS_Y - 5, center=False)
        add_text('BOT', 30, LIGHT_GRAY, 625, P1_SETTINGS_Y - 5, center=False)
        
        add_text("PLAYER 2:", 25, DARK_GRAY, 30, P2_SETTINGS_Y, center=False)
        add_text('BOT', 30, DARK_GRAY, 450, P2_SETTINGS_Y, center=False)

        for i in range(len(USER_COLORS)):
            pygame.draw.rect(DISPLAYSURF, USER_COLORS[i], self.p1_rects[i])
            pygame.draw.rect(DISPLAYSURF, USER_COLORS[i], self.p2_rects[i])

        pygame.draw.rect(DISPLAYSURF, ORANGE, self.start_button)
        add_text('START GAME!', 38, WHITE, CENTER_X, WINDOW_HEIGHT - 100)

        pygame.draw.rect(DISPLAYSURF, DARK_GRAY, self.p1_color_select, 3)
        pygame.draw.rect(DISPLAYSURF, DARK_GRAY, self.p2_color_select, 3)


    def handle_click(self, x, y):
        global PLAYER_1_COLOR, PLAYER_2_COLOR
        if self.start_button.collidepoint(x,y):
            return True
        for i in range(len(USER_COLORS)):
            if self.p1_rects[i].collidepoint(x,y):
                PLAYER_1_COLOR = USER_COLORS[i]
                self.p1_color_select.center = self.p1_rects[i].center
                return False
            if self.p2_rects[i].collidepoint(x,y):
                PLAYER_2_COLOR = USER_COLORS[i]
                self.p2_color_select.center = self.p2_rects[i].center
                return False


class GameScreen(object):
    """An instance represents the active gameplay screen of TRONBOTS.
    All internal game state is kept within this class.

    An instance of GameView must be initialized before this class can be used.
    """

    def __init__(self):
        self.num_wins = 0
        self.total_games = 1

    def new_game(self):
        self.total_games += 1

    def draw_stats(self):
        pygame.draw.rect(DISPLAYSURF, DARK_GRAY, Rect(0, GAME_HEIGHT, 
            GAME_WIDTH, GAME_HEIGHT))
        text_y = (WINDOW_HEIGHT - GAME_HEIGHT) / 2
        p1_wins = 'PLAYER 1 WIN COUNT: 0'
        add_text(p1_wins, 24, OFF_WHITE, CENTER_X / 2, STATS_PADDING)
        p2_wins = 'PLAYER 2 WIN COUNT: 0'
        add_text(p2_wins, 24, OFF_WHITE, CENTER_X * 1.5, STATS_PADDING)

    def draw_grid(self):
        for x in range(0, GAME_WIDTH, CELL_WIDTH): # Vertical lines
            pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (x, 0), (x, GAME_HEIGHT))
        for y in range(0, GAME_HEIGHT, CELL_WIDTH): # Horizontal lines
            pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (0, y), (GAME_WIDTH, y))

    def draw_player1(self):
        pass

    def draw_player2(self):
        pass

    def draw(self):
        self.draw_grid()
        self.draw_player1()
        self.draw_player2()
        self.draw_stats()

        pygame.display.update()

        #Placeholder
        while True:
            if len(pygame.event.get(QUIT)) > 0:
                pygame.quit()
                sys.exit()
            if len(pygame.event.get(KEYUP)) != 0:
                break