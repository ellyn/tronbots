import pygame, os
from pygame.locals import *
from constants import *
from player import *
from randbot import *
from minimaxbot import *

# Initializations of player colors
PLAYER_1_COLOR = USER_COLORS[0]
PLAYER_2_COLOR = USER_COLORS[1]

P1_HUMAN = False

PLAYER_INFO = None

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
        self.modeselect = ModeSelect()
        self.tournament = Tournament()

    def is_p1_human(self):
        return P1_HUMAN

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
        self._gamescreen.setup_game(PLAYER_INFO)

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

    def draw_modeselection(self):
        DISPLAYSURF.fill(OFF_WHITE)
        self.modeselect.draw()
        pygame.display.update()

    def draw_tournament(self):
        DISPLAYSURF.fill(OFF_WHITE)
        self.tournament.draw()
        pygame.display.update()

    def draw_tournament_results(self, results):
        DISPLAYSURF.fill(OFF_WHITE)
        add_text('TOURNAMENT RESULTS:', 50, DARK_GRAY, CENTER_X, CENTER_Y - 80)

        p1_wins = 'PLAYER 1 WINS: ' + str(results[0])
        add_text(p1_wins, 36, PLAYER_1_COLOR, CENTER_X, CENTER_Y - 20)

        p2_wins = 'PLAYER 2 WINS: ' + str(results[1])
        add_text(p2_wins, 36, PLAYER_2_COLOR, CENTER_X, CENTER_Y + 30)

        add_text('Press any key to return to mode selection!', 29, GRAY, CENTER_X, 
            CENTER_Y + 110, bold=False)

        pygame.display.update()


class PlayerSettings(object):
    """An instance represents the player settings screen of the game. 
    Draws all objects shown on the screen and also handles all user events 
    for this game state.
    """

    def __init__(self):
        self.phase = 0

        self.start_button = Rect(0, 0, 300, 70)
        self.start_button.center = (CENTER_X, WINDOW_HEIGHT - 100)

        self.human1 = Rect(450, P1_SETTINGS_Y - 5, 120, 40)
        self.bot1 = Rect(625, P1_SETTINGS_Y - 5, 70, 40)

        self.colors_x = [SQUARE_INIT_PADDING + i*SQUARE_SEP 
                            for i in range(len(USER_COLORS))]
        
        self.p1_rects = [Rect(x, P1_SETTINGS_Y + 2, SQUARE_WIDTH, SQUARE_WIDTH) 
                            for x in self.colors_x]
        self.p2_rects = [Rect(x, P2_SETTINGS_Y + 2, SQUARE_WIDTH, SQUARE_WIDTH) 
                            for x in self.colors_x]

        self.p1_color_select = self.p1_rects[0].inflate(2,2)
        self.p2_color_select = self.p2_rects[1].inflate(2,2)

        self.naive = Rect(250, P1_SETTINGS_Y-50, 200, 30)
        self.minimax = Rect(540, P1_SETTINGS_Y-50, 220, 30)

        self.pruning_on_button =  Rect(680, P1_SETTINGS_Y-5, 40, 30)
        self.pruning_off_button = Rect(725, P1_SETTINGS_Y-5, 50, 30)

        self.depth_plus = Rect(690, P1_SETTINGS_Y+45, 30, 30)
        self.depth_minus = Rect(725, P1_SETTINGS_Y+45, 30, 30)

        self.ratio = Rect(250, P2_SETTINGS_Y, 110, 30)
        self.chamber = Rect(410, P2_SETTINGS_Y, 170, 30)
        self.voronoi = Rect(610, P2_SETTINGS_Y, 160, 30)

        self.heuristic_selected = SIMPLE_RATIO
        self.algorithm_selected = MINIMAX
        self.pruning_on = True
        self.depth = 5

        self.first_player_select = True
        self.player_info = []

    def reset(self):
        self.first_player_select = True
        self.heuristic_selected = SIMPLE_RATIO
        self.algorithm_selected = MINIMAX
        self.pruning_on = True
        self.depth = 5
        self.phase = 0
        self.player_info = []

    def draw(self):
        if self.phase == 0:
            add_text('Choose your player settings:', 40, DARK_GRAY, CENTER_X, 100)
            add_text('PLAYER 1:', 25, DARK_GRAY, 30, P1_SETTINGS_Y, center=False)

            if P1_HUMAN:
                add_text('HUMAN', 30, DARK_GRAY, 450, P1_SETTINGS_Y - 5, center=False)
                add_text('BOT', 30, LIGHT_GRAY, 625, P1_SETTINGS_Y - 5, center=False)
            else:
                add_text('HUMAN', 30, LIGHT_GRAY, 450, P1_SETTINGS_Y - 5, center=False)
                add_text('BOT', 30, DARK_GRAY, 625, P1_SETTINGS_Y - 5, center=False)
            
            add_text('PLAYER 2:', 25, DARK_GRAY, 30, P2_SETTINGS_Y, center=False)
            add_text('BOT', 30, DARK_GRAY, 450, P2_SETTINGS_Y, center=False)

            add_text('Use the WASD keys or the arrow keys to move!', 20, 
                GRAY, CENTER_X, WINDOW_HEIGHT - 180)

            for i in range(len(USER_COLORS)):
                pygame.draw.rect(DISPLAYSURF, USER_COLORS[i], self.p1_rects[i])
                pygame.draw.rect(DISPLAYSURF, USER_COLORS[i], self.p2_rects[i])

            pygame.draw.rect(DISPLAYSURF, ORANGE, self.start_button)
            add_text('CONTINUE', 38, WHITE, CENTER_X, WINDOW_HEIGHT - 100)

            pygame.draw.rect(DISPLAYSURF, DARK_GRAY, self.p1_color_select, 3)
            pygame.draw.rect(DISPLAYSURF, DARK_GRAY, self.p2_color_select, 3)

        else:
            pygame.draw.rect(DISPLAYSURF, GRAY, self.start_button)
            if self.first_player_select:
                add_text('Set settings for Player 1', 40, DARK_GRAY, CENTER_X, 60)
            else:
                add_text('Set settings for Player 2', 40, DARK_GRAY, CENTER_X, 60)

            add_text('ALGORITHM:', 25, BLUE, 30, P1_SETTINGS_Y-50, center=False)
            add_text('HEURISTIC:', 25, ORANGE, 30, P2_SETTINGS_Y, center=False)

            if self.algorithm_selected == NAIVE:
                add_text('NAIVE BOT', 30, DARK_GRAY, 350, P1_SETTINGS_Y-35)
                add_text('MINIMAX BOT', 30, LIGHT_GRAY, 650, P1_SETTINGS_Y-35)

                add_text('RATIO', 30, LIGHT_GRAY, 300, P2_SETTINGS_Y+15)
                add_text('CHAMBER', 30, LIGHT_GRAY, 490, P2_SETTINGS_Y+15)
                add_text('VORONOI', 30, LIGHT_GRAY, 690, P2_SETTINGS_Y+15)
            else:
                add_text('NAIVE BOT', 30, LIGHT_GRAY, 350, P1_SETTINGS_Y-35)
                add_text('MINIMAX BOT', 30, DARK_GRAY, 650, P1_SETTINGS_Y-35)

                add_text('PRUNING: ', 25, DARK_GRAY, 545, P1_SETTINGS_Y-5, 
                    center=False, bold=False)
                if self.pruning_on:
                    add_text('ON', 22, DARK_GRAY, 700, P1_SETTINGS_Y+11)
                    add_text('OFF', 22, LIGHT_GRAY, 750, P1_SETTINGS_Y+11)
                else:
                    add_text('ON', 22, LIGHT_GRAY, 700, P1_SETTINGS_Y+11)
                    add_text('OFF', 22, DARK_GRAY, 750, P1_SETTINGS_Y+11)

                add_text('DEPTH: ', 25, DARK_GRAY, 545, P1_SETTINGS_Y+45, 
                    center=False, bold=False)
                add_text(str(self.depth), 28, DARK_GRAY, 670, P1_SETTINGS_Y+60)
                add_text('+  -', 40, DARK_GRAY, 720, P1_SETTINGS_Y+60)

                if self.heuristic_selected == SIMPLE_RATIO:
                    add_text('RATIO', 30, DARK_GRAY, 300, P2_SETTINGS_Y+15)
                    add_text('CHAMBER', 30, LIGHT_GRAY, 490, P2_SETTINGS_Y+15)
                    add_text('VORONOI', 30, LIGHT_GRAY, 690, P2_SETTINGS_Y+15)
                elif self.heuristic_selected == CHAMBER:
                    add_text('RATIO', 30, LIGHT_GRAY, 300, P2_SETTINGS_Y+15)
                    add_text('CHAMBER', 30, DARK_GRAY, 490, P2_SETTINGS_Y+15)
                    add_text('VORONOI', 30, LIGHT_GRAY, 690, P2_SETTINGS_Y+15)
                else:
                    add_text('RATIO', 30, LIGHT_GRAY, 300, P2_SETTINGS_Y+15)
                    add_text('CHAMBER', 30, LIGHT_GRAY, 490, P2_SETTINGS_Y+15)
                    add_text('VORONOI', 30, DARK_GRAY, 690, P2_SETTINGS_Y+15)

            pygame.draw.rect(DISPLAYSURF, GREEN, self.start_button)
            if self.first_player_select:
                add_text('NEXT PLAYER', 38, WHITE, CENTER_X, WINDOW_HEIGHT - 100)
            else:
                add_text('START!', 38, WHITE, CENTER_X, WINDOW_HEIGHT - 100)

    """ Returns a list. The first and second indices are dicts representing 
    player 1 and player 2 respectively, each with the following key-value pairs:
        algorithm:  Algorithm that was chosen. Either NAIVE or MINIMAX.
        depth:      Maximum depth (if minimax was chosen)
        pruning:    True if alpha-beta pruning is on (if minimax was chosen)
        heurustic:  Heuristic that was chosen (if minimax was chosen)

    The third index is the number of matches to play.

    Returns None if no state change.
    """
    def handle_click(self, x, y):
        global PLAYER_1_COLOR, PLAYER_2_COLOR, P1_HUMAN, PLAYER_INFO
        if self.phase == 0:
            if self.start_button.collidepoint(x,y):
                if P1_HUMAN:
                    self.player_info.append({'algorithm': HUMAN})
                self.phase = 1
            elif self.human1.collidepoint(x,y):
                P1_HUMAN = True
                self.first_player_select = False
            elif self.bot1.collidepoint(x,y):
                P1_HUMAN = False
                self.first_player_select = True
            for i in range(len(USER_COLORS)):
                if self.p1_rects[i].collidepoint(x,y):
                    PLAYER_1_COLOR = USER_COLORS[i]
                    self.p1_color_select.center = self.p1_rects[i].center
                    return False
                if self.p2_rects[i].collidepoint(x,y):
                    PLAYER_2_COLOR = USER_COLORS[i]
                    self.p2_color_select.center = self.p2_rects[i].center
                    return False
            return False
        else:
            if self.start_button.collidepoint(x,y):
                info = {'algorithm': self.algorithm_selected}
                if self.algorithm_selected == MINIMAX:
                    info['depth'] = self.depth
                    info['pruning'] = self.pruning_on
                    info['heuristic'] = self.heuristic_selected
                self.player_info.append(info)
                if self.first_player_select:
                    self.first_player_select = False
                    self.heuristic_selected = SIMPLE_RATIO
                    self.algorithm_selected = MINIMAX
                    self.pruning_on = True
                    self.depth = 5
                    return False
                else:
                    PLAYER_INFO = self.player_info
                    return True

            if self.naive.collidepoint(x,y):
                self.algorithm_selected = NAIVE
            elif self.minimax.collidepoint(x,y):
                self.algorithm_selected = MINIMAX
            elif self.algorithm_selected == MINIMAX:
                if self.pruning_on_button.collidepoint(x,y):
                    self.pruning_on = True
                elif self.pruning_off_button.collidepoint(x,y):
                    self.pruning_on = False
                elif self.depth_plus.collidepoint(x,y):
                    self.depth += 1
                elif self.depth_minus.collidepoint(x,y) and self.depth > 1:
                    self.depth -= 1

                elif self.ratio.collidepoint(x,y):
                    self.heuristic_selected = SIMPLE_RATIO
                elif self.chamber.collidepoint(x,y):
                    self.heuristic_selected = CHAMBER
                elif self.voronoi.collidepoint(x,y):
                    self.heuristic_selected = VORONOI

            return False


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
        self.is_player1_turn = True

    def setup_game(self, player_info):
        if player_info == None:
            self.player1 = Player(PLAYER_1_COLOR, 1)
            self.player2 = MinimaxBot(PLAYER_2_COLOR, 2)
        else:
            p1 = player_info[0]
            p2 = player_info[1]

            if p1['algorithm'] == HUMAN:
                self.player1 = Player(PLAYER_1_COLOR, 1)
            elif p1['algorithm'] == NAIVE:
                self.player1 = RandBot(PLAYER_1_COLOR, 1)
            else:
                self.player1 = MinimaxBot(PLAYER_1_COLOR, 1, pruning=p1['pruning'], 
                                depth=p1['depth'], heuristic=p1['heuristic'])
            
            if p2['algorithm'] == NAIVE:
                self.player2 = RandBot(PLAYER_2_COLOR, 2)
            else:
                self.player2 = MinimaxBot(PLAYER_2_COLOR, 2, pruning=p2['pruning'], 
                                depth=p2['depth'], heuristic=p2['heuristic'])
        self.total_games += 1

    def check_collisions(self):
        p1_lost = self.player1.has_collided(self.player2)
        p2_lost = self.player2.has_collided(self.player1)
        if p1_lost or p2_lost:
            DISPLAYSURF.fill(OFF_WHITE)
            if p1_lost and self.is_player1_turn:
                self.num_p2_wins += 1
                self.draw_stats()
                return P2_WIN 
            elif p2_lost and not self.is_player1_turn:
                self.num_p1_wins += 1
                self.draw_stats()
                return P1_WIN
            else:
                raise Exception('Collision logic error')
        else:
            self.is_player1_turn = not self.is_player1_turn
            return IN_PROGRESS

    def draw_stats(self):
        pygame.draw.rect(DISPLAYSURF, DARK_GRAY, Rect(0, GAME_HEIGHT, 
            GAME_WIDTH, GAME_HEIGHT))

        p1_wins = 'PLAYER 1 WINS: ' + str(self.num_p1_wins)
        add_text(p1_wins, 24, OFF_WHITE, CENTER_X / 3, STATS_PADDING)

        p2_wins = 'PLAYER 2 WINS: ' + str(self.num_p2_wins)
        add_text(p2_wins, 24, OFF_WHITE, CENTER_X * (5.0/3), STATS_PADDING)

        total_games = 'TOTAL GAMES: ' + str(self.total_games)
        add_text(total_games, 24, OFF_WHITE, CENTER_X, STATS_PADDING)

    def draw_grid(self):
        for x in range(0, GAME_WIDTH, CELL_WIDTH): # Vertical lines
            pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (x, 0), (x, GAME_HEIGHT))
        for y in range(0, GAME_HEIGHT, CELL_WIDTH): # Horizontal lines
            pygame.draw.line(DISPLAYSURF, LIGHT_GRAY, (0, y), (GAME_WIDTH, y))

    def draw_player1(self):
        if self.is_player1_turn:
            self.player1.choose_move(self.player2)
        self.player1.draw(DISPLAYSURF)

    def draw_player2(self):
        if not self.is_player1_turn:
            self.player2.choose_move(self.player1)
        self.player2.draw(DISPLAYSURF)

    def draw(self):
        self.draw_grid()
        self.draw_player1()
        self.draw_player2()
        self.draw_stats()

    # Used for tournament mode. Plays a turn of the game.
    # Returns outcome of the game.
    def play_turn(self):
        if self.is_player1_turn:
            self.player1.choose_move(self.player2)
        else:
            self.player2.choose_move(self.player1)

        p1_lost = self.player1.has_collided(self.player2)
        p2_lost = self.player2.has_collided(self.player1)
        if p1_lost or p2_lost:
            if p1_lost and self.is_player1_turn:
                self.num_p2_wins += 1
                return P2_WIN 
            elif p2_lost and not self.is_player1_turn:
                self.num_p1_wins += 1
                return P1_WIN
        else:
            self.is_player1_turn = not self.is_player1_turn
            return IN_PROGRESS

    def get_results(self):
        return [self.num_p1_wins, self.num_p2_wins]


class RematchOptions(object):
    def __init__(self):
        self.yes = Rect(0, 0, 100, 40)
        self.yes.center = (CENTER_X - 130, CENTER_Y + 40)

        self.no = Rect(0, 0, 90, 40)
        self.no.center = (CENTER_X + 130, CENTER_Y + 40)

        self.mode = Rect(0, 0, 330, 70)
        self.mode.center = (CENTER_X, WINDOW_HEIGHT - 120)

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

        pygame.draw.rect(DISPLAYSURF, GRAY, self.mode)
        add_text('Return to mode selection', 24, WHITE, CENTER_X, WINDOW_HEIGHT - 120)

    def handle_click(self, x, y):
        if self.yes.collidepoint(x,y):
            return GAME_SCREEN
        if self.no.collidepoint(x,y):
            return END_GAME
        if self.mode.collidepoint(x,y):
            return MODE_SELECT
        return -1


class ModeSelect(object):
    def __init__(self):
        self.game_mode = Rect(0, 0, 800, 100)
        self.game_mode.center = (CENTER_X, CENTER_Y - 100)

        self.tournament_mode = Rect(0, 0, 800, 100)
        self.tournament_mode.center = (CENTER_X, CENTER_Y + 100)

    def draw(self):
        add_text('GAME MODE', 70, PURPLE, CENTER_X, CENTER_Y - 120)
        add_text('Play against a bot or view two bots play a match in real-time!', 
            20, DARK_GRAY, CENTER_X, CENTER_Y - 75, bold=False)

        add_text('TOURNAMENT MODE', 60, RED, CENTER_X, CENTER_Y + 80)
        add_text('See how certain bots fare after a specified number of matches.', 
            20, DARK_GRAY, CENTER_X, CENTER_Y + 125, bold=False)

    def handle_click(self, x, y):
        if self.game_mode.collidepoint(x,y):
            return PLAYER_SETTINGS
        if self.tournament_mode.collidepoint(x,y):
            return TOURNAMENT
        return -1


class Tournament(object):
    def __init__(self):
        self.start_button = Rect(0, 0, 280, 70)
        self.start_button.center = (CENTER_X, WINDOW_HEIGHT - 100)

        self.naive = Rect(250, P1_SETTINGS_Y-50, 200, 30)
        self.minimax = Rect(540, P1_SETTINGS_Y-50, 220, 30)

        self.pruning_on_button =  Rect(680, P1_SETTINGS_Y-5, 40, 30)
        self.pruning_off_button = Rect(725, P1_SETTINGS_Y-5, 50, 30)

        self.depth_plus = Rect(690, P1_SETTINGS_Y+45, 30, 30)
        self.depth_minus = Rect(725, P1_SETTINGS_Y+45, 30, 30)

        self.ratio = Rect(250, P2_SETTINGS_Y, 110, 30)
        self.chamber = Rect(410, P2_SETTINGS_Y, 170, 30)
        self.voronoi = Rect(610, P2_SETTINGS_Y, 160, 30)

        self.match_plus = Rect(510, P2_SETTINGS_Y+70, 30, 30)
        self.match_minus = Rect(545, P2_SETTINGS_Y+70, 30, 30)

        self.heuristic_selected = SIMPLE_RATIO
        self.algorithm_selected = MINIMAX
        self.pruning_on = True
        self.depth = 5

        self.match_index = 0
        self.match_numbers = [1, 2, 5, 25, 50]

        self.first_bot_select = True
        self.bot_info = []

        self.selection_complete = False

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, GRAY, self.start_button)
        if self.first_bot_select:
            add_text('Set settings for Bot 1', 40, DARK_GRAY, CENTER_X, 60)
        else:
            add_text('Set settings for Bot 2', 40, DARK_GRAY, CENTER_X, 60)

        add_text('ALGORITHM:', 25, BLUE, 30, P1_SETTINGS_Y-50, center=False)
        add_text('HEURISTIC:', 25, ORANGE, 30, P2_SETTINGS_Y, center=False)

        if self.algorithm_selected == NAIVE:
            add_text('NAIVE BOT', 30, DARK_GRAY, 350, P1_SETTINGS_Y-35)
            add_text('MINIMAX BOT', 30, LIGHT_GRAY, 650, P1_SETTINGS_Y-35)

            add_text('RATIO', 30, LIGHT_GRAY, 300, P2_SETTINGS_Y+15)
            add_text('CHAMBER', 30, LIGHT_GRAY, 490, P2_SETTINGS_Y+15)
            add_text('VORONOI', 30, LIGHT_GRAY, 690, P2_SETTINGS_Y+15)
        else:
            add_text('NAIVE BOT', 30, LIGHT_GRAY, 350, P1_SETTINGS_Y-35)
            add_text('MINIMAX BOT', 30, DARK_GRAY, 650, P1_SETTINGS_Y-35)

            add_text('PRUNING: ', 25, DARK_GRAY, 545, P1_SETTINGS_Y-5, 
                center=False, bold=False)
            if self.pruning_on:
                add_text('ON', 22, DARK_GRAY, 700, P1_SETTINGS_Y+11)
                add_text('OFF', 22, LIGHT_GRAY, 750, P1_SETTINGS_Y+11)
            else:
                add_text('ON', 22, LIGHT_GRAY, 700, P1_SETTINGS_Y+11)
                add_text('OFF', 22, DARK_GRAY, 750, P1_SETTINGS_Y+11)

            add_text('DEPTH: ', 25, DARK_GRAY, 545, P1_SETTINGS_Y+45, 
                center=False, bold=False)
            add_text(str(self.depth), 28, DARK_GRAY, 670, P1_SETTINGS_Y+60)
            add_text('+  -', 40, DARK_GRAY, 720, P1_SETTINGS_Y+60)

            if self.heuristic_selected == SIMPLE_RATIO:
                add_text('RATIO', 30, DARK_GRAY, 300, P2_SETTINGS_Y+15)
                add_text('CHAMBER', 30, LIGHT_GRAY, 490, P2_SETTINGS_Y+15)
                add_text('VORONOI', 30, LIGHT_GRAY, 690, P2_SETTINGS_Y+15)
            elif self.heuristic_selected == CHAMBER:
                add_text('RATIO', 30, LIGHT_GRAY, 300, P2_SETTINGS_Y+15)
                add_text('CHAMBER', 30, DARK_GRAY, 490, P2_SETTINGS_Y+15)
                add_text('VORONOI', 30, LIGHT_GRAY, 690, P2_SETTINGS_Y+15)
            else:
                add_text('RATIO', 30, LIGHT_GRAY, 300, P2_SETTINGS_Y+15)
                add_text('CHAMBER', 30, LIGHT_GRAY, 490, P2_SETTINGS_Y+15)
                add_text('VORONOI', 30, DARK_GRAY, 690, P2_SETTINGS_Y+15)

        if self.selection_complete:
            pygame.draw.rect(DISPLAYSURF, GRAY, self.start_button)
        else:
            pygame.draw.rect(DISPLAYSURF, GREEN, self.start_button)
        if self.first_bot_select:
            add_text('NEXT BOT', 38, WHITE, CENTER_X, WINDOW_HEIGHT - 100)
        else:
            add_text('START!', 38, WHITE, CENTER_X, WINDOW_HEIGHT - 100)
            add_text('Number of matches: ', 25, DARK_GRAY, 220, P2_SETTINGS_Y+70, 
                center=False, bold=False)
            add_text(str(self.match_numbers[self.match_index]), 28, DARK_GRAY, 
                490, P2_SETTINGS_Y+85)
            add_text('+  -', 40, DARK_GRAY, 540, P2_SETTINGS_Y+85)

    def reset(self):
        self.first_bot_select = True
        self.bot_info = []
        self.selection_complete = False
        self.heuristic_selected = SIMPLE_RATIO
        self.algorithm_selected = MINIMAX
        self.pruning_on = True
        self.depth = 5

    """ Returns a list. The first and second indices are dicts representing 
    player 1 and player 2 respectively, each with the following key-value pairs:
        algorithm:  Algorithm that was chosen. Either NAIVE or MINIMAX.
        depth:      Maximum depth (if minimax was chosen)
        pruning:    True if alpha-beta pruning is on (if minimax was chosen)
        heurustic:  Heuristic that was chosen (if minimax was chosen)

    The third index is the number of matches to play.

    Returns None if no state change.
    """
    def handle_click(self, x, y):
        if self.start_button.collidepoint(x,y):
            info = {'algorithm': self.algorithm_selected}
            if self.algorithm_selected == MINIMAX:
                info['depth'] = self.depth
                info['pruning'] = self.pruning_on
                info['heuristic'] = self.heuristic_selected
            self.bot_info.append(info)
            if self.first_bot_select:
                self.first_bot_select = False
                self.heuristic_selected = SIMPLE_RATIO
                self.algorithm_selected = MINIMAX
                self.pruning_on = True
                self.depth = 5
                return None
            else:
                self.bot_info.append(self.match_numbers[self.match_index])
                self.selection_complete = True
                return self.bot_info

        if not self.first_bot_select:
            if self.match_plus.collidepoint(x,y):
                if self.match_index < len(self.match_numbers) - 1:
                    self.match_index += 1
            elif self.match_minus.collidepoint(x,y):
                if self.match_index > 0:
                    self.match_index -= 1

        if self.naive.collidepoint(x,y):
            self.algorithm_selected = NAIVE
        elif self.minimax.collidepoint(x,y):
            self.algorithm_selected = MINIMAX
        elif self.algorithm_selected == MINIMAX:
            if self.pruning_on_button.collidepoint(x,y):
                self.pruning_on = True
            elif self.pruning_off_button.collidepoint(x,y):
                self.pruning_on = False
            elif self.depth_plus.collidepoint(x,y):
                self.depth += 1
            elif self.depth_minus.collidepoint(x,y) and self.depth > 1:
                self.depth -= 1

            elif self.ratio.collidepoint(x,y):
                self.heuristic_selected = SIMPLE_RATIO
            elif self.chamber.collidepoint(x,y):
                self.heuristic_selected = CHAMBER
            elif self.voronoi.collidepoint(x,y):
                self.heuristic_selected = VORONOI

        return None