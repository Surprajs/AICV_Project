import pygame
import sys
from Const import Const
from Board import Field


class GUIController:

    def __init__(self, board):
        self.board = board
        self.marked = [None, None]

    def print_board(self, win):
        rect = Const.background.get_rect()
        win.blit(Const.background, rect)
        pygame.display.update()

    def print_piece(self, win):
        b = self.board.get_board()
        for row in range(Const.ROW):
            for col in range(Const.COL):
                if b[col][row] == Field.black:
                    win.blit(Const.pawnBlack, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.white:
                    win.blit(Const.pawnWhite, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.black_king:
                    win.blit(Const.kingBlack, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.white_king:
                    win.blit(Const.kingWhite, (col * 80 + 40, row * 80 + 40))
        pygame.display.flip()

    def check_position(self, pos, win):
        _, possible_moves = self.board.count_moves()
        _, possible_captures = self.board.count_captures()
        x = (pos[0] - 40) // 80
        y = ((pos[1] - 40) // 80)
        if self.marked:
            if possible_moves:
                for move in possible_moves:
                    start_col, start_row, end_col, end_row = move
                    if start_col == self.marked[0] and start_row == self.marked[1]:
                        if end_col == x and end_row == y:
                            self.board.move(start_col, start_row, end_col, end_row)

            if possible_captures:
                for capture in possible_captures:
                    start_col, start_row, end_col, end_row = capture
                    if start_col == self.marked[0] and start_row == self.marked[1]:
                        if end_col == x and end_row == y:
                            self.board.move(start_col, start_row, end_col, end_row)
            self.print_board(win)
            self.print_piece(win)
            self.marked = [None, None]

        if possible_moves:
            for move in possible_moves:
                start_col, start_row, end_col, end_row = move
                if start_col == x and start_row == y:
                    win.blit(Const.source, (start_col * 80 + 40, start_row * 80 + 40))
                    win.blit(Const.destination, (end_col * 80 + 40, end_row * 80 + 40))
                    pygame.display.flip()
                    self.marked = [start_col, start_row]
        if possible_captures:
            for capture in possible_captures:
                start_col, start_row, end_col, end_row = capture
                if start_col == x and start_row == y:
                    win.blit(Const.source, (start_col * 80 + 40, start_row * 80 + 40))
                    win.blit(Const.destination, (end_col * 80 + 40, end_row * 80 + 40))
                    pygame.display.flip()
                    self.marked = [start_col, start_row]

    def play(self):
        WIN = pygame.display.set_mode((Const.WIDTH, Const.HEIGHT))
        pygame.display.set_caption('Checkers')
        self.print_board(WIN)
        self.print_piece(WIN)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.check_position(pos, WIN)
            if self.board.is_end():
                running = False
                pygame.quit()
                sys.exit()
