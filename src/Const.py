import pygame

class Const:
    # Board
    ROW = 8
    COL = 8
    DRAW = 39
    WIDTH, HEIGHT = 720, 720
    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    # images
    background = pygame.image.load('./graphics/board.png')
    pawnBlack = pygame.image.load('./graphics/black.png')
    pawnWhite = pygame.image.load('./graphics/white.png')
    kingBlack = pygame.image.load('./graphics/black_king_crown.png')
    kingWhite = pygame.image.load('./graphics/white_king_crown.png')
    source = pygame.image.load('./graphics/source.png')
    destination = pygame.image.load('./graphics/destination.png')
    turnWhite = pygame.image.load('./graphics/w_turn.png')
    turnBlack = pygame.image.load('./graphics/b_turn.png')
    # AI constants
    SCORE_WIN = 10_000
    SCORE_LOST = -10_000

