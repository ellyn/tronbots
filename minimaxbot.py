from player import *
from constants import *
from heuristic import *
import timeit
import random


class MinimaxBot(Player):
    """ This bot uses the well-known Minimax algorithm for its strategy,
    along with alpha-beta pruning to remove suboptimal branches.

    We use the following heuristic function to evaluate states:
    <To be done>

    For the leaves of the game tree, we consider win states to be 1
    and losses to be -1.
    """

    def __init__(self, color, player_num, pruning=True, depth=1, heuristic=CHAMBER):
        Player.__init__(self, color, player_num)
        self.heuristic = heuristic
        self.pruning = pruning
        self.max_depth = depth # Max depth to explore for game tree

    def choose_move(self, other_player):
        self.set_direction(self.minimax(other_player, 0))
        self.move()

    def evaluate_board(self, player, opponent, turn):
        player_lost = player.has_collided(opponent)
        opponent_lost = opponent.has_collided(player)
        if (turn == FRIENDLY):
            if player_lost:
                return LOSE
            if opponent_lost:
                return WIN
        if (turn == OPPONENT):
            if opponent_lost:
                return WIN
            if player_lost:
                return LOSE

        if self.heuristic == SIMPLE_RATIO:
            return simple_ratio_heuristic(player, opponent)

        if self.heuristic == VORONOI:
            return voronoi_heuristic(player, opponent)

        if self.heuristic == CHAMBER:
            return chamber_heuristic(player,opponent)

        raise Exception("Heuristic Not Implemented")

    def minimax(self, opponent, depth):
        #print "Minimaxing for player#" + str(self.player_num)
        start_timer = timeit.default_timer()
        scores = [LOSE]*4
        moves = [UP,DOWN,LEFT,RIGHT]
        random.shuffle(moves)
        max_score = LOSE
        for move in moves:
            if not self.direction_valid(move):
                continue
            scores[move] = self.min_play(self.clone(direction=move), opponent, depth+1, max_score, WIN)
            max_score = max(max_score, scores[move])
            if self.pruning and max_score >= WIN:
                break
        total_time = timeit.default_timer() - start_timer
        #print total_time
        #ret = scores.index(max(scores))
        #print "chose from: " + str(scores)
        return scores.index(max(scores)) # Move with highest score

    def min_play(self, player, opponent, depth, alpha, beta):
        outcome = self.evaluate_board(player, opponent, OPPONENT)
        if outcome == WIN or outcome == LOSE or depth == self.max_depth:
            return outcome
        min_score = WIN
        for move in range(4):
            if not opponent.direction_valid(move):
                continue
            cloned_opponent = self.clone(player=opponent, direction=move)
            cur_val = self.max_play(player, cloned_opponent, depth+1, alpha, beta)
            min_score = min(cur_val, min_score)
            beta = min(beta, min_score)
            if self.pruning and beta <= alpha:
                break
            if min_score == WIN:
                return WIN
        return min_score

    def max_play(self, player, opponent, depth, alpha, beta):
        outcome = self.evaluate_board(player, opponent, FRIENDLY)
        if outcome == WIN or outcome == LOSE or depth == self.max_depth:
            return outcome

        max_score = LOSE
        for move in range(4):
            if (not player.direction_valid(move)):
                continue
            cloned_player = self.clone(player=player, direction=move)
            cur_val = self.min_play(cloned_player, opponent, depth+1, alpha, beta)
            max_score = max(cur_val, max_score)
            alpha = max(max_score, alpha)
            if self.pruning and beta <= alpha:
                break
            if max_score == WIN:
                return WIN
        return max_score
