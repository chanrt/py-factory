import pygame as pg

from constants import consts as c
from id_mapping import id_map
from images import img as i


class Conveyor:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()

    def update(self, sm, im):
        pass

    def render(self):
        c.screen.blit(i.images[id_map["conveyor"]][self.direction], (self.x - c.player_x, self.y - c.player_y))

    def render_tooltip(self):
        pass

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 4

    def calc_position(self):
        self.x = self.col * c.cell_length
        self.y = self.row * c.cell_length


class ConveyorUnderground:
    def __init__(self, row, col, direction):
        self.source_row = row
        self.source_col = col
        self.direction = direction
        self.length = c.ug_state
        self.init_target()
        self.calc_position()

    def update(self, sm, im):
        pass

    def render(self):
        c.screen.blit(i.images[id_map["conveyor_underground"]][self.direction], (self.source_x - c.player_x, self.source_y - c.player_y))
        c.screen.blit(i.images[id_map["conveyor_underground"]][self.direction + 4], (self.target_x - c.player_x, self.target_y - c.player_y))

    def render_tooltip(self):
        pg.draw.line(
            c.screen, c.action_color, 
            (self.source_x - c.player_x + c.cell_length // 2, self.source_y - c.player_y + c.cell_length // 2), 
            (self.target_x - c.player_x + c.cell_length // 2, self.target_y - c.player_y + c.cell_length // 2), 
            3
        )

    def init_target(self):
        self.target_row = self.source_row
        self.target_col = self.source_col

        if self.direction == 0:
            self.target_row -= self.length
        elif self.direction == 1:
            self.target_col += self.length
        elif self.direction == 2:
            self.target_row += self.length
        elif self.direction == 3:
            self.target_col -= self.length

    def calc_position(self):
        self.source_x = self.source_col * c.cell_length
        self.source_y = self.source_row * c.cell_length
        self.target_x = self.target_col * c.cell_length
        self.target_y = self.target_row * c.cell_length