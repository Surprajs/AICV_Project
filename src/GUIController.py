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
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] == Field.black:
                    win.blit(Const.pawnBlack, (j * 80 + 40, i * 80 + 40))
                elif b[i][j] == Field.white:
                    win.blit(Const.pawnWhite, (j * 80 + 40, i * 80 + 40))
                elif b[i][j] == Field.black_king:
                    win.blit(Const.kingBlack, (j * 80 + 40, i * 80 + 40))
                elif b[i][j] == Field.white_king:
                    win.blit(Const.kingWhite, (j * 80 + 40, i * 80 + 40))
        pygame.display.flip()

    def check_position(self, pos, win):
        moves_counter, possible_moves = self.board.count_moves()
        captures_counter, possible_captures = self.board.count_captures()
        x = (pos[0] - 40) // 80
        y = ((pos[1] - 40) // 80)
        if self.marked:
            if possible_moves:
                for move in possible_moves:
                    start_row, start_col, end_row, end_col = move
                    if start_row == self.marked[0] and start_col == self.marked[1]:
                        if end_row == y and end_col == x:
                            self.board.move(start_row, start_col, end_row, end_col)

            if possible_captures:
                for capture in possible_captures:
                    start_row, start_col, end_row, end_col = capture
                    if start_row == self.marked[0] and start_col == self.marked[1]:
                        if end_row == y and end_col == x:
                            self.board.move(start_row, start_col, end_row, end_col)
            self.print_board(win)
            self.print_piece(win)
            self.marked = [None, None]

        if possible_moves:
            for move in possible_moves:
                start_row, start_col, end_row, end_col = move
                if start_row == y and start_col == x:
                    win.blit(Const.source, (start_col * 80 + 40, start_row * 80 + 40))
                    win.blit(Const.destination, (end_col * 80 + 40, end_row * 80 + 40))
                    pygame.display.flip()
                    self.marked = [start_row, start_col]
        if possible_captures:
            for capture in possible_captures:
                start_row, start_col, end_row, end_col = capture
                if start_row == y and start_col == x:
                    win.blit(Const.source, (start_col * 80 + 40, start_row * 80 + 40))
                    win.blit(Const.destination, (end_col * 80 + 40, end_row * 80 + 40))
                    pygame.display.flip()
                    self.marked = [start_row, start_col]

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
