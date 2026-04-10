import pygame

BLUE = (5, 126, 153)
RED = (196, 24, 78)
GRAY = (110, 110, 110)
BLACK = (30, 30, 30)
WHITE = (230, 230, 230)

ROWS = 6
COLS = 7
CELL_SIZE = 100

WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS+1) * CELL_SIZE
RADIUS = CELL_SIZE//2 - 8

def load_fonts():
    return {
        "main": pygame.font.SysFont("calibri", 28, bold=True),
        "title": pygame.font.SysFont("calibri", 36, bold=True),
        "button": pygame.font.SysFont("calibri", 28, bold=True),
        "small": pygame.font.SysFont("calibri", 20),
    }