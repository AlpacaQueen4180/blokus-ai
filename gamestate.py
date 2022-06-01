import sys
import math
import random
import copy
import numpy as np
from chess import *


class Board:
    def __init__(self, nrow, ncol):
        self.nrow = nrow
        self.ncol = ncol
        self.state = [['_'] * ncol for _ in range(nrow)]

    def update(self, player_id, placement):
        for row in range(self.nrow):
            for col in range(self.ncol):
                if(col, row) in placement:
                    self.state[row][col] = player_id

    def in_bounds(self, point):
        return 0 <= point[0] < self.ncol and 0 <= point[1] < self.nrow

    def overlap(self, placement):
        return False in [(self.state[y][x] == '_') for x, y in placement]

    def adj(self, player_id, placement):
        adjacents = []
        for x, y in placement:
            if self.in_bounds((x + 1, y)):
                adjacents += [self.state[y][x + 1] == player_id]
            if self.in_bounds((x - 1, y)):
                adjacents += [self.state[y][x - 1] == player_id]
            if self.in_bounds((x, y - 1)):
                adjacents += [self.state[y - 1][x] == player_id]
            if self.in_bounds((x, y + 1)):
                adjacents += [self.state[y + 1][x] == player_id]
        return True in adjacents

    def corner(self, player_id, placement):
        corners = []
        for x, y in placement:
            if self.in_bounds((x + 1, y + 1)):
                corners += [self.state[y + 1][x + 1] == player_id]
            if self.in_bounds((x - 1, y - 1)):
                corners += [self.state[y - 1][x - 1] == player_id]
            if self.in_bounds((x + 1, y - 1)):
                corners += [self.state[y - 1][x + 1] == player_id]
            if self.in_bounds((x - 1, y + 1)):
                corners += [self.state[y + 1][x - 1] == player_id]
        return True in corners

    def print_board(self):
        print("Current Board Layout:")
        for row in range(len(self.state)):
            for col in range(len(self.state[0])):
                print(" " + str(self.state[row][col]), end='')
            print()


class GameState:
    def __init__(self, playerid, strategy, board):
        self.playerid = playerid                    # player's id
        self.pieces: list[Shape] = []                # player's unused game piece, list of Pieces
        self.corners = set()            # current valid corners on board
        self.strategy = strategy        # player's strategy
        self.score = 0                  # player's current score
        self.is_blocked = False
        self.board = board

    def getscore(self):
        return self.score

    def getunusedpiece(self):
        return self.pieces

    def add_pieces(self, pieces):
        self.pieces = pieces

    def remove_piece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id]

    def update_player(self, piece: Shape, board: Board):
        self.score += piece.size  # If you're placing your last piece, you get +15 bonus
        if len(self.pieces) == 1:
            self.score += 15
            if piece.id == 'Pole':  # +5 extra if its the [] piece
                self.score += 5
        for c in piece.corners:  # Add the player's available corners
            if board.in_bounds(c) and not board.overlap([c]):
                self.corners.add(c)

    # Updates the corners of the player, in case the corners have been covered by another player's pieces.
    def getpossiblemoves(self, pieces: list[Shape], game):
        self.corners = set(
            [(x, y) for (x, y) in self.corners if game.board.state[y][x] == '_'])
        placements = []  # a list of possible placements
        visited = []  # a list placements (a set of points on board)
        for cr in self.corners:          # Check every available corner
            for sh in pieces:            # Check every available piece
                # Check every reference point the piece could have
                for num in range(sh.size):
                    for flip in ["h", "v"]:                         # Check every flip
                        for rot in [0, 90, 180, 270]:               # Check every rotation
                            # Create a copy to prevent an overwrite on the original
                            candidate = copy.deepcopy(sh)
                            candidate.create(num, cr)
                            candidate.flip(flip)
                            candidate.rotate(rot)
                            # If the placement is valid and new
                            if game.valid_move(self, candidate.points):
                                if not set(candidate.points) in visited:
                                    placements.append(candidate)
                                    visited.append(set(candidate.points))
        return placements
