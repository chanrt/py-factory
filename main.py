import pygame as pg

from constants import consts as c
from game_loop import game_loop


def main_menu():
    # this should lead to the menu screen (to be developed later)
    game_loop()
    

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    main_menu()