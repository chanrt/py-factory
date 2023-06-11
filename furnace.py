import pygame as pg

from constants import consts as c
from id_mapping import id_map
from images import img as i
from world import world as w


class Furnace:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.x = col * c.cell_length
        self.y = row * c.cell_length
        self.direction = direction
        self.init_target()

        self.smelting = None
        self.progress = 0

    def update(self, sm, im):
        if self.smelting is None:
            if im.contains_ore(self.row, self.col):
                self.smelting = im.grid[self.row][self.col]
                self.smelting.display = False
                self.progress = 0
        else: 
            if self.progress < c.smelt_time:
                self.progress += c.dt
            elif im.grid[self.target_row][self.target_col] == 0 and sm.item_can_be_placed(self.target_row, self.target_col):
                im.remove(self.row, self.col)
                if self.smelting.item == id_map["iron_ore"]:
                    smelted_item_index = id_map["iron"]
                elif self.smelting.item == id_map["copper_ore"]:
                    smelted_item_index = id_map["copper"]

                im.add(self.target_row, self.target_col, smelted_item_index)
                self.smelting = None
                self.progress = 0

    def render(self):
        c.screen.blit(i.images[id_map["furnace"]], (self.x - c.player_x, self.y - c.player_y))
        if self.progress != 0 and self.progress < c.smelt_time:
            pg.draw.rect(c.screen, c.working_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 2)
        elif self.progress >= c.smelt_time:
            pg.draw.rect(c.screen, c.full_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 3)

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