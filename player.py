import pygame
from pygame.locals import *
from constants import *

class Player(object):
    def __init__(self, color, player_num):
        self.color = color
        self.direction = UP
        loc = P1_LOC if player_num == 1 else P2_LOC
        self.segments = [pygame.Rect(loc[0], loc[1], CELL_WIDTH, CELL_WIDTH)]

    def set_direction(self, direction):
        self.direction = direction

    def set_color(self, color):
        self.color = color

    def has_collided(self, other_player):
        head = self.segments[0]
        head_loc = head.topleft
        return (not (0 <= head_loc[0] <= GAME_WIDTH - CELL_WIDTH) or 
                not (0 <= head_loc[1] <= GAME_HEIGHT - CELL_WIDTH) or
                head.collidelist(self.segments[1:]) != -1 or 
                head.collidelist(other_player.segments) != -1)

    def draw(self, display_surface):
        for segment in self.segments:
            pygame.draw.rect(display_surface, self.color, segment)

    def move(self):
        head_loc = self.segments[0].topleft
        delta = DIRECTION_DELTAS[self.direction]
        new_x = head_loc[0] + delta['x'] * CELL_WIDTH
        new_y = head_loc[1] + delta['y'] * CELL_WIDTH
        head = pygame.Rect(new_x, new_y, CELL_WIDTH, CELL_WIDTH)
        self.segments.insert(0, head)

    def choose_move(self, other_player):
        self.move()