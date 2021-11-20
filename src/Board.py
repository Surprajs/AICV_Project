from enum import Enum
from Const import Const


# possible values of the square
class Field(Enum):
    white = 1
    white_king = 2
    black = 3
    black_king = 4
    empty = 0
    out_of_play = -1


class Board:

    def __init__(self):
        self.__white_turn = True  # move indicator
        self.__draw = 0  # draw indicator
        self.__board = [[Field.empty for _ in range(8)] for _ in range(8)]  # 8x8 board
        for row in range(Const.ROW):
            for col in range(Const.COL):
                if (row+col)%2:
                    if row <= 2:
                        self.__board[col][row] = Field.black
                    elif row >= 5: 
                        self.__board[col][row] = Field.white
                else:
                    self.__board[col][row] == Field.out_of_play


    def set_square(self, col, row, ch):
        self.__board[col][row] = ch

    # change move indicator
    def change_move(self):
        self.__white_turn = not self.__white_turn

    # increase draw counter (if no capture were made)
    def increase_draw_counter(self):
        self.__draw += 1

    # reset draw counter (if capture was made)
    def reset_draw_counter(self):
        self.__draw = 0

    # getters
    def get_board(self):
        return self.__board

    def get_square(self, col, row):
        if col not in range(0,8) or row not in range(0,8):
            return Field.out_of_play
        return self.__board[col][row]

    def get_draw(self):
        return self.__draw

    def get_turn(self):
        return self.__white_turn

    def is_enemy(self, col, row):
        if self.__white_turn:
            return self.get_square(col, row) in [Field.black, Field.black_king]
        else:
            return self.get_square(col, row) in [Field.white, Field.white_king]

    def is_friend(self, col, row):
        if self.__white_turn:
            return self.get_square(col, row) in [Field.white, Field.white_king]
        else:
            return self.get_square(col, row) in [Field.black, Field.black_king]

    # returns direction as a number, useful for adding to initial position of the piece when it moves
    def direction(self):
        return -1 if self.__white_turn else 1

    # no paramters: checks for captures in general, paramters: checks if particular piece can capture
    def can_capture(self, col=None, row=None):
        if col is not None and row is not None:  # row and col passed, checks capture for particular square
            if not self.is_friend(col, row):
                return [False, "You can't capture with this piece."]

            possible_captures = []
            square = self.get_square(col, row)
            if square in [Field.white, Field.black]:
                for i in [-1, 1]:
                    if self.legal_capture(col, row, col + 2*i , row + 2*self.direction()):
                        possible_captures.append([col + 2*i, row + 2*self.direction()])

            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_capture(col, row, col + 2*i, row + 2*j):
                            possible_captures.append([col + 2*i, row + 2*j])

            if possible_captures:
                return [True, possible_captures]
            return [False, "You can't capture with this piece."]
        else:  # no arguments passed, checks for possibility of capture in general
            for row in range(Const.ROW):
                for col in range(Const.COL):
                    if self.can_capture(col,row)[0]:
                        return True
            return False

    # no paramters: checks for moves in general, paramters: checks if particular piece can move
    def can_move(self, col=None, row=None):
        if col is not None and row is not None:  # row and col passed, checks move for particular square
            if not self.is_friend(col, row):
                return [False, "You can't move this piece."]
            possible_moves = []

            square = self.get_square(col, row)
            if square in [Field.white, Field.black]:

                for i in [-1, 1]:
                    if self.legal_move(col, row, col + i, row + self.direction()):
                        possible_moves.append([col + i, row + self.direction()])

            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_move(col, row, col + i, row + j):
                            possible_moves.append([col + i, row + j])
            if possible_moves:
                return [True, possible_moves]
            return [False, "You can't move this piece."]
        else:  # no arguments passed, checks for possibility of move in general
            for row in range(Const.ROW):
                for col in range(Const.COL):
                    if self.can_move(col, row)[0]:
                        return True
            return False

    def legal_move(self, start_col, start_row, end_col, end_row):
        if self.can_capture():
            return False
        if abs(end_col - start_col) != 1:
            return False
        if self.can_capture(start_col, start_row)[0]:
            return False

        start_square = self.get_square(start_col, start_row)
        end_square = self.get_square(end_col, end_row)
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row - start_row == self.direction()
        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row - start_row) == 1
        return False

    def legal_capture(self, start_col, start_row, end_col, end_row):
        if [abs(end_col - start_col), abs(end_row - start_row)] != [2, 2]:
            return False

        start_square = self.get_square(start_col, start_row)
        end_square = self.get_square(end_col, end_row)
        row_between = (start_row + end_row)//2
        col_between = (start_col + end_col)//2
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row - start_row == 2*self.direction() and self.is_enemy(
                col_between, row_between)

        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row - start_row) == 2 and self.is_enemy(col_between,
                                                                                                 row_between)

    # no paramters: count captures in general, paramters: count captures of particular piece
    def count_captures(self, col=None, row=None):
        counter = 0
        all_captures = []

        if col is not None and row is not None:  # row and col passed, counts captures for specific square
            square = self.get_square(col, row)

            if square in [Field.white, Field.black]:
                for i in [-1, 1]:
                    if self.legal_capture(col, row, col + 2*i, row + 2*self.direction()):
                        counter += 1
                        all_captures.append([col, row, col + 2*i, row + 2*self.direction()])

            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_capture(col, row, col + 2*j, row + 2*i):
                            counter += 1
                            # all_captures.append(f"{row}{col}->{row+2*i}{col+2*j}")
                            all_captures.append([col, row, col + 2*j, row + 2*i])
            return counter, all_captures
        else:  # no parameters passed, counts all possible captures
            if self.__white_turn:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(col, row) in [Field.white, Field.white_king]:
                            to_counter, to_all_captures = self.count_captures(col, row)
                            counter += to_counter
                            all_captures += to_all_captures
            else:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(col, row) in [Field.black, Field.black_king]:
                            to_counter, to_all_captures = self.count_captures(col, row)
                            counter += to_counter
                            all_captures += to_all_captures
            return counter, all_captures

    # no paramters: count moves in general, paramters: count moves of particular piece
    def count_moves(self, col=None, row=None):
        counter = 0
        all_moves = []
        if col is not None and row is not None:  # row and col passed, counts moves for specific square
            square = self.get_square(col, row)
            if square in [Field.white, Field.black]:
                for i in [-1, 1]:
                    if self.legal_move(col, row, col + i, row + self.direction()):
                        counter += 1
                        all_moves.append([col, row, col + i, row + self.direction()])
            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_move(col, row, col + i, row + j):
                            counter += 1
                            # all_moves.append(f"{row}{col}->{row+i}{col+j}")
                            all_moves.append([col, row, col + i, row + j])
            return counter, all_moves
        else:  # no parameters passed, counts all possible moves
            if self.can_capture():
                return counter, all_moves
            if self.__white_turn:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(col, row) in [Field.white, Field.white_king]:
                            to_counter, to_all_moves = self.count_moves(col, row)
                            counter += to_counter
                            all_moves += to_all_moves

            else:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(col, row) in [Field.black, Field.black_king]:
                            to_counter, to_all_moves = self.count_moves(col, row)
                            counter += to_counter
                            all_moves += to_all_moves
            return counter, all_moves

    # at the end of the turn checks if any of the piece is at the first row of the opposite color (if yes, promote it)
    def promotion(self):
        for col in self.__board:
            col[0] = Field.white_king if col[0] == Field.white else col[0]
            col[7] = Field.black_king if col[7] == Field.black else col[7]

    def move(self, start_col, start_row, end_col, end_row):
        start_square = self.get_square(start_col, start_row)

        if self.get_square(start_col, start_row) in [Field.white, Field.black, Field.white_king, Field.black_king]:
            if self.legal_capture(start_col, start_row, end_col, end_row):
                self.reset_draw_counter()
                self.set_square(start_col, start_row, Field.empty)
                self.set_square((start_col + end_col)//2, (start_row + end_row)//2, Field.empty)
                self.set_square(end_col, end_row, start_square)

                if not self.can_capture(end_col, end_row)[0]:
                    self.change_move()
            elif self.legal_move(start_col, start_row, end_col, end_row):
                if start_square in [Field.white_king, Field.black_king]:
                    self.increase_draw_counter()
                self.set_square(start_col, start_row, Field.empty)
                self.set_square(end_col, end_row, start_square)
                self.change_move()
            else:
                return False
        else:
            return False
        self.promotion()
        return True

    def is_draw(self):
        return self.__draw > Const.DRAW

    def is_end(self):
        if self.is_draw():
            return True
        if self.can_move() or self.can_capture():
            return False
        return True
