from Board import Field
from Const import Const


class TUIController:
    def __init__(self, board, debug):
        self.board = board
        self.debug = debug

    # for translation of the move notation
    def letter(self,col):
        return chr(97+col)
    def digit(self,col):
        return ord(col)-97

    def print_board(self, debug=False):
        if debug:
            moves_counter, possible_moves = self.board.count_moves()
            captures_counter, possible_captures = self.board.count_captures()
        print(f"\nMove: {'white' if self.board.get_turn() else 'black'}")
        if debug:
            print(f"Legal moves: {moves_counter}")
            if possible_moves:
                for move in possible_moves:
                    print(move)
                    for m in move:
                        start, end = m
                        start_col, start_row = start
                        end_col, end_row = end
                        print(f"{self.letter(start_col)}{8-start_row}->{self.letter(end_col)}{8-end_row}", end=" ")
                    print()
            print(f"Legal captures: {captures_counter}")
            if possible_captures:
                for capture in possible_captures:
                    print(capture)
                    for move in capture:
                        start, end = move
                        start_col, start_row = start
                        end_col, end_row = end
                        print(f"{self.letter(start_col)}{8-start_row}->{self.letter(end_col)}{8-end_row}", end=" ")
                    # print()
                print()
        print(f"Moves until draw: {self.board.get_draw()}/{Const.DRAW+1}")
        translation = {Field.white : "w",
                       Field.white_king : "W",
                       Field.black : "b",
                       Field.black_king : "B",
                       Field.empty : "_",
                       Field.out_of_play : "_"}
        
        print(f"   {''.join([f' {chr(i)} ' for i in range(ord('a'),ord('h')+1)])}")
        b = self.board.get_board()
        for row in range(Const.ROW):
            for col in range(Const.COL):
                if col == 0:
                    print(f"{Const.ROW-row}  ", end="")
                print(f"[{translation[b[col][row]]}]",end="")
                if col == Const.COL-1:
                    print(f"  {Const.ROW-row}", end="")
            print()
        print(f"   {''.join([f' {chr(i)} ' for i in range(ord('a'),ord('h')+1)])}")

    def play(self):
        running = True
        while running:
            self.print_board(self.debug)
            print(self.board.create_fen())
            print("Input moves as a combination of letter and digit, e.g. a3 or f4.")
            start = input("Start: ")
            if len(start)==2 and start[0] in "abcdefgh" and start[1] in "12345678":
                start_row = 8-int(start[1])
                start_col = self.digit((start[0]))
            else:
                input("Wrong syntax. Press ENTER to continue...")
                continue
            if self.board.can_capture():
                status, message = self.board.can_capture(start_col,start_row)
                if status:
                    print("Possible destinations: ", end="")
                    for destination in message:
                        col, row = destination
                        print(f"{self.letter(col)}{8-row}", end=" ")
                    print()
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            if self.board.can_move():
                status, message = self.board.can_move(start_col,start_row)
                if status:
                    print("Possible destinations: ", end="")
                    for destination in message:
                        col, row = destination
                        print(f"{self.letter(col)}{8-row}", end=" ")
                    print()
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            end = input("End: ")
            if len(end)==2 and end[0] in "abcdefgh" and end[1] in "12345678":      
                end_row = 8-int(end[1])
                end_col = self.digit((end[0]))
            else:
                input("Wrong syntax. Press ENTER to continue...")
                continue

            if not self.board.move(start_col,start_row,end_col,end_row):
                print(start_col,start_row,end_col,end_row)
                input("This move isn't legal. Press ENTER to continue...")
                continue
        if self.board.is_end():
            print(f"End of the game. {'Black' if self.board.get_turn() else 'White'} won!")
            running = False





"""
def play(self):
        running = True
        while running:
            self.print_board(self.debug)
            print("Input moves as a combination of letter and digit, e.g. a3 or f4.")
            start = input("Start: ")
            if len(start)==2 and start[0] in "abcdefgh" and start[1] in "12345678":
                start_row = 8-int(start[1])
                start_col = self.digit((start[0]))
            else:
                input("Wrong syntax. Press ENTER to continue...")
                continue
            if self.board.can_capture():
                status, message = self.board.can_capture(start_col,start_row)
                if status:
                    print("Possible destinations: ", end="")
                    for destination in message:
                        col, row = destination
                        print(f"{self.letter(col)}{8-row}", end=" ")
                    print()
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            if self.board.can_move():
                status, message = self.board.can_move(start_col,start_row)
                if status:
                    print("Possible destinations: ", end="")
                    for destination in message:
                        col, row = destination
                        print(f"{self.letter(col)}{8-row}", end=" ")
                    print()
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            end = input("End: ")
            if len(end)==2 and end[0] in "abcdefgh" and end[1] in "12345678":      
                end_row = 8-int(end[1])
                end_col = self.digit((end[0]))
            else:
                input("Wrong syntax. Press ENTER to continue...")
                continue

            if not self.board.move(start_col,start_row,end_col,end_row):
                print(start_col,start_row,end_col,end_row)
                input("This move isn't legal. Press ENTER to continue...")
                continue
            if self.board.is_end():
                print(f"End of the game. {'Black' if self.board.get_turn() else 'White'} won!")
                running = False



"""


