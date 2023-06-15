import pygame as pg

from constants import consts as c
from id_mapping import id_map
from images import img as i
from ui.game_ui import ui


class Splitter:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()
        self.init_targets()

        self.state = 1
        self.item = None

        self.target1_open = False
        self.target2_open = False

    def update(self, sm, im):
        if Splitter.can_be_directed_to(sm, im, self.target1_row, self.target1_col):
            self.target1_open = True
        else:
            self.target1_open = False

        if Splitter.can_be_directed_to(sm, im, self.target2_row, self.target2_col):
            self.target2_open = True
        else:
            self.target2_open = False

        if im.grid[self.row][self.col] != 0:
            self.item = im.grid[self.row][self.col].item

            if self.state == 1:
                if self.target1_open:
                    self.direct_to_one(im)
                    self.state = 2
                    self.target1_open = False
                elif self.target2_open:
                    self.direct_to_two(im)
                    self.state = 1
                    self.target2_open = False

            elif self.state == 2:
                if self.target2_open:
                    self.direct_to_two(im)
                    self.state = 1
                    self.target2_open = False
                elif self.target1_open:
                    self.direct_to_one(im)
                    self.state = 2
                    self.target1_open = False

    @staticmethod
    def can_be_directed_to(sm, im, row, col):
        return im.grid[row][col] == 0 and sm.item_can_be_placed(row, col)

    def direct_to_one(self, im):
        im.remove(self.row, self.col)
        im.add(self.target1_row, self.target1_col, self.item)

    def direct_to_two(self, im):
        im.remove(self.row, self.col)
        im.add(self.target2_row, self.target2_col, self.item)

    def can_accept_item(self, a, b):
        return self.target1_open or self.target2_open

    def render(self):
        c.screen.blit(i.images[id_map["splitter"]][self.direction], (self.x - c.player_x, self.y - c.player_y))

    def rotate(self, rotation):
        self.direction = (self.direction + rotation) % 4
        self.init_targets()

    def render_tooltip(self):
        pg.draw.rect(c.screen, c.source_color, (self.col * c.cell_length - c.player_x, self.row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)
        pg.draw.rect(c.screen, c.target_color, (self.target1_col * c.cell_length - c.player_x, self.target1_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)
        pg.draw.rect(c.screen, c.target_color, (self.target2_col * c.cell_length - c.player_x, self.target2_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)

        if not self.target1_open and not self.target2_open:
            status = "FULL"
        else:
            status = "WORKING"
        
        ui.render_text(f"Splitter [{status}]: (L/R) to rotate")

    def calc_position(self):
        self.x = self.col * c.cell_length
        self.y = self.row * c.cell_length

    def init_targets(self):
        if self.direction == 0:
            self.target1_row = self.target2_row = self.row - 1
            self.target1_col = self.col - 1
            self.target2_col = self.col + 1
        elif self.direction == 1:
            self.target1_col = self.target2_col = self.col + 1
            self.target1_row = self.row - 1
            self.target2_row = self.row + 1
        elif self.direction == 2:
            self.target1_row = self.target2_row = self.row + 1
            self.target1_col = self.col + 1
            self.target2_col = self.col - 1
        elif self.direction == 3:
            self.target1_col = self.target2_col = self.col - 1
            self.target1_row = self.row + 1
            self.target2_row = self.row - 1