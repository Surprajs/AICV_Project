import pygame
import sys
import cv2
from Const import Const
from Board import Field


class GUIController:

    def __init__(self, board):
        self.board = board
        self.marked = [None, None]
        self.WIN = pygame.display.set_mode((Const.WIDTH, Const.HEIGHT))
        self.camera = cv2.VideoCapture(0)

    def print_board(self):
        rect = Const.background.get_rect()
        self.WIN.blit(Const.background, rect)
        pygame.display.update()

    def print_piece(self):
        b = self.board.get_board()
        for row in range(Const.ROW):
            for col in range(Const.COL):
                if b[col][row] == Field.black:
                    self.WIN.blit(Const.pawnBlack, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.white:
                    self.WIN.blit(Const.pawnWhite, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.black_king:
                    self.WIN.blit(Const.kingBlack, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.white_king:
                    self.WIN.blit(Const.kingWhite, (col * 80 + 40, row * 80 + 40))
        pygame.display.flip()

    def check_position(self, pos):
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
            self.print_board()
            self.print_piece()
            self.marked = [None, None]

        if possible_moves:
            for move in possible_moves:
                start_col, start_row, end_col, end_row = move
                if start_col == x and start_row == y:
                    self.WIN.blit(Const.source, (start_col * 80 + 40, start_row * 80 + 40))
                    self.WIN.blit(Const.destination, (end_col * 80 + 40, end_row * 80 + 40))
                    pygame.display.flip()
                    self.marked = [start_col, start_row]
        if possible_captures:
            for capture in possible_captures:
                start_col, start_row, end_col, end_row = capture
                if start_col == x and start_row == y:
                    self.WIN.blit(Const.source, (start_col * 80 + 40, start_row * 80 + 40))
                    self.WIN.blit(Const.destination, (end_col * 80 + 40, end_row * 80 + 40))
                    pygame.display.flip()
                    self.marked = [start_col, start_row]

    def get_frame(self):
        _, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        surf = pygame.surfarray.make_surface(frame)
        self.WIN.blit(surf, (720, 0))
        if self.board.get_turn():
            self.WIN.blit(Const.turnWhite, (720, 480))
        else:
            self.WIN.blit(Const.turnBlack, (720, 480))
        pygame.display.flip()

    def play(self):
        pygame.display.set_caption('Checkers')
        self.print_board()
        self.print_piece()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.check_position(pos)
            if self.board.is_end():
                running = False
                pygame.quit()
                self.vid.release()
                sys.exit()
            self.get_frame()
