import sys
import math
import random
import copy
from typing import Literal
from chess import *
from dataclasses import dataclass

from colorama import init, Back
init()

BOARD_COL = 20
BOARD_ROW = 20
PLAYER_NUM = 4

class Board:
    def __init__(self, nrow, ncol):
        """
        (0, 0) left-bottom, (row, col), top-right
        """
        self.nrow = nrow
        self.ncol = ncol
        self.state = [['_'] * ncol for _ in range(nrow)]

    def place(self, playerid, placement):
        for row in range(self.nrow):
            for col in range(self.ncol):
                if(col, row) in placement:
                    self.state[col][row] = playerid

    def inbounds(self, placement):
        """Check if placement inbounds"""
        # return 0 <= point[0] < self.ncol and 0 <= point[1] < self.nrow
        for x, y in placement:
            if not (0 <= x < self.ncol and 0 <= y < self.nrow):
                return False
        return True

    def overlap(self, placement):
        """Check if placement overlap"""
        return False in [self.state[y][x] == '_' for x, y in placement]

    def adj(self, playerid, placement):
        """Check if placement adj to own piece"""
        adjacents = []
        for x, y in placement:
            if self.inbounds((x + 1, y)):
                adjacents += [self.state[y][x + 1] == playerid]
            if self.inbounds((x - 1, y)):
                adjacents += [self.state[y][x - 1] == playerid]
            if self.inbounds((x, y - 1)):
                adjacents += [self.state[y - 1][x] == playerid]
            if self.inbounds((x, y + 1)):
                adjacents += [self.state[y + 1][x] == playerid]
        return True in adjacents

    def corner(self, playerid, placement):
        """Check if placed at corner"""
        corners = []
        for x, y in placement:
            if self.inbounds((x + 1, y + 1)):
                corners += [self.state[y + 1][x + 1] == playerid]
            if self.inbounds((x - 1, y - 1)):
                corners += [self.state[y - 1][x - 1] == playerid]
            if self.inbounds((x + 1, y - 1)):
                corners += [self.state[y - 1][x + 1] == playerid]
            if self.inbounds((x - 1, y + 1)):
                corners += [self.state[y + 1][x - 1] == playerid]
        return True in corners

    def print(self):
        print("Current Board Layout:")
        for row in reversed(range(self.nrow)):
            for col in range(self.ncol):
                match self.state[col][row]:
                    case 0: print(Back.BLUE + '  ', end='')
                    case 1: print(Back.GREEN + '  ', end='')
                    case 2: print(Back.RED + '  ', end='')
                    case 3: print(Back.YELLOW + '  ', end='')
                    case _: print(Back.RESET + '--', end='')      
            print(Back.RESET)


class Player:
    def __init__(self, id: int, agent, board: Board):
        self.id = id                    # player's id
        # player's unused game piece, list of Pieces
        self.pieces = copy.copy(SHAPES_ID)
        self.corners = set()            # current valid corners on board
        self.agent = agent              # player's strategy
        self.score = 0                  # player's current score
        self.is_blocked = False         #
        self.board = board              # The game board

    def __repr__(self) -> str:
        return f"""
        Player {self.id}:
            Score: {self.score}
            Agent: {self.agent}
            Pieces: {self.pieces}
            Placed Pieces: {SHAPES_ID - self.pieces}
            Corners: {self.corners}
        """

    def get_score(self):
        return self.score

    def get_unused_piece(self):
        return self.pieces

    def add_pieces(self, pieces):
        self.pieces.add(pieces)

    def remove_piece(self, piece_id: str):
        self.pieces.remove(piece_id)

    def add_corner(self, corner):
        self.corners.add(corner)

    def remove_corner(self, corner):
        self.corners.remove(corner)

    def update_corner(self):
        corners = set()
        board = self.board
        for y in range(BOARD_ROW):
            for x in range(BOARD_COL):
                if self.board.state[y][x] != self.id: continue
                for dy, dx in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    if not board.inbounds([(y+dy, x+dx)]) or self.board.state[y + dy][x + dx] != '_': continue
                    l = []
                    for ey, ex in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        if not board.inbounds([(y+dy+ey, x+dx+ex)]): continue
                        l.append(self.board.state[y + dy + ey][x + dx + ex])
                    if self.id not in l: 
                        corners.add((y+dy, x+dx))
        self.corners = corners

    def update_player(self, piece: Shape):
        """
        Place piece, update score, corners
        """
        self.score += piece.size
        # If you're placing your last piece, you get +15 bonus
        if len(self.pieces) == 1:
            self.score += 15
            if piece.id == 'I1':  # +5 extra if the piece is I1
                self.score += 5
        # Add the player's available corners
        for c in piece.corners:  
            print(c)
            if self.board.inbounds([c]) and not self.board.overlap([c]):
                self.add_corner(c)
        self.remove_piece(piece.id)
        for point in piece.points:
            if point in self.corners: self.remove_corner(point)


class Blokus:
    def __init__(self, players = [], row = 20, col = 20):
        self.player_agent = players
        self.player_num = len(players)              # list of players in the game
        self.rounds = 0                        # current round in the game
        self.board = Board(row, col)                  # the game's board
        self.previous = 0                   # previous total available moves from all players
        # counter for how many times the total available moves are the same by checking previous round
        self.repeat = 0
        self.winplayer = 0                  # winner
        self.init_players()

    def init_players(self):
        self.players = [Player(i, agent, self.board) for i, agent in enumerate(self.player_agent)]
        corners = [(0, self.board.nrow-1), (0, 0), (self.board.ncol-1, 0), (self.board.ncol-1, self.board.nrow-1)]
        for i, corner in enumerate(corners):
            self.players[i].corners.add(corner)

    def place(self, player_id, action: Action):
        shape: Shape = SHAPES_CLASS[action.shape](*action.coord)
        print(shape.points)
        # shape.place((0, 19), (0, 19))
        if not self.valid_move(player_id, shape.points):
            print("not a valid move")
            return
        self.board.place(player_id, shape.points)
        self.players[player_id].update_player(shape)
        print(f"placed {shape.id} at {action.coord}")
        self.board.print()

    def winner(self):
        """
        Check for the winner (or tied) in the game and return the winner's id. Or return nothing if the game can still progress
        """
        # get all possible moves for all players
        moves = [p.get_possible_moves(p.pieces, self) for p in self.players]

        # check how many rounds the total available moves from all players are the same and increment the counter if so
        if self.previous == sum([len(mv) for mv in moves]):
            self.repeat += 1
        else:
            self.repeat = 0

        # if there is still moves possible or total available moves remain static for too many rounds (repeat reaches over a certain threshold)
        if False in [len(mv) == 0 for mv in moves] and self.repeat < 4:
            self.previous = sum([len(mv) for mv in moves])
            return None                         # Nothing to return to continue the game
        else:                                   # No more move available, the game ends order the players by highest score first
            candidates = [(p.score, p.id) for p in self.players]
            candidates.sort(key=lambda x: x[0], reverse=True)
            highest = candidates[0][0]
            result = [candidates[0][1]]

        # Check for tied score
        for candidate in candidates[1:]:
            if highest == candidate[0]:
                result += [candidate[1]]
        return result

    def get_possible_moves(self, player_id):
        # Updates the corners of the player, in case the corners have been covered by another player's pieces.
        # self.corners = set(
        #     [(x, y) for (x, y) in self.corners if game.board.state[y][x] == '_'])
        placements = []  # a list of possible placements
        visited = []  # a list placements (a set of points on board)
        player = self.players[player_id]
        for cr in player.corners:          # Check every available corner
            # for sh in player.pieces:           # Check every available piece
            sh = 'I2'
            # Check every reference point the piece could have
            shape: Shape = SHAPES_CLASS[sh](0, 0)
            for i in range(shape.size):
                for flip in [False, True]:             # Check every flip
                    for rot in range(4):               # Check every rotation
                        # Create a copy to prevent an overwrite on the original
                        if flip: shape.flip()
                        shape.rotate(rot)
                        shape.place(shape.points[i], cr)
                        # If the placement is valid and new
                        if self.valid_move(player.id, shape.points):
                            if set(shape.points) not in visited:
                                placements.append((shape.id, shape.points))
                                visited.append(set(shape.points))
        return placements

    def get_next_move(self, player_id) -> Action:
        return self.players[player_id].agent.get_next_move(self)

    def valid_move(self, player_id, placement):
        if self.rounds < len(self.players):             # Check for starting corner
            return (self.board.inbounds(placement)
                    and not self.board.overlap(placement)
                    and (True in [(pt in self.players[player_id].corners) for pt in placement]))
        return (self.board.inbounds(placement)
                and not self.board.overlap(placement)
                and not self.board.adj(player_id, placement)
                and self.board.corner(player_id, placement))

    def play(self):        
        winner = self.winner()                  # get game status
        if winner is None:                      # no winner, the game continues
            current = self.players[0]           # get current player
            # get the next move based on the player's strategy
            act = current.next_move(self)
            if act is not None:            # if there a possible proposed move check if the move is valid
                # update the board and the player status
                self.place(current.id, act)
        # put the current player to the back of the queue
            first = self.players.pop(0)
            self.players += [first]
            self.rounds += 1                                    # update game round
        # a winner (or tied) is found
        else:
            if len(winner) == 1:                                # if the game results in a winner
                self.winplayer = winner[0]
                print('Game over! The winner is: ' + str(winner[0]))
            else:                                               # if the game results in a tie
                print('Game over! Tied between players: ' +
                      ', '.join(map(str, winner)))
