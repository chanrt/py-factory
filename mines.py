import pygame as pg

from constants import consts as c
from grid import grid_manager as gm
from items import item_manager as im
from world import world as w


class Mine:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.x = col * c.cell_length
        self.y = row * c.cell_length

        self.direction = direction
        self.init_target()

        self.mining = None
        self.progress = 0

    def init_target(self):
        if self.direction == 1:
            self.target_row = self.row - 1
            self.target_col = self.col
        elif self.direction == 2:
            self.target_row = self.row
            self.target_col = self.col + 1
        elif self.direction == 3:
            self.target_row = self.row + 1
            self.target_col = self.col
        elif self.direction == 4:
            self.target_row = self.row
            self.target_col = self.col - 1

    def update(self):
        if self.mining is None:
            if w.world[self.row][self.col] > 0:
                self.mining = w.world[self.row][self.col]
                self.progress = 0
        else:
            if self.progress < c.mine_time:
                self.progress += c.dt
            elif im.item_grid[self.target_row][self.target_col] == 0 and gm.item_can_be_placed((self.target_row, self.target_col)):
                if self.mining == 1:
                    im.add_item(7, self.target_row, self.target_col)
                if self.mining == 2:
                    im.add_item(9, self.target_row, self.target_col)

                self.mining = None
                self.progress = 0

    def render(self):
        if self.progress != 0 and self.progress < c.mine_time:
            pg.draw.rect(c.screen, c.working_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 2)
        elif self.progress >= c.mine_time:
            pg.draw.rect(c.screen, c.full_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 3)
        

class MineManager:
    def __init__(self):
        self.mines = []

    def add_mine(self, row, col, direction):
        self.mines.append(Mine(row, col, direction))

    def remove_mine(self, row, col):
        for mine in self.mines:
            if mine.row == row and mine.col == col:
                self.mines.remove(mine)

    def toggle_rotation(self, row, col):
        for mine in self.mines:
            if mine.row == row and mine.col == col:
                if mine.direction == 4:
                    mine.direction = 1
                else:
                    mine.direction += 1
                mine.init_target()

    def update(self):
        for mine in self.mines:
            mine.update()

    def render(self):
        for mine in self.mines:
            mine.render()


mine_manager = MineManager()