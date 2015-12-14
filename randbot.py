import random
from player import *
from constants import *

class RandBot(Player):
    def __init__(self, color, player_num):
        Player.__init__(self, color, player_num)

    def choose_move(self, other_player):
        possible_directions = range(4)
        safe_directions = possible_directions[:]
        head = self.segments[0].topleft

        # Prevent collisions with board edges and players
        for direction in possible_directions:
            delta = DIRECTION_DELTAS[direction]
            x = head[0] + delta['x'] * CELL_WIDTH
            y = head[1] + delta['y'] * CELL_WIDTH
            possible_head = Rect(x, y, CELL_WIDTH, CELL_WIDTH)
            if self.has_collided(other_player, head=possible_head):
                safe_directions.remove(direction)
        
        # Randomly choose new direction from safe directions 
        # if current direction is unsafe
        if self.direction not in safe_directions and safe_directions != []:
            self.direction = random.choice(safe_directions)

        self.move()