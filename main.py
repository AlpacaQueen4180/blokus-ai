from gamestate import *
from agent import Agent
import screen
from pprint import pprint


if __name__ == '__main__':
    player_id = screen.check_id()
    print(player_id)
    players = [None] * PLAYER_NUM
    players[player_id] = Agent(index=player_id)
    game = Blokus(players, BOARD_ROW, BOARD_COL)
    player: Player = game.players[player_id]
    while True:
        screen.get_board_from_screen(game.board)
        game.board.print()
        # act = game.get_next_move(player_id)
        player.update_corner()
        # print(act)
        # player.remove_piece(act.shape)
        print(player)
        input()
    # game.board.print()
