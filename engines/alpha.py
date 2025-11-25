from __future__ import absolute_import
from engines import Engine
from copy import deepcopy
import random
class AlphaEngine(Engine):
    #set the infinity
    INFINITY = float('inf')
    WEIGHTS = [4, -3, 2, 2, 2, 2, -3, 4,
               -3, -4, -1, -1, -1, -1, -4, -3,
               2, -1, 1, 0, 0, 1, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 1, 0, 0, 1, -1, 2,
               -3, -4, -1, -1, -1, -1, -4, -3,
               4, -3, 2, 2, 2, 2, -3, 4]
    num_node = 0
    num_dup = 0
    node_list = []
    branch_list = [0,0,0]
    
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = False
        self.ply_maxmin = 4
        self.ply_alpha = 4
        print("Call alpha beta pruning\n")

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Return a move for the given color that maximizes the difference in 
        number of pieces for that color. """
        # Get a list of all legal moves.
        # moves = board.get_legal_moves(color)

        # Return the best move according to our simple utility function:
        # which move yields the largest different in number of pieces for the
        # given color vs. the opponent?
        # print(self.ply_maxmin," ", self.ply_alpha," ", self.alpha_beta)
        if (self.alpha_beta == False):
           score, finalmove = self._minmax(board, color, move_num, time_remaining, time_opponent, self.ply_maxmin)
        else:
           score, finalmove = self._minmax_with_alpha_beta(board, color, move_num, time_remaining, time_opponent, self.ply_alpha)
       # print "final move" + str(finalmove) + "final score: " + str(score) + "number of nodes:" + str(StudentEngine.num_node) + "number of duplicate" + str(StudentEngine.num_dup) + str(StudentEngine.node_list)# + str(self.cornerweight(color, board)) + "get cost:" + str(self._get_cost(board, color))
        #print "ply = 3" + str(StudentEngine.branch_list[0]) + "ply =2" + str(StudentEngine.branch_list[1]) + "ply = 1" + str(StudentEngine.branch_list[2])
        return finalmove
        #maxmin function created by hyl
    def _minmax(self, board, color, move_num, time_remaining, time_opponent, ply):
        #need to get all the legal moves
        #def value(board):
        #    return self.minmax(board, -color, move_num, time_remaining, time_opponent, ply-1)[0]
        #if ply == 0:
        #   return board.count(color), None
        moves = board.get_legal_moves(color)
        if move_num > 7 and move_num < 15:
           self.ply_maxmin = 2
        if time_remaining < 20:
           return (0, max(moves, key=lambda move: self.greedy(board, color, move)) )

        #print "leagal move" + str(moves)
        if not isinstance(moves, list):
           score = self.heuristic(board, color, move_num)
           return score,None
        #if time_remaining < 10:
        #   return (0, max(moves, key=lambda move: self.greedy(board, color, move)) )
        #print ply
        return_move = moves[0]
        bestscore = - AlphaEngine.INFINITY
        #       print "using minmax best score:"+ str(bestscore)
        #ply = 4
        #will define ply later;
        for move in moves:
            #if move in StudentEngine.node_list:
            #   StudentEngine.num_dup += 1
            #if move not in StudentEngine.node_list:
            #   StudentEngine.node_list.append(move)
            #StudentEngine.num_node += 1 
            #StudentEngine.branch_list[0] += 1
            newboard = deepcopy(board)
            newboard.execute_move(move,color)

            score = self.min_score(newboard, -color, move_num, ply-1)
            if score > bestscore:
                bestscore = score
                return_move = move
                #print "return move" + str(return_move) + "bestscore" + str(bestscore)
        #newboard = deepcopy(board)
        #return max((value(newboard.execute_move(m, color)),m) for m in moves)
        return (bestscore,return_move)

    #MAX_VALUE = StudentEngine.INFINITY
    #MIN_VALUE = -MAX_VALUE


    def max_score(self, board, color, move_num, ply):
        #print "move_num" + str(move_num)
        moves = board.get_legal_moves(color)
        #if not isinstance(moves, list):
        #   return board.count(color)
        if ply == 0:
           #StudentEngine.num_node += 1
           return self.heuristic(board, color, move_num)
        bestscore = -AlphaEngine.INFINITY
        for move in moves:
            #if move in StudentEngine.node_list:
            #    StudentEngine.num_dup += 1
            #if move not in StudentEngine.node_list:
            #    StudentEngine.node_list.append(move)
            #if (ply == 2):
            #     StudentEngine.branch_list[1] += 1
            #if (ply == 1):
            #     StudentEngine.branch_list[2] += 1            
            #StudentEngine.num_node += 1        
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.min_score(newboard, -color, move_num, ply-1)
            if score > bestscore:
                bestscore = score
        return bestscore

    def min_score(self, board, color, move_num, ply):
        #print "move_num" + str(move_num)
        moves = board.get_legal_moves(color)
        #if not isinstance(moves, list):
        #   return board.count(color)
        if ply == 0:
           #StudentEngine.num_node += 1
           return self.heuristic(board, color, move_num)
        bestscore = AlphaEngine.INFINITY
        for move in moves:
            if move in AlphaEngine.node_list:
                AlphaEngine.num_dup += 1
            if move not in AlphaEngine.node_list:
                AlphaEngine.node_list.append(move)
            #if (ply == 2):
            #     StudentEngine.branch_list[1] += 1
            #if (ply == 1):
            #     StudentEngine.branch_list[2] += 1            
            #StudentEngine.num_node += 1
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.max_score(newboard, -color, move_num, ply-1)
            if score < bestscore:
                bestscore = score
        return bestscore

    def _minmax_with_alpha_beta(self, board, color, move_num, time_remaining, time_opponent, ply):
        moves = board.get_legal_moves(color)
        #print "leagal move" + str(moves)
        if not isinstance(moves, list):
           score = board.count(color)
           return score, None
        moves.sort(key=lambda move: self.greedy(board, color, move), reverse=False)
        #moves = moves[:6] # Chỉ kiểm tra 6 node đầu 
        #print ply
        return_move = moves[0]
        bestscore = - AlphaEngine.INFINITY
        #print "using alpha_beta best score:"+ str(bestscore)
        #ply = 4
        #will define ply later;
        #if move_num > 7 and move_num < 15:
        #   StudentEngine.ply_maxmin = 2;
        if time_remaining < 5:
           return (0, max(moves, key=lambda move: self.greedy(board, color, move)) )
        for move in moves:
            #if move in StudentEngine.node_list:
            #    StudentEngine.num_dup += 1
            #if move not in StudentEngine.node_list:
            #    StudentEngine.node_list.append(move)
            #StudentEngine.num_node += 1
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            AlphaEngine.branch_list[0] +=1
            score = self.min_score_alpha_beta(newboard, -color, move_num, ply-1, -AlphaEngine.INFINITY, AlphaEngine.INFINITY)
            if score > bestscore:
               bestscore = score
               return_move = move
               #print "return move" + str(return_move) + "best score" + str(bestscore)

        return (bestscore,return_move)

    def max_score_alpha_beta(self, board, color, move_num, ply, alpha, beta):
        if ply == 0:
            #StudentEngine.num_node +=1
            return self.heuristic(board, color, move_num)
        bestscore = -AlphaEngine.INFINITY
        moves = board.get_legal_moves(color)
        #moves.sort(key=lambda move: self.greedy(board, color, move), reverse=True)

        for move in moves:

            #if (ply == 2):
            #     StudentEngine.branch_list[1] += 1
            #if (ply == 1):
            #     StudentEngine.branch_list[2] += 1

            #if move in StudentEngine.node_list:
            #    StudentEngine.num_dup += 1
            #if move not in StudentEngine.node_list:
            #    StudentEngine.node_list.append(move)            
            #StudentEngine.num_node += 1
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.min_score_alpha_beta(newboard, -color, move_num, ply-1, alpha, beta)
            if score > bestscore:
                bestscore = score
            if bestscore >= beta:
                return bestscore
            alpha = max (alpha,bestscore)
        return bestscore

    def min_score_alpha_beta(self, board, color, move_num, ply, alpha, beta):
        if ply == 0:
             #StudentEngine.num_node +=1
            return self.heuristic(board, color, move_num)
        bestscore = AlphaEngine.INFINITY
        moves = board.get_legal_moves(color)
        #moves.sort(key=lambda move: self.greedy(board, color, move), reverse=True)

        for move in moves:
              #if (ply == 2):
              #   StudentEngine.branch_list[1] += 1
              #if (ply == 1):
              #   StudentEngine.branch_list[2] += 1
              #if move in StudentEngine.node_list:
              #   StudentEngine.num_dup += 1
              #if move not in StudentEngine.node_list:
              #   StudentEngine.node_list.append(move)
              #StudentEngine.num_node += 1
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            score = self.max_score_alpha_beta(newboard, -color, move_num, ply-1, alpha, beta)
            if score < bestscore:
                bestscore = score
            if bestscore <= alpha:
                return bestscore
            beta = min(beta,bestscore)
        return bestscore

    def heuristic(self, board, color, move_num):
        move_count = move_num  
        mobility = len(board.get_legal_moves(color)) - len(board.get_legal_moves(-color))
        frontier = -self.frontier_discs(board, color)
        corner = self.cornerweight(color, board)
        piece_diff = self._get_cost(board, color)

        if move_count < 20:  
            return 4 * mobility + 3 * frontier + 2 * corner
        elif move_count < 50:  
            return 3 * mobility + 2 * frontier + 3 * corner + piece_diff
        else:  
            return 5 * piece_diff + 3 * corner

    def frontier_discs(self, board, color):
        frontier = 0
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for r in range(8):
            for c in range(8):
                if board[r][c] == color:
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == 0:
                            frontier += 1
                            break
        return frontier
    
    def cornerweight(self, color, board):
        total = 0
        i = 0
        while i < 64:
            if board[i//8][i%8] == color:
               total += AlphaEngine.WEIGHTS[i]
               #print "weights" + str(i) + "number:"+ str(StudentEngine.WEIGHTS[i])
            if board[i//8][i%8] == -color:
               total -= AlphaEngine.WEIGHTS[i]
               #print "weights" + str(i) + "number:"+ str(StudentEngine.WEIGHTS[i])
            i += 1
        #print "cornerweight" + str(total)
        return total

    def greedy(self, board, color, move):
        """ Return the difference in number of pieces after the given move 
        is executed. """

        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))

        # Return the difference in number of pieces
        return num_pieces_me - num_pieces_op

    def _get_cost(self, board, color):
        """ Return the difference in number of pieces after the given move 
        is executed. """

        # Create a deepcopy of the board to preserve the state of the actual board
        #newboard = deepcopy(board)
        #newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board
        num_pieces_op = board.count(-color)
        num_pieces_me = board.count(color)
        #print "_get_cost" + str(num_pieces_me - num_pieces_op)
        # Return the difference in number of pieces
        return num_pieces_me - num_pieces_op

engine = AlphaEngine
