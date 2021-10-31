class Board:
    __board = [["-" for _ in range(8)] for _ in range(8)]
    def __init__(self):
        self.board = [["-" for _ in range(8)] for _ in range(8)]
        # self.__board[0][0::2] = ["B"]*4
        # self.__board[1][1::2] = ["B"]*4
        # self.__board[2][0::2] = ["B"]*4
        # self.__board[5][0::2] = ["W"]*4
        # self.__board[6][1::2] = ["W"]*4
        # self.__board[7][0::2] = ["W"]*4


    def print_board(self):
        for row in self.__board:
            print(f"{' '.join(row)}")
        
    def get_board(self):
        return self.__board
b1 = Board()

# print(b1._a)
print(b1.print_board())
print(b1.board)
