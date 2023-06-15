import pygame as pg

from constants import consts as c
from id_mapping import id_map
from images import img as i
from ui.game_ui import ui


class Conveyor:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()
        self.init_squares()

    def update(self, sm, im):
        pass

    def render(self):
        c.screen.blit(i.images[id_map["conveyor"]][self.direction], (self.x - c.player_x, self.y - c.player_y))

    def render_tooltip(self):
        pg.draw.rect(c.screen, c.source_color, (self.source_col * c.cell_length - c.player_x, self.source_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)
        pg.draw.rect(c.screen, c.target_color, (self.target_col * c.cell_length - c.player_x, self.target_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)
        ui.render_text("Conveyor [WORKING]: (L/R) to rotate")

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 4

    def calc_position(self):
        self.x = self.col * c.cell_length
        self.y = self.row * c.cell_length

    def init_squares(self):
        if self.direction == 0:
            self.source_row = self.row + 1
            self.source_col = self.col
            self.target_row = self.row - 1
            self.target_col = self.col
        elif self.direction == 1:
            self.source_row = self.row
            self.source_col = self.col - 1
            self.target_row = self.row
            self.target_col = self.col + 1
        elif self.direction == 2:
            self.source_row = self.row - 1
            self.source_col = self.col
            self.target_row = self.row + 1
            self.target_col = self.col
        elif self.direction == 3:
            self.source_row = self.row
            self.source_col = self.col + 1
            self.target_row = self.row
            self.target_col = self.col - 1


class ConveyorUnderground:
    def __init__(self, row, col, direction):
        self.source_row = row
        self.source_col = col
        self.direction = direction
        self.length = c.ug_state

        self.init_target()
        self.calc_position()
        
        self.storage = []
        self.timers = []
        self.items_removed = []

    def update(self, sm, im):
        # decrease timers of all items in storage
        for i in range(len(self.timers)):
            self.timers[i] += c.dt

        # check if the first item in storage is ready to come out
        if len(self.storage) > 0:
            if self.timers[0] > self.moving_time:
                if im.grid[self.target_row][self.target_col] == 0 and sm.item_can_be_placed(self.target_row, self.target_col):
                    im.add(self.target_row, self.target_col, self.storage[0].item)
                    self.storage.pop(0)
                    self.timers.pop(0)

        # check for new items being added
        if im.grid[self.source_row][self.source_col] != 0 and len(self.storage) < self.length:
            item = im.grid[self.source_row][self.source_col]
            self.storage.append(item)
            self.timers.append(0)
            im.remove(self.source_row, self.source_col)

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

        if len(self.storage) == self.length:
            status = "FULL"
        elif len(self.storage) == 0:
            status = "EMPTY"
        else:
            status = "WORKING"
        ui.render_text(f"Underground Conveyor [{status}]")

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
        self.moving_time = self.length * c.cell_length / c.conveyor_speed

    def can_accept_item(self, row, col):
        if row != self.source_row or col != self.source_col:
            return True
        elif len(self.storage) == self.length:
            return False
        else:
            return True