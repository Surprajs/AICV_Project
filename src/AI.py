from Const import Const
from Board import Board, Field
from TUIController import TUIController
from copy import deepcopy
from Tree import Tree


class AI:
    def __init__(self, board, white_ai=False, depth=5):
        self.board = board
        self.white_ai = white_ai
        self.depth = depth
        self.tree = None

    def get_score(self, this_board=None):
        if not this_board:
            this_board = self.board
        score = 0
        if this_board.is_draw():
            return score
        if this_board.is_end():
            if this_board.get_turn() ^ self.white_ai:
                return Const.SCORE_WIN
            else:
                return Const.SCORE_LOST


        weights = {Field.white : -30, 
                  Field.black : 30,
                  Field.white_king : -50, 
                  Field.black_king : 50
                  }

        for row in range(Const.ROW):
            for col in range(Const.COL):
                if (row+col)%2:
                    square = this_board.get_square(col,row)
                    score += weights.get(square, 0)
                    if square == Field.white:
                        score -= 7-row
                    elif square == Field.black:
                        score += row
        return -score if self.white_ai else score



    def go_deeper(self, board, current_depth, node):
        if current_depth == self.depth:
            return


        if not node.is_external():
            for child in node.get_children():
                self.go_deeper(deepcopy(board), current_depth+1, child)
        else:
            _, moves = board.count_moves()
            _, captures = board.count_captures()
            
            if captures:
                for capture in captures:
                    start_col, start_row, end_col, end_row = capture
                    new_board = deepcopy(board)
                    new_board.move(start_col, start_row, end_col, end_row)
                    child = node.add_child(new_board)
                    self.go_deeper(new_board, current_depth+1, child)
                    
            if moves:
                for move in moves:
                    start_col, start_row, end_col, end_row = move
                    new_board = deepcopy(board)
                    new_board.move(start_col, start_row, end_col, end_row)
                    child = node.add_child(new_board)
                    self.go_deeper(new_board, current_depth+1, child)



    def play(self):
        if not self.tree:
            self.tree = Tree(deepcopy(self.board))
        else:
            # cut other than opponent's move
            pass

        
        self.go_deeper(self.board, 0, self.tree)
        # get best move
        # do best move  
        # cut the rest (other than best move)
        




if __name__ == "__main__":
    b1 = Board()
    ai = AI(b1)
    t1 = TUIController(b1, ai, True)

    t1.play()

