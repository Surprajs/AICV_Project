import pygame
import numpy as np
import sys
import cv2
from enum import Enum

from Const import Const
from ConstGraphic import ConstGraphic
from Board import Field


class State(Enum):
    start = 0
    game = 1
    results = 2
    end = -1


class GUIController:

    def __init__(self, board):
        self.board = board
        self.ai = None
        self.board_recognizer = None
        self.marked = [None, None]
        self.state = State.start
        self.WIN = None
        self.camera = None
        self.opponent = False
        self.depth = 3
        self.camera_WN = False
        self.white_ai = False
        self.frame_copy = None
        self.new_camera_matrix = None
        self.mtx = None
        self.dist = None

    def print_board(self):
        rect = ConstGraphic.background.get_rect()
        self.WIN.blit(ConstGraphic.background, rect)
        pygame.display.update()

    def print_piece(self):
        b = self.board.get_board()
        for row in range(Const.ROW):
            for col in range(Const.COL):
                if b[col][row] == Field.black:
                    self.WIN.blit(ConstGraphic.pawnBlack, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.white:
                    self.WIN.blit(ConstGraphic.pawnWhite, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.black_king:
                    self.WIN.blit(ConstGraphic.kingBlack, (col * 80 + 40, row * 80 + 40))
                elif b[col][row] == Field.white_king:
                    self.WIN.blit(ConstGraphic.kingWhite, (col * 80 + 40, row * 80 + 40))
        pygame.display.flip()

    def check_position(self, pos):
        _, possible_moves = self.board.count_moves()
        _, possible_captures = self.board.count_captures()
        possible_moves.extend(possible_captures)
        x = (pos[0] - 40) // 80
        y = ((pos[1] - 40) // 80)
        if self.marked:
            if possible_moves:
                for move in possible_moves:
                    start, end = move[0]
                    start_col, start_row = start
                    end_col, end_row = end
                    if start_col == self.marked[0] and start_row == self.marked[1]:
                        if end_col == x and end_row == y:
                            self.board.move(start_col, start_row, end_col, end_row)

            # if possible_captures:
            #     for capture in possible_captures:
            #         start, end = capture[0]
            #         start_col, start_row = start
            #         end_col, end_row = end
            #         if start_col == self.marked[0] and start_row == self.marked[1]:
            #             if end_col == x and end_row == y:
            #                 self.board.move(start_col, start_row, end_col, end_row)
            self.print_board()
            self.print_piece()
            self.marked = [None, None]

        if pos[1] in range(600, 700+1) and pos[0] in range(740, 1420+1):
            self.evaluate()

        if possible_moves:
            for move in possible_moves:
                start, end = move[0]
                start_col, start_row = start
                end_col, end_row = end
                if start_col == x and start_row == y:
                    self.WIN.blit(ConstGraphic.source, (start_col * 80 + 40, start_row * 80 + 40))
                    self.WIN.blit(ConstGraphic.destination, (end_col * 80 + 40, end_row * 80 + 40))
                    pygame.display.flip()
                    self.marked = [start_col, start_row]
        # if possible_captures:
        #     for capture in possible_captures:
        #         start, end = capture[0]
        #         start_col, start_row = start
        #         end_col, end_row = end
        #         if start_col == x and start_row == y:
        #             self.WIN.blit(ConstGraphic.source, (start_col * 80 + 40, start_row * 80 + 40))
        #             self.WIN.blit(ConstGraphic.destination, (end_col * 80 + 40, end_row * 80 + 40))
        #             pygame.display.flip()
        #             self.marked = [start_col, start_row]

    def get_frame(self):
        _, frame = self.camera.read()
        frame = cv2.undistort(frame, self.mtx, self.dist, None, self.new_camera_matrix)
        self.frame_copy = np.copy(frame)
        cv2.rectangle(frame, (280, 0), (1000, 719), (0, 0, 255), thickness=3)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.resize(frame, (405, 720))
        surf = pygame.surfarray.make_surface(frame)
        self.WIN.blit(ConstGraphic.menu_bg, (720, 0))
        self.WIN.blit(ConstGraphic.turnWhite, (955, 415)) if self.board.get_turn() else self.WIN.blit(ConstGraphic.turnBlack, (958, 415))
        self.WIN.blit(ConstGraphic.evaluate, (720, 580))
        self.WIN.blit(surf, (720, 0))
        pygame.display.flip()

    def evaluate(self):
        board = self.frame_copy[:, 280:1000]
        board = cv2.flip(board,1)
        points = self.board_recognizer.get_points(board)
        squares = self.board_recognizer.crop_squares(board, points)
        if squares:
            fen = self.board_recognizer.create_fen(squares)
            self.board.load_from_fen(fen)
            self.board.change_move()
            self.print_board()
            self.print_piece()
        else:
            print("board could not be recognized")


    def menu_position(self, pos):
        if pos[1] in range(45, 225 + 1):
            if pos[0] in range(45, 338 + 1):
                self.WIN.blit(ConstGraphic.p_ai_click, (45, 45))
                self.WIN.blit(ConstGraphic.p_human, (382, 45))
                self.WIN.blit(ConstGraphic.depth_3_click, (45, 270))
                self.WIN.blit(ConstGraphic.depth_5, (270, 270))
                self.WIN.blit(ConstGraphic.depth_8, (495, 270))
                self.WIN.blit(ConstGraphic.p_aswhite, (45, 585))
                self.WIN.blit(ConstGraphic.p_asblack, (382, 585))
                self.opponent = True
            if pos[0] in range(382, 675 + 1):
                self.WIN.blit(ConstGraphic.menu_bg, (0, 0))
                self.WIN.blit(ConstGraphic.p_ai, (45, 45))
                self.WIN.blit(ConstGraphic.p_human_click, (382, 45))
                if self.camera_WN:
                    self.WIN.blit(ConstGraphic.w_camera_click, (45, 405))
                    self.WIN.blit(ConstGraphic.no_camera, (382, 405))
                else:
                    self.WIN.blit(ConstGraphic.w_camera, (45, 405))
                    self.WIN.blit(ConstGraphic.no_camera_click, (382, 405))
                self.WIN.blit(ConstGraphic.start, (495, 585))
                self.opponent = False

        if self.opponent:
            if pos[1] in range(270, 360 + 1):
                if pos[0] in range(45, 225 + 1):
                    self.WIN.blit(ConstGraphic.depth_3_click, (45, 270))
                    self.WIN.blit(ConstGraphic.depth_5, (270, 270))
                    self.WIN.blit(ConstGraphic.depth_8, (495, 270))
                    self.depth = 3
                if pos[0] in range(270, 450 + 1):
                    self.WIN.blit(ConstGraphic.depth_3, (45, 270))
                    self.WIN.blit(ConstGraphic.depth_5_click, (270, 270))
                    self.WIN.blit(ConstGraphic.depth_8, (495, 270))
                    self.depth = 5
                if pos[0] in range(495, 675 + 1):
                    self.WIN.blit(ConstGraphic.depth_3, (45, 270))
                    self.WIN.blit(ConstGraphic.depth_5, (270, 270))
                    self.WIN.blit(ConstGraphic.depth_8_click, (495, 270))
                    self.depth = 8

        if pos[1] in range(405, 495 + 1):
            if pos[0] in range(45, 338 + 1):
                self.WIN.blit(ConstGraphic.w_camera_click, (45, 405))
                self.WIN.blit(ConstGraphic.no_camera, (382, 405))
                self.camera_WN = True
            if pos[0] in range(382, 675 + 1):
                self.WIN.blit(ConstGraphic.w_camera, (45, 405))
                self.WIN.blit(ConstGraphic.no_camera_click, (382, 405))
                self.camera_WN = False

        pygame.display.flip()

    def show_default_start(self):
        self.WIN = pygame.display.set_mode((Const.WIDTH, Const.HEIGHT))
        rect = ConstGraphic.background.get_rect()
        self.WIN.blit(ConstGraphic.menu_bg, rect)
        self.WIN.blit(ConstGraphic.p_ai, (45, 45))
        self.WIN.blit(ConstGraphic.p_human_click, (382, 45))
        self.WIN.blit(ConstGraphic.w_camera, (45, 405))
        self.WIN.blit(ConstGraphic.no_camera_click, (382, 405))
        self.WIN.blit(ConstGraphic.start, (495, 585))
        pygame.display.set_caption('Start')
        pygame.display.flip()

    def start(self):
        self.show_default_start()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if not self.opponent:
                        if pos[0] in range(495, 675 + 1) and pos[1] in range(585, 675 + 2):
                            running = False
                        else:
                            self.menu_position(pos)
                    else:
                        if pos[1] in range(585, 675 + 1):
                            if pos[0] in range(45, 338 + 1):
                                running = False
                                self.white_ai = False
                            if pos[0] in range(382, 675 + 1):
                                running = False
                                self.white_ai = True
                        else:
                            self.menu_position(pos)
        self.WIN = pygame.display.quit()
        if self.opponent:
            from AI import AI
            self.ai = AI(self.board, white_ai=self.white_ai, depth=self.depth)
        self.state = State.game

    def game(self):
        if self.camera_WN:
            from BoardRecognition import BoardRecognition
            self.WIN = pygame.display.set_mode((Const.WIDTH_CAM, Const.HEIGHT))
            self.WIN.blit(ConstGraphic.menu_bg, (720, 0))
            self.camera = cv2.VideoCapture(2)
            width, height = 1280, 720
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            with np.load("calibration/camera_parameters.npz") as file:
                self.mtx, self.dist = file["mtx"], file["dist"]
            self.new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(self.mtx,self.dist, (width,height), 0, (width,height))
            self.board_recognizer = BoardRecognition()
        else:
            self.WIN = pygame.display.set_mode((Const.WIDTH, Const.HEIGHT))
        pygame.display.set_caption('Checkers')
        self.print_board()
        self.print_piece()
        running = True
        while running:
            if self.camera_WN:
                self.get_frame()
            if self.opponent:
                if self.ai.get_ai_color() == self.board.get_turn():
                    self.ai.play()
                    self.print_board()
                    self.print_piece()
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            if self.camera_WN:
                                self.camera.release()
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            self.check_position(pos)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if self.camera_WN:
                            self.camera.release()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        self.check_position(pos)
            if self.board.is_end():
                running = False
                if self.camera_WN:
                    self.camera.release()
                self.state = State.results
                self.WIN = pygame.display.quit()

    def results(self):
        self.WIN = pygame.display.set_mode((Const.WIDTH_CAM, Const.HEIGHT))
        self.print_board()
        self.print_piece()
        self.WIN.blit(ConstGraphic.menu_bg, (720, 0))
        self.WIN.blit(ConstGraphic.exit, (765, 585))
        self.WIN.blit(ConstGraphic.p_again, (1102, 585))
        if self.board.is_draw():
            self.WIN.blit(ConstGraphic.r_draw, (765, 45))
        elif self.board.get_turn():
            self.WIN.blit(ConstGraphic.r_black, (765, 45))
        else:
            self.WIN.blit(ConstGraphic.r_white, (765, 45))

        pygame.display.set_caption('Results')
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(765, 1058 + 1) and pos[1] in range(585, 675 + 2):
                        running = False
                        self.state = State.end
                    elif pos[0] in range(1102, 1395 + 1) and pos[1] in range(585, 675 + 2):
                        running = False
                        self.state = State.start
                        self.depth = 3
                        self.camera_WN = False
                        self.opponent = False
        self.WIN = pygame.display.quit()

    def play(self):
        while self.state != State.end:
            {
                State.start: self.start(),
                State.game: self.game(),
                State.results: self.results(),
                State.end: None,
            }[self.state]
        pygame.quit()
        sys.exit()
