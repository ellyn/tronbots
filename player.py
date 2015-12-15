import pygame
from pygame.locals import *
from constants import *
from copy import deepcopy
import numpy as np

class Player(object):
    def __init__(self, color, player_num):
        self.color = color
        self.direction = UP
        self.player_num = player_num
        self.move_counter = 0 # Keeps track of movement to regulate growth rate
        loc = P1_LOC if player_num == 1 else P2_LOC
        self.segments = [Rect(loc[0], loc[1], CELL_WIDTH, CELL_WIDTH)]

    def direction_valid(self,direction):
        if (direction == UP and self.direction == DOWN):
            return False
        if (direction == LEFT and self.direction == RIGHT):
            return False
        if (direction == DOWN and self.direction == UP):
            return False
        if (direction == RIGHT and self.direction == LEFT):
            return False
        return True

    def set_direction(self, direction):
        if self.direction_valid(direction):
            self.direction = direction

    def set_color(self, color):
        self.color = color

    def clone(self, player=None, direction=None):
        if player == None:
            player = self
        cloned_player = deepcopy(player)
        if direction != None:
            cloned_player.direction = direction
            cloned_player.move()
        return cloned_player

    def get_state(self, other_player):
        state = np.zeros((GAME_HEIGHT/CELL_WIDTH, GAME_WIDTH/CELL_WIDTH))
        for rect in self.segments:
            loc = rect.topleft
            x,y = loc[0]/CELL_WIDTH, loc[1]/CELL_WIDTH
            state[y,x] = FRIENDLY
        for rect in other_player.segments:
            loc = rect.topleft
            x,y = loc[0]/CELL_WIDTH, loc[1]/CELL_WIDTH
            state[y,x] = OPPONENT
        return state


    def has_collided(self, other_player, head = None):
        segments_to_check = self.segments[:]
        if head == None:
            head = self.segments[0]
            segments_to_check.pop(0)
        head_loc = head.topleft
        return (not (0 <= head_loc[0] <= GAME_WIDTH - CELL_WIDTH) or
                not (0 <= head_loc[1] <= GAME_HEIGHT - CELL_WIDTH) or
                head.collidelist(segments_to_check) != -1 or
                head.collidelist(other_player.segments) != -1)

    def draw(self, display_surface):
        for segment in self.segments:
            pygame.draw.rect(display_surface, self.color, segment)

    def move(self):
        head_loc = self.segments[0].topleft
        delta = DIRECTION_DELTAS[self.direction]
        new_x = head_loc[0] + delta['x'] * CELL_WIDTH
        new_y = head_loc[1] + delta['y'] * CELL_WIDTH
        head = Rect(new_x, new_y, CELL_WIDTH, CELL_WIDTH)
        self.segments.insert(0, head)
        self.move_counter = (self.move_counter + 1) % PLAYER_GROWTH_RATE
        if self.move_counter == 0:
            self.segments.pop() # Remove last segment of tail

    """ Chooses the next move to make in the game.
    Subclasses of Player (aka custom bots) should override this method.

    other_player is a dict object with the following key/values:
        direction: The other player's current direction (i.e. UP)
        segments: Copy of list of segments of the other player
    """
    def choose_move(self, other_player):
        self.move()
