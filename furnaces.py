import pygame as pg

from constants import consts as c
from grid import grid_manager as gm
from items import item_manager as im
from world import world as w


class Furnace:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.x = col * c.cell_length
        self.y = row * c.cell_length
        self.direction = direction

        if direction == 1:
            self.target_row = row - 1
            self.target_col = col
        elif direction == 2:
            self.target_row = row
            self.target_col = col + 1
        elif direction == 3:
            self.target_row = row + 1
            self.target_col = col
        elif direction == 4:
            self.target_row = row
            self.target_col = col - 1

        self.smelting = None
        self.progress = 0

    def update(self):
        if self.smelting is None:
            if im.contains_ore(self.row, self.col):
                self.smelting = im.item_grid[self.row][self.col]
                self.smelting.display = False
                self.progress = 0
        else: 
            if self.progress < c.smelt_time:
                self.progress += c.dt
            elif im.item_grid[self.target_row][self.target_col] == 0 and gm.item_can_be_placed((self.target_row, self.target_col)):
                im.remove_item(self.row, self.col)
                if self.smelting.item == 7:
                    smelted_item_index = 5
                elif self.smelting.item == 9:
                    smelted_item_index = 8

                im.add_item(smelted_item_index, self.target_row, self.target_col)
                self.smelting = None
                self.progress = 0

    def render(self):
        if self.progress != 0 and self.progress < c.smelt_time:
            pg.draw.rect(c.screen, c.working_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 2)
        elif self.progress >= c.smelt_time:
            pg.draw.rect(c.screen, c.full_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 3)


class FurnaceManager:
    def __init__(self):
        self.furnaces = []

    def add_furnace(self, row, col, direction):
        self.furnaces.append(Furnace(row, col, direction))

    def remove_furnace(self, row, col):
        for furnace in self.furnaces:
            if furnace.row == row and furnace.col == col:
                self.furnaces.remove(furnace)

    def update(self):
        for furnace in self.furnaces:
            furnace.update()

    def render(self):
        for furnace in self.furnaces:
            furnace.render()


furnace_manager = FurnaceManager()