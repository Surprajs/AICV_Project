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
        self.__board[0][1::2] = [Field.black] * 4
        self.__board[1][0::2] = [Field.black] * 4
        self.__board[2][1::2] = [Field.black] * 4
        self.__board[5][0::2] = [Field.white] * 4
        self.__board[6][1::2] = [Field.white] * 4
        self.__board[7][0::2] = [Field.white] * 4
        self.__board = [[Field.out_of_play if not (c + r) % 2 else square for c, square in enumerate(row)] for r, row in
                        enumerate(self.__board)]

    def letter(self, col):
        return chr(97 + col)

    def digit(self, col):
        return ord(col) - 97

    def set_square(self, row, col, ch):
        self.__board[row][col] = ch

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

    def get_square(self, row, col):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return Field.out_of_play
        return self.__board[row][col]

    def get_draw(self):
        return self.__draw

    def get_turn(self):
        return self.__white_turn

    def is_enemy(self, row, col):
        if self.__white_turn:
            return self.get_square(row, col) in [Field.black, Field.black_king]
        else:
            return self.get_square(row, col) in [Field.white, Field.white_king]

    def is_friend(self, row, col):
        if self.__white_turn:
            return self.get_square(row, col) in [Field.white, Field.white_king]
        else:
            return self.get_square(row, col) in [Field.black, Field.black_king]

    # returns direction as a number, useful for adding to initial position of the piece when it moves
    def direction(self):
        return -1 if self.__white_turn else 1

    # no paramters: checks for captures in general, paramters: checks if particular piece can capture
    def can_capture(self, row=None, col=None):
        if row is not None and col is not None:  # row and col passed, checks capture for particular square
            if not self.is_friend(row, col):
                return [False, "You can't capture with this piece."]

            possible_captures = []
            square = self.get_square(row, col)
            if square in [Field.white, Field.black]:
                for i in [-1, 1]:
                    if self.legal_capture(row, col, row + 2 * self.direction(), col + 2 * i):
                        possible_captures.append([row + 2 * self.direction(), col + 2 * i])

            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_capture(row, col, row + 2 * i, col + 2 * j):
                            possible_captures.append([row + 2 * i, col + 2 * j])

            if possible_captures:
                return [True, possible_captures]
            return [False, "You can't capture with this piece."]
        else:  # no arguments passed, checks for possibility of capture in general
            for row in range(Const.ROW):
                for col in range(Const.COL):
                    if self.can_capture(row, col)[0]:
                        return True
            return False

    # no paramters: checks for moves in general, paramters: checks if particular piece can move
    def can_move(self, row=None, col=None):
        if row is not None and col is not None:  # row and col passed, checks move for particular square
            if not self.is_friend(row, col):
                return [False, "You can't move this piece."]
            possible_moves = []

            square = self.get_square(row, col)
            if square in [Field.white, Field.black]:

                for i in [-1, 1]:
                    if self.legal_move(row, col, row + self.direction(), col + i):
                        possible_moves.append([row + self.direction(), col + i])

            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_move(row, col, row + i, col + j):
                            possible_moves.append([row + i, col + j])
            if possible_moves:
                return [True, possible_moves]
            return [False, "You can't move this piece."]
        else:  # no arguments passed, checks for possibility of move in general
            for row in range(Const.ROW):
                for col in range(Const.COL):
                    if self.can_move(row, col)[0]:
                        return True
            return False

    def legal_move(self, start_row, start_col, end_row, end_col):
        if self.can_capture():
            return False
        if abs(end_col - start_col) != 1:
            return False
        if self.can_capture(start_row, start_col)[0]:
            return False

        start_square = self.get_square(start_row, start_col)
        end_square = self.get_square(end_row, end_col)
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row - start_row == self.direction()
        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row - start_row) == 1
        return False

    def legal_capture(self, start_row, start_col, end_row, end_col):
        if [abs(end_col - start_col), abs(end_row - start_row)] != [2, 2]:
            return False

        start_square = self.get_square(start_row, start_col)
        end_square = self.get_square(end_row, end_col)
        row_between = (start_row + end_row) // 2
        col_between = (start_col + end_col) // 2
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row - start_row == 2 * self.direction() and self.is_enemy(
                row_between, col_between)

        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row - start_row) == 2 and self.is_enemy(row_between,
                                                                                                 col_between)

    # no paramters: count captures in general, paramters: count captures of particular piece
    def count_captures(self, row=None, col=None):
        counter = 0
        all_captures = []

        if row is not None and col is not None:  # row and col passed, counts captures for specific square
            square = self.get_square(row, col)

            if square in [Field.white, Field.black]:
                for i in [-1, 1]:
                    if self.legal_capture(row, col, row + 2 * self.direction(), col + 2 * i):
                        counter += 1
                        # all_captures.append(f"{row}{col}->{row+2*self.direction()}{col+2*i}")
                        all_captures.append([row, col, row + 2 * self.direction(), col + 2 * i])

            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_capture(row, col, row + 2 * i, col + 2 * j):
                            counter += 1
                            # all_captures.append(f"{row}{col}->{row+2*i}{col+2*j}")
                            all_captures.append([row, col, row + 2 * i, col + 2 * j])
            return counter, all_captures
        else:  # no parameters passed, counts all possible captures
            if self.__white_turn:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(row, col) in [Field.white, Field.white_king]:
                            to_counter, to_all_captures = self.count_captures(row, col)
                            counter += to_counter
                            all_captures += to_all_captures
            else:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(row, col) in [Field.black, Field.black_king]:
                            to_counter, to_all_captures = self.count_captures(row, col)
                            counter += to_counter
                            all_captures += to_all_captures
            return counter, all_captures

    # no paramters: count moves in general, paramters: count moves of particular piece
    def count_moves(self, row=None, col=None):
        counter = 0
        all_moves = []
        if row is not None and col is not None:  # row and col passed, counts moves for specific square
            square = self.get_square(row, col)
            if square in [Field.white, Field.black]:
                for i in [-1, 1]:
                    if self.legal_move(row, col, row + self.direction(), col + i):
                        counter += 1
                        # all_moves.append(f"{row}{col}->{row+self.direction()}{col+i}")
                        all_moves.append([row, col, row + self.direction(), col + i])
            if square in [Field.white_king, Field.black_king]:
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.legal_move(row, col, row + i, col + j):
                            counter += 1
                            # all_moves.append(f"{row}{col}->{row+i}{col+j}")
                            all_moves.append([row, col, row + i, col + j])
            return counter, all_moves
        else:  # no parameters passed, counts all possible moves
            if self.can_capture():
                return counter, all_moves
            if self.__white_turn:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(row, col) in [Field.white, Field.white_king]:
                            to_counter, to_all_moves = self.count_moves(row, col)
                            counter += to_counter
                            all_moves += to_all_moves

            else:
                for row in range(Const.ROW):
                    for col in range(Const.COL):
                        if self.get_square(row, col) in [Field.black, Field.black_king]:
                            to_counter, to_all_moves = self.count_moves(row, col)
                            counter += to_counter
                            all_moves += to_all_moves
            return counter, all_moves

    # at the end of the turn checks if any of the piece is at the first row of the opposite color (if yes, promote it)
    def promotion(self):
        self.__board[0][:] = [Field.white_king if piece == Field.white else piece for piece in self.__board[0][:]]
        self.__board[7][:] = [Field.black_king if piece == Field.black else piece for piece in self.__board[7][:]]

    def move(self, start_row, start_col, end_row, end_col):
        start_square = self.get_square(start_row, start_col)

        if self.get_square(start_row, start_col) in [Field.white, Field.black, Field.white_king, Field.black_king]:
            if self.legal_capture(start_row, start_col, end_row, end_col):
                self.reset_draw_counter()
                self.set_square(start_row, start_col, Field.empty)
                self.set_square((start_row + end_row) // 2, (start_col + end_col) // 2, Field.empty)
                self.set_square(end_row, end_col, start_square)

                if not self.can_capture(end_row, end_col)[0]:
                    self.change_move()
            elif self.legal_move(start_row, start_col, end_row, end_col):
                if start_square in [Field.white_king, Field.black_king]:
                    self.increase_draw_counter()
                self.set_square(start_row, start_col, Field.empty)
                self.set_square(end_row, end_col, start_square)
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
