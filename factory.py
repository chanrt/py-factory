import pygame as pg

from constants import consts as c
from id_mapping import id_map
from images import img as i


class Factory:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()
        self.init_target()
        
    def update(self, sm, im):
        pass

    def render(self):
        c.screen.blit(i.images[id_map["factory"]], (self.x - c.player_x, self.y - c.player_y))

    def render_tooltip(self):
        pg.draw.circle(c.screen, c.target_color, (self.target_col * c.cell_length - c.player_x + c.cell_length // 2, self.target_row * c.cell_length - c.player_y + c.cell_length // 2), 5)

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 4
        self.init_target()

    def init_target(self):
        if self.direction == 0:
            self.target_row = self.row - 1
            self.target_col = self.col
        elif self.direction == 1:
            self.target_row = self.row
            self.target_col = self.col + 1
        elif self.direction == 2:
            self.target_row = self.row + 1
            self.target_col = self.col
        elif self.direction == 3:
            self.target_row = self.row
            self.target_col = self.col - 1

    def calc_position(self):
        self.x = self.col * c.cell_length
        self.y = self.row * c.cell_length