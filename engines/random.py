"""
Eric P. Nichols
Feb 8, 2008

This is a human move engine. It simply reads and validates user input
to get the move to make.
"""

from engines import Engine
import random

class RandomEngine(Engine):

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        legal_moves = board.get_legal_moves(color)

    
        return random.choice(legal_moves)

engine = RandomEngine