from player import *
from constants import *

class MinimaxBot(Player):
    """ This bot uses the well-known Minimax algorithm for its strategy,
    along with alpha-beta pruning to remove suboptimal branches.

    We use the following heuristic function to evaluate states:
    <To be done>

    For the leaves of the game tree, we consider win states to be 100
    and losses to be -100.
    """

    def __init__(self, color, player_num):
        Player.__init__(self, color, player_num)
        self.max_depth = 5 # Max depth to explore for game tree

    def choose_move(self, other_player):
        self.direction = self.minimax(other_player, 0)
        self.move()

    def get_safe_directions(self, player1, player2):
        possible_directions = range(4)
        safe_directions = possible_directions[:]
        head = player1.segments[0].topleft

        # Prevent collisions with board edges and players
        for direction in possible_directions:
            delta = DIRECTION_DELTAS[direction]
            x = head[0] + delta['x'] * CELL_WIDTH
            y = head[1] + delta['y'] * CELL_WIDTH
            possible_head = Rect(x, y, CELL_WIDTH, CELL_WIDTH)
            if player1.has_collided(player2, head=possible_head):
                safe_directions.remove(direction)

        return safe_directions

    def heuristic(self, player, other_player):
        #state = player.get_state(other_player)
        #head = player.segments[0].topleft
        #hx,hy = head[0]/CELL_WIDTH, head[1]/CELL_WIDTH
        #assert state[hy,hx] == FRIENDLY, "Head of player not friendly"
        return len(self.get_safe_directions(player, other_player)) /
            float(len(self.get_safe_directions(other_player, player)))


    def evaluate_board(self, player, other_player, own_turn):
        player_lost = player.has_collided(other_player)
        other_player_lost = other_player.has_collided(player)
        if own_turn and player_lost:
            return -100
        elif not own_turn and other_player_lost:
            return 100
        elif player_lost or other_player_lost:
            raise Exception('Evaluation logic error')




        # Add heuristic logic here
        return self.heuristic(player, other_player)

    def minimax(self, other_player, depth):
        scores = map(lambda move:
            self.min_play(self.clone(direction=move), other_player, depth+1), 
            range(4))
        return scores.index(max(scores)) # Move with highest score

    def min_play(self, player, other_player, depth):
        outcome = self.evaluate_board(player, other_player, True)
        if outcome == 100 or outcome == -100 or depth == self.max_depth:
            return outcome

        return min(map(lambda move:
            self.max_play(player, self.clone(player=other_player, direction=move), depth+1),
            range(4)))

    def max_play(self, player, other_player, depth):
        outcome = self.evaluate_board(player, other_player, False)
        if outcome == 100 or outcome == -100 or depth == self.max_depth:
            return outcome
        return max(map(lambda move:
            self.min_play(self.clone(player=player, direction=move), other_player, depth+1),
            range(4)))
