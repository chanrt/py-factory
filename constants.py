import pygame as pg


class Constants:
    def __init__(self):
        self.num_cells = 100
        self.cell_length = 25

        self.player_x = 0
        self.player_y = 0
        self.player_speed = 1

        self.bg_color = pg.Color("#013220")
        self.grid_color = pg.Color("#ffffff")

    def set_screen(self, screen):
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()


consts = Constants()