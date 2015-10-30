import pygame, sys, os
from pygame.locals import *
from constants import *
from player import *
from randbot import *

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
        self.playersettings = PlayerSettings()
        self._gamescreen = GameScreen()
        self.rematchoptions = RematchOptions()

    def draw_startscreen(self):
        DISPLAYSURF.fill(OFF_WHITE)
        add_text('TRONBOTS', 90, BLUE, CENTER_X, CENTER_Y - 30)
        add_text('Press any key to start.', 28, GRAY, CENTER_X, CENTER_Y + 40, bold=False)
        pygame.display.update()

    def draw_playersettings(self):
        DISPLAYSURF.fill(OFF_WHITE)
        self.playersettings.draw()
        pygame.display.update()

    def setup_gamescreen(self):
        self._gamescreen.setup_game()

    def update_gamescreen(self):
        DISPLAYSURF.fill(OFF_WHITE)
        self._gamescreen.draw()
        pygame.display.update()

    def update_P1_direction(self, direction):
        self._gamescreen.player1.set_direction(direction)

    def check_game_status(self):
        return self._gamescreen.check_collisions()

    def draw_rematchoptions(self, outcome):
        self.rematchoptions.draw(outcome)
        pygame.display.update()


class PlayerSettings(object):
    """An instance represents the player settings screen of the game. 
    Draws all objects shown on the screen and also handles all user events 
    for this game state.
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
        
        add_text('PLAYER 2:', 25, DARK_GRAY, 30, P2_SETTINGS_Y, center=False)
        add_text('BOT', 30, DARK_GRAY, 450, P2_SETTINGS_Y, center=False)

        add_text('Use the WASD keys or the arrow keys to move!', 20, 
            GRAY, CENTER_X, WINDOW_HEIGHT - 180)

        for i in range(len(USER_COLORS)):
            pygame.draw.rect(DISPLAYSURF, USER_COLORS[i], self.p1_rects[i])
            pygame.draw.rect(DISPLAYSURF, USER_COLORS[i], self.p2_rects[i])

        pygame.draw.rect(DISPLAYSURF, ORANGE, self.start_button)
        add_text('START GAME!', 38, WHITE, CENTER_X, WINDOW_HEIGHT - 100)

        pygame.draw.rect(DISPLAYSURF, DARK_GRAY, self.p1_color_select, 3)
        pygame.draw.rect(DISPLAYSURF, DARK_GRAY, self.p2_color_select, 3)

    # Returns a tuple of booleans: (game ready to start?, is Player 1 human?)
    def handle_click(self, x, y):
        global PLAYER_1_COLOR, PLAYER_2_COLOR
        if self.start_button.collidepoint(x,y):
            return True, True
        for i in range(len(USER_COLORS)):
            if self.p1_rects[i].collidepoint(x,y):
                PLAYER_1_COLOR = USER_COLORS[i]
                self.p1_color_select.center = self.p1_rects[i].center
                return False, True
            if self.p2_rects[i].collidepoint(x,y):
                PLAYER_2_COLOR = USER_COLORS[i]
                self.p2_color_select.center = self.p2_rects[i].center
                return False, True


class GameScreen(object):
    """An instance represents the active gameplay screen of TRONBOTS.
    All internal game state is kept within this class.

    An instance of GameView must be initialized before this class can be used.
    """

    def __init__(self):
        self.num_p1_wins = 0
        self.num_p2_wins = 0
        self.total_games = 0
        self.game_outcome = None

    def setup_game(self):
        self.player1 = Player(PLAYER_1_COLOR, 1)
        self.player2 = Player(PLAYER_2_COLOR, 2)
        self.total_games += 1

    def check_collisions(self):
        p1_lost = self.player1.has_collided(self.player2)
        p2_lost = self.player2.has_collided(self.player1)
        if p1_lost or p2_lost:
            DISPLAYSURF.fill(OFF_WHITE)
            if p1_lost and not p2_lost:
                self.num_p2_wins += 1
                self.draw_stats()
                return P2_WIN 
            elif not p1_lost and p2_lost:
                self.num_p1_wins += 1
                self.draw_stats()
                return P1_WIN
            else:
                self.draw_stats()
                return TIE
        else:
            return IN_PROGRESS

    def draw_stats(self):
        pygame.draw.rect(DISPLAYSURF, DARK_GRAY, Rect(0, GAME_HEIGHT, 
            GAME_WIDTH, GAME_HEIGHT))

        p1_wins = 'PLAYER 1 WIN COUNT: '
        p1_wins += str(self.num_p1_wins) + ' / ' + str(self.total_games)
        add_text(p1_wins, 24, OFF_WHITE, CENTER_X / 2, STATS_PADDING)

        p2_wins = 'PLAYER 2 WIN COUNT: '
        p2_wins += str(self.num_p2_wins) + ' / ' + str(self.total_games)
        add_text(p2_wins, 24, OFF_WHITE, CENTER_X * 1.5, STATS_PADDING)

    def draw_grid(self):
        for x in range(0, GAME_WIDTH, CELL_WIDTH): # Vertical lines
            pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (x, 0), (x, GAME_HEIGHT))
        for y in range(0, GAME_HEIGHT, CELL_WIDTH): # Horizontal lines
            pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (0, y), (GAME_WIDTH, y))

    def draw_player1(self):
        self.player1.choose_move(self.player2)
        self.player1.draw(DISPLAYSURF)

    def draw_player2(self):
        self.player2.choose_move(self.player1)
        self.player2.draw(DISPLAYSURF)

    def draw(self):
        self.draw_grid()
        self.draw_player1()
        self.draw_player2()
        self.draw_stats()


class RematchOptions(object):
    def __init__(self):
        self.yes = Rect(0, 0, 100, 40)
        self.yes.center = (CENTER_X - 130, CENTER_Y + 40)

        self.no = Rect(0, 0, 90, 40)
        self.no.center = (CENTER_X + 130, CENTER_Y + 40)

    def draw(self, outcome):
        if outcome == TIE:
            add_text('TIE', 100, PURPLE, CENTER_X, CENTER_Y-100)
        elif outcome == P1_WIN:
            add_text('PLAYER 1 WINS', 86, PLAYER_1_COLOR, CENTER_X, CENTER_Y-100)
        elif outcome == P2_WIN:
            add_text('PLAYER 2 WINS', 86, PLAYER_2_COLOR, CENTER_X, CENTER_Y-100)
        add_text('Would you like a rematch?', 40, DARK_GRAY, CENTER_X, CENTER_Y-25, bold=False)
        
        add_text('YES', 40, DARK_GRAY, CENTER_X - 130, CENTER_Y + 40)
        add_text('NO', 40, DARK_GRAY, CENTER_X + 130, CENTER_Y + 40)

    def handle_click(self, x, y):
        if self.yes.collidepoint(x,y):
            return GAME_SCREEN
        if self.no.collidepoint(x,y):
            return END_GAME
        return -1