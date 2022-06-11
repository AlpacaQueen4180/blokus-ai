from gamestate import *

BOARD_COL = 20
BOARD_ROW = 20
PLAYER_NUM = 4
ALL_SHAPE

if __name__ == '__main__':
    board = Board(BOARD_COL, BOARD_COL)
    players = [GameState(i, 0, board) for i in range(PLAYER_NUM)]
    game = Blokus(players, board)