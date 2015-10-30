import random
from player import *
from constants import *

class RandBot(Player):
	def __init__(self, color, player_num):
		Player.__init__(self, color, player_num)
		self.buffer = CELL_WIDTH

	def choose_move(self, other_player):
		choice = random.randint(1,4)
		if choice == 1:
			possible_directions = [i for i in range(4)]
			if self.direction == UP:
				possible_directions.remove(DOWN)
			elif self.direction == DOWN:
				possible_directions.remove(UP)
			elif self.direction == LEFT:
				possible_directions.remove(RIGHT)
			else:
				possible_directions.remove(LEFT)

			head = self.segments[0].topleft
			if head[0] < self.buffer:
				possible_directions.remove(LEFT)
			elif head[0] > GAME_WIDTH - self.buffer:
				possible_directions.remove(RIGHT)

			if head[1] < self.buffer:
				possible_directions.remove(UP)
			elif head[1] > GAME_WIDTH - self.buffer:
				possible_directions.remove(DOWN)

			self.direction = random.choice(possible_directions)
		self.move()