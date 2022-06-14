import copy
from gamestate import Blokus
from chess import *


class Agent:

    def __init__(self, index=0, depth=2) -> None:
        self.index = index
        self.depth = depth

    def get_next_move(self, game_state: Blokus) -> Action:
        """
        Gets the next move using Minimax search.
        """
        num_player = game_state.player_num
        actions = game_state.get_possible_moves(self.index)
        print(actions)
        next_agent = (self.index + 1) % num_player
        depth = self.depth
        if next_agent == self.index: depth -= 1
        alpha = v = -float('inf')
        beta = float('inf')
        for i, action in enumerate(actions):
            new_state = game_state.get_next_state(action)
            new_v = self._v(new_state, next_agent, depth, alpha, beta)
            if new_v > v:
                v = new_v
                best_i = i
            alpha = max(alpha, v)
        best_action = actions[best_i]
        return best_action

    def eval_fn(self, game_state: Blokus) -> int:
        """
        Return a value based on the game state.
        """
        player = game_state.players[self.index]
        val = len(player.corners) + player.score
        return val

    def _v(self, new_state: Blokus, agent_index, depth, alpha, beta):
        """
        Do alpha beta max
        """
        if depth == 0:
            return self.eval_fn(self.index, new_state)
        actions = new_state.get_possible_moves(self.index)
        next_agent = (self.index + 1) % new_state.player_num
        if next_agent == self.index: depth -= 1
        # TODO
        
