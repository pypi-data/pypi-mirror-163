# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 14:54:55 2022

@author: richa
"""
from dataclasses import dataclass
from typing import Dict
from typing import List

from .algorithm import ReversibleMove
from .consts import EARLY_VALUES
from .piece import King
from .piece import Piece
from .piece import Queen

@dataclass
class Team:
    """Contains all the pieces for a side"""

    pieces: List[Piece]
    representation: str

    def __post_init__(self):
        self.king = [x for x in self.pieces if isinstance(x, King)][0]
        self.queen = [x for x in self.pieces if isinstance(x, Queen)][0]
        self.sort_pieces(EARLY_VALUES)

    def __repr__(self):
        return self.representation

    def sort_pieces(self, values: Dict[str, int]):
        """Sorts the pieces by the specified values dict"""
        self.pieces.sort(key=lambda x: values.get(x.representation[0]), reverse=True)

    def compute_all_moves(self, board):
        """Returns all valid moves for all pieces passed in"""
        return [(piece, move) for piece in self.pieces
                for move in piece.compute_valid_moves(board)]

    def compute_valid_moves(self, board, enemy_pieces):
        """Returns moves not resulting in a check of the allied king"""
        valid_moves = []
        for piece, move in self.compute_all_moves(board):
            with ReversibleMove(board, piece, move.position, enemy_pieces):
                if not self.in_check(board, enemy_pieces):
                    valid_moves.append((piece, move))
        #random.shuffle(valid_moves) #HACK to avoid the same game consistently
        valid_moves.sort(key=lambda x: x[1].can_capture, reverse=True)
        return valid_moves

    def in_check(self, board, enemy_pieces) -> bool:
        """Returns True if any enemy pieces can capture at the specified position"""
        #optimization: True for all truthy elements.
        #Directly checking capture state would be slower
        return any(True for x in enemy_pieces if x.can_capture_at(board, self.king.position))
