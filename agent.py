from gamestate import Blokus, Action
from chess import *


class Agent:

    def __init__(self, index=0, depth=2) -> None:
        self.index = index
        self.depth = depth

    def get_next_move(self, game_state: Blokus) -> Action:
        """
        Gets the next move using Minimax search.
        """
        num_player = len(game_state.players)
        actions = game_state.players[self.index].get_possible_moves(game_state)
        next_agent = (self.index + 1) % num_player
        depth = self.depth
        return Action(Shape())

    def eval_fn(self, game_state: Blokus) -> int:
        """
        Return a value based on the game state.
        """
