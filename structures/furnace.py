import pygame as pg

from constants import consts as c
from id_mapping import id_map, reverse_id_map
from images import img as i
from ui.game_ui import ui


class Furnace:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()
        self.init_target()

        self.smelting = None
        self.buffer = []
        self.progress = 0

    def update(self, sm, im):
        if self.smelting is None:
            if im.contains_ore(self.row, self.col):
                self.smelting = im.grid[self.row][self.col]
                im.remove(self.row, self.col)
                self.progress = 0
        else: 
            if self.progress < c.smelt_time:
                self.progress += c.dt
            elif len(self.buffer) < c.buffer_size:
                if self.smelting.item == id_map["iron_ore"]:
                    smelted_item_index = id_map["iron"]
                elif self.smelting.item == id_map["copper_ore"]:
                    smelted_item_index = id_map["copper"]

                self.buffer.append(smelted_item_index)
                self.smelting = None
                self.progress = 0

        if len(self.buffer) > 0:
            if im.grid[self.target_row][self.target_col] == 0 and sm.item_can_be_placed(self.target_row, self.target_col):
                im.add(self.target_row, self.target_col, self.buffer.pop(0))

    def render(self):
        c.screen.blit(i.images[id_map["furnace"]], (self.x - c.player_x, self.y - c.player_y))
        if self.progress != 0 and self.progress < c.smelt_time:
            pg.draw.rect(c.screen, c.working_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 2)
        elif len(self.buffer) == c.buffer_size:
            pg.draw.rect(c.screen, c.full_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 3)

    def render_tooltip(self):
        pg.draw.rect(c.screen, c.target_color, (self.target_col * c.cell_length - c.player_x, self.target_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)

        if len(self.buffer) == c.buffer_size:
            status = "FULL"
        elif self.smelting is None:
            status = "EMPTY"
        elif self.progress < c.smelt_time:
            status = "WORKING"
        else:
            status = "ERROR"

        ui.render_text(f"Furnace [{status}]: (L/R) to rotate")

        if len(self.buffer) > 0:
            item_text = f"{len(self.buffer)} metals(s) in buffer"
            ui.render_desc(item_text)

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

    def will_accept_item(self, item):
        if "ore" in reverse_id_map[item] and len(self.buffer) < c.buffer_size:
            return True
        else:
            return False