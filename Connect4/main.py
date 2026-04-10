import pygame
from Connect4.UI.ui_pygame import GameUI


pygame.init()

def main():
    game = GameUI()
    game.run()

if __name__ == "__main__":
    main()
