import pygame as pg

from constants import consts as c
from id_mapping import id_map
from images import img as i
from recipes import recipes


class Factory:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()
        self.init_target()

        self.recipe = 0
        self.storage = []
        self.progress = 0
        
    def update(self, sm, im):
        if im.grid[self.row][self.col] != 0:
            item_inside = im.grid[self.row][self.col]
            if self.will_accept_item(item_inside.item):
                self.storage.append(item_inside.item)
                im.remove(self.row, self.col)

        if self.recipe_fulfilled():
            self.progress += c.dt

            if self.progress > recipes[self.recipe]["time"]:
                if im.grid[self.target_row][self.target_col] == 0 and sm.item_can_be_placed(self.target_row, self.target_col):
                    self.progress = 0
                    self.storage = []
                    im.add(self.target_row, self.target_col, recipes[self.recipe]["output"])

    def render(self):
        c.screen.blit(i.images[id_map["factory"]], (self.x - c.player_x, self.y - c.player_y))

        if self.recipe is not None:
            if self.progress != 0 and self.progress < recipes[self.recipe]["time"]:
                pg.draw.rect(c.screen, c.working_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 2)
            elif self.progress >= recipes[self.recipe]["time"]:
                pg.draw.rect(c.screen, c.full_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 3)

    def render_tooltip(self):
        pg.draw.rect(c.screen, c.target_color, (self.target_col * c.cell_length - c.player_x, self.target_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)

    def will_accept_item(self, item):
        if self.recipe is None:
            return False

        if item in recipes[self.recipe]["inputs"]:
            num_in_storage = sum([1 for stored_item in self.storage if stored_item == item])
            if num_in_storage < recipes[self.recipe]["inputs"][item]:
                return True
            else:
                return False
        else:
            return False
        
    def recipe_fulfilled(self):
        for item in recipes[self.recipe]["inputs"]:
            num_in_storage = sum([1 for stored_item in self.storage if stored_item == item])

            if num_in_storage < recipes[self.recipe]["inputs"][item]:
                return False

        return True

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