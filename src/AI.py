from Const import Const
from Board import Board, Field
from TUIController import TUIController
from copy import deepcopy
from Tree import Tree


class AI:
    def __init__(self, board, white_ai=True, depth=2):
        self.board = board
        self.white_ai = white_ai
        self.depth = depth
        self.tree = None

    def get_ai_color(self):
        return self.white_ai

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



    def minmax(self, current_depth, node, alpha, beta, is_maximizing):
        best_node = None
        if current_depth == self.depth:
            # print(alpha)
            # print(beta)
            # print("here???")
            return self.get_score(node.get_value()), None


        if not node.is_external():
            # print("AAA")
            minmax_score = Const.SCORE_LOST-1 if is_maximizing else Const.SCORE_WIN+1
            for child in node.get_children():
                score, _ = self.minmax(current_depth+1, child, alpha, beta, not is_maximizing)
                if is_maximizing:
                    if score > minmax_score:
                        minmax_score = score
                        alpha = max(alpha, score)
                        best_node = child
                else:
                    if score < minmax_score:
                        minmax_score = score
                        beta = min(beta, score)
                        best_node = child

                # if beta <= alpha:
                #     break
            return score, best_node
        else:
            _, moves = node.get_value().count_moves()
            _, captures = node.get_value().count_captures()                

            moves.extend(captures)
            if moves:
                minmax_score = Const.SCORE_LOST-1 if is_maximizing else Const.SCORE_WIN+1
                for move in moves:
                    new_board = deepcopy(node.get_value())

                    # print(f"move: {move}")
                    for m in move:
                        # print(m)
                        start, end = m
                        start_col, start_row = start
                        end_col, end_row = end
                        new_board.move(start_col, start_row, end_col, end_row)
                    child = node.add_child(new_board)
                    score, _ = self.minmax(current_depth+1, child, alpha, beta, not is_maximizing)
                    if is_maximizing:
                        if score > minmax_score:
                            minmax_score = score
                            alpha = max(alpha, score)
                            best_node = child
                    else:
                        if score < minmax_score:
                            minmax_score = score
                            beta = min(beta, score)
                            best_node = child

                    if beta <= alpha:
                        break
                # print("kurwa")
                # print(best_node)
                return minmax_score, best_node
            else:
                return self.get_score(node.get_value()), best_node


    def play(self):
        print(self.depth)
        if not self.tree:
            self.tree = Tree(deepcopy(self.board))
        else:
            self.tree = self.tree.cut_tree(self.board.get_board())
            if not self.tree:
                self.tree = Tree(deepcopy(self.board))
        
        _, node = self.minmax(0, self.tree, Const.SCORE_LOST, Const.SCORE_WIN, True)
        # start_col, start_row, end_col, end_row = move
        # self.board.move(start_col, start_row, end_col, end_row)
        # print(node is self.tree)
        # print(self.board.get_turn())
        self.board.change_board(node.get_value())
        # print(self.board.get_turn())
        # self.board.print_board()
        # print(len(self.tree.get_children()))
        self.tree = self.tree.cut_tree(self.board.get_board())
        




if __name__ == "__main__":
    b1 = Board()
    ai = AI(b1, depth=6)
    t1 = TUIController(b1, ai,True)
    # ai.play()
    t1.play()

