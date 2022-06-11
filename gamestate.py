import sys
import math
import random
import copy
import numpy as np
from chess import *
from dataclasses import dataclass


@dataclass
class Action:
    shape: Shape
    rotate: int = 0
    flip: bool = False


class Board:
    def __init__(self, nrow, ncol):
        self.nrow = nrow
        self.ncol = ncol
        self.state = [['_'] * ncol for _ in range(nrow)]

    def update(self, playerid, placement):
        for row in range(self.nrow):
            for col in range(self.ncol):
                if(col, row) in placement:
                    self.state[row][col] = playerid

    def inbounds(self, point):
        return 0 <= point[0] < self.ncol and 0 <= point[1] < self.nrow

    def overlap(self, placement):
        return False in [(self.state[y][x] == '_') for x, y in placement]

    def adj(self, playerid, placement):
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

    def printboard(self):
        print("Current Board Layout:")
        for row in range(len(self.state)):
            for col in range(len(self.state[0])):
                print(" " + str(self.state[row][col]), end='')
            print()


class GameState:
    def __init__(self, playerid, strategy, board):
        self.playerid = playerid                    # player's id
        # player's unused game piece, list of Pieces
        self.pieces: list[Shape] = []
        self.corners = set()            # current valid corners on board
        self.strategy = strategy        # player's strategy
        self.score = 0                  # player's current score
        self.is_blocked = False
        self.board = board

    def getscore(self):
        return self.score

    def getunusedpiece(self):
        return self.pieces

    def addpieces(self, pieces):
        self.pieces = pieces

    def removepiece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id]

    def updateplayer(self, piece: Shape, board: Board):
        self.score += piece.size  # If you're placing your last piece, you get +15 bonus
        if len(self.pieces) == 1:
            self.score += 15
            if piece.id == 'Pole':  # +5 extra if its the [] piece
                self.score += 5
        for c in piece.corners:  # Add the player's available corners
            if board.inbounds(c) and not board.overlap([c]):
                self.corners.add(c)

    # Updates the corners of the player, in case the corners have been covered by another player's pieces.
    def get_possible_moves(self, game):
        self.corners = set(
            [(x, y) for (x, y) in self.corners if game.board.state[y][x] == '_'])
        placements = []  # a list of possible placements
        visited = []  # a list placements (a set of points on board)
        for cr in self.corners:          # Check every available corner
            for sh in self.pieces:            # Check every available piece
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
                            if game.validmove(self, candidate.points):
                                if not set(candidate.points) in visited:
                                    placements.append(candidate)
                                    visited.append(set(candidate.points))
        return placements

    def nextmove(self, game):
        return self.strategy(self, game)


class Blokus:
    def __init__(self, players: list[GameState], board: Board):
        self.players = players              # list of players in the game
        self.rounds = 0                     # current round in the game
        self.board = board                  # the game's board
        self.previous = 0                   # previous total available moves from all players
        # counter for how many times the total available moves are the same by checking previous round
        self.repeat = 0
        self.winplayer = 0                  # winner

    def winner(self) -> list[GameState] | None:
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

    def valid_move(self, player, placement):
        if self.rounds < len(self.players):             # Check for starting corner
            return not ((False in [self.board.inbounds(pt) for pt in placement])
                        or self.board.overlap(placement)
                        or not (True in [(pt in player.corners) for pt in placement]))
        return not ((False in [self.board.inbounds(pt) for pt in placement])
                    or self.board.overlap(placement)
                    or self.board.adj(player.id, placement)
                    or not self.board.corner(player.id, placement))

    def play(self):
        # At the beginning of the game, it should give the players their pieces and a corner to start.
        if self.rounds == 0:                    # set up starting corners and players' initial pieces
            maxx = self.board.ncol - 1
            maxy = self.board.nrow - 1
            starts = [(0, 0), (maxx, maxy), (0, maxy), (maxx, 0)]
            for i in range(len(self.players)):
                self.players[i].addpieces(list(self.allpieces))
                self.players[i].startcorner(starts[i])
        winner = self.winner()                  # get game status
        if winner is None:                      # no winner, the game continues
            current = self.players[0]           # get current player
            # get the next move based on the player's strategy
            proposal = current.nextmove(self)
            if proposal is not None:            # if there a possible proposed move check if the move is valid
                # update the board and the player status
                if self.valid_move(current, proposal.points):
                    self.board.update(current.id, proposal.points)
                    current.updateplayer(proposal, self.board)
                    # remove used piece
                    current.removepiece(proposal)
                else:                                           # end the game if an invalid move is proposed
                    raise Exception(
                        "Invalid move by player " + str(current.id))
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
