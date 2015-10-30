import pygame
from pygame.locals import *
from constants import *

class Player(object):
    def __init__(self, color, gameview=None):
        self.color = color
        self.length = 1
        self.isBot = gameview != None
        self.gameview = gameview

    def move(self, display_surface, direction):
        self.length += 1

    def choose_move(self):
        if self.isBot:
            pass
        else:
            self.move(0)

