from enum import Enum

# constants
ROW = 8
COL = 8
DRAW = 39

class Field(Enum):
    white = 1
    white_king = 2
    black = 3
    black_king = 4
    empty = 0
    out_of_play = -1



class Board:
    __board = [[Field.empty for _ in range(8)] for _ in range(8)] # [row][col]
    __white_turn = True # move indicator
    __draw = 0 # draw indicator
    def __init__(self):

        self.__board[0][1::2] = [Field.black]*4
        self.__board[1][0::2] = [Field.black]*4
        self.__board[2][1::2] = [Field.black]*4
        self.__board[5][0::2] = [Field.white]*4
        self.__board[6][1::2] = [Field.white]*4
        self.__board[7][0::2] = [Field.white]*4


    def print_board(self):
        print(f"\nMove: {'white' if self.__white_turn else 'black'}")
        print(f"Legal moves: {self.count_all_moves()}")
        print(f"Legal captures: {self.count_all_captures()}")
        print(f"Moves until draw: {self.__draw}/{DRAW+1}")
        translation = {Field.white : "w",
                       Field.white_king : "W",
                       Field.black : "b",
                       Field.black_king : "B",
                       Field.empty : "_",
                       Field.out_of_play : " "}

        for row in self.__board:
            print(f"{''.join([f'[{translation[square]}]' for square in row])}")
 
    def set_square(self,row,col,ch):
        self.__board[row][col] = ch

    
    def change_move(self):
        self.__white_turn = not self.__white_turn
    def add_to_draw(self):
        self.__draw += 1
    # getters
    def get_board(self):
        return self.__board

    def get_square(self, row, col):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return Field.out_of_play
        if not (row+col)%2:
            return Field.empty
        return self.__board[row][col]

    def get_draw(self):
        return self.__draw

    def get_white_move(self):
        return self.__white_turn 

    def is_enemy(self, row, col):
        if self.__white_turn:
            return self.get_square(row,col) in [Field.black, Field.black_king]
        else:
            return self.get_square(row,col) in [Field.white, Field.white_king]

    def is_friend(self, row, col):
        if self.__white_turn:
            return self.get_square(row,col) in [Field.white, Field.white_king]
        else:
            return self.get_square(row,col) in [Field.black, Field.black_king]

    def direction(self):
        return -1 if self.__white_turn else 1

    def can_capture_any(self):
        for row in range(ROW):
            for col in range(COL):
                if self.can_capture(row,col):
                    return True
        return False

    def can_capture(self, row, col):
        if not self.is_friend(row,col):
            return False
        
        square = self.get_square(row,col)
        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_capture(row, col, row+2*self.direction(), col+2*i):
                    return True

        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_capture(row, col, row+2*i, col+2*j):
                        return True
        return False


    def legal_capture(self, start_row, start_col, end_row, end_col):
        if abs(end_col-start_col) != 2:
            return False
        
        start_square = self.get_square(start_row,start_col)
        end_square = self.get_square(end_row,end_col)
        row_between = (start_row+end_row)//2
        col_between = (start_col+end_col)//2
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row-start_row == 2*self.direction() and self.is_enemy(row_between,col_between)

        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row-start_row) == 2 and self.is_enemy(row_between,col_between)

    def can_move_any(self):
        for row in range(ROW):
            for col in range(COL):
                if self.can_move(row,col):
                    return True
        return False                


    def can_move(self,row,col):
        if not self.is_friend(row,col):
            return False
        
        square = self.get_square(row,col)
        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_move(row,col,row+self.direction(),col+i):
                    return True
        
        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_move(row,col,row+i,col+j):
                        return True
        return False

    def legal_move(self,start_row,start_col,end_row,end_col):
        if self.can_capture_any():
            return False
        if abs(end_col-start_col) != 1:
            return False
        if self.can_capture(start_row,start_col):
            return False
        
        start_square = self.get_square(start_row,start_col)
        end_square = self.get_square(end_row,end_col)
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row-start_row == self.direction()
        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row-start_row) == 1
        return False    


    # debugging
    def count_all_captures(self):
        counter = 0
        if self.__white_turn:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.white, Field.white_king]:
                        counter += self.count_captures(row,col)
        else:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.black, Field.black_king]:
                        counter += self.count_captures(row,col)
        return counter

    def count_captures(self, row, col):
        counter = 0
        square = self.get_square(row,col)

        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_capture(row,col,row+2*self.direction(),col+2*i):
                    counter += 1
                    # print(row,col,row+2*self.direction(),col+2*i,sep=".")
                    print(f"({row},{col}) -> ({row+2*self.direction()},{col+2*i})")
        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_capture(row,col,row+2*i,col+2*j):
                        counter += 1
                        print(f"({row},{col}) -> ({row+2*i},{col+2*j})")
        return counter

    def count_all_moves(self):
        counter = 0
        if self.__white_turn:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.white, Field.white_king]:
                        counter += self.count_moves(row,col)
        else:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.black, Field.black_king]:
                        counter += self.count_moves(row,col)
        return counter

    def count_moves(self,row,col):
        counter = 0
        if self.can_capture_any():
            return counter
        square = self.get_square(row,col)

        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_move(row,col,row+self.direction(),col+i):
                    counter += 1
                    print(f"({row},{col}) -> ({row+self.direction()},{col+i})")
        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_move(row,col,row+i,col+j):
                        counter +=1
                        print(f"({row},{col}) -> ({row+i},{col+j})")
        return counter

    def promotion(self):
        self.__board[0][:] = [Field.white_king if piece == Field.white else piece for piece in self.__board[0][:]]
        self.__board[7][:] = [Field.black_king if piece == Field.black else piece for piece in self.__board[7][:]]



    def move(self, start_row,start_col,end_row,end_col):
        start_square = self.get_square(start_row,start_col)

        if self.get_square(start_row,start_col) in [Field.white, Field.black, Field.white_king, Field.black_king]:
            if self.legal_capture(start_row,start_col,end_row,end_col):
                self.set_square(start_row,start_col,Field.empty)
                self.set_square((start_row+end_row)//2,(start_col+end_col)//2,Field.empty)
                self.set_square(end_row,end_col,start_square)

                if not self.can_capture(end_row,end_col):
                    self.change_move()
            elif self.legal_move(start_row,start_col,end_row,end_col):
                self.set_square(start_row,start_col,Field.empty)
                self.set_square(end_row,end_col,start_square)

                self.change_move()
                self.add_to_draw()
            else:
                return False
        else:
            return False
        self.promotion()
        return True

    def play(self):
        running = True
        
        while running:
            self.print_board()
            start_row = int(input("Starting row: "))
            start_col = int(input("Starting col: "))
            end_row = int(input("Ending row: "))
            end_col = int(input("Ending col: "))
            if not self.move(start_row,start_col,end_row,end_col):
                print("This move isn't legal.")
            if self.is_end():
                print("End of the game.")
                running = False


    def is_draw(self):
        return self.__draw > DRAW

    def is_end(self):
        if self.is_draw():
            return True
        if self.can_move_any() or self.can_capture_any():
            return False
        return True

b1 = Board()
# b1.set_square(7,0,Field.black)
# b1.set_square(0,5,Field.white)
b1.play()




# print(b1.can_move(0,0,))

