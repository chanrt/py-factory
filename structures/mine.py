import pygame as pg

from constants import consts as c
from id_mapping import id_map, reverse_id_map
from images import img as i
from world import world as w
from ui.game_ui import ui


class Mine:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction

        self.init_target()
        self.calc_position()

        self.mining = None
        self.progress = 0
        self.target_blocked = False
        self.buffer = []

    def update(self, sm, im):
        if self.mining is None and len(self.buffer) < c.buffer_size:
            if w.grid[self.row][self.col] > 0:
                self.mining = w.grid[self.row][self.col]
                self.progress = 0
        else:
            if self.progress < c.mine_time:
                self.progress += c.dt
            elif len(self.buffer) < c.buffer_size:
                self.buffer.append(self.mining)
                self.mining = None
                self.progress = 0
    
        if len(self.buffer) > 0:
            if im.grid[self.target_row][self.target_col] == 0 and sm.item_can_be_placed(self.target_row, self.target_col):
                im.add(self.target_row, self.target_col, self.buffer.pop(0))

    def render(self):
        c.screen.blit(i.images[id_map["mine"]], (self.x - c.player_x, self.y - c.player_y))

        if self.progress != 0 and self.progress < c.mine_time:
            pg.draw.rect(c.screen, c.working_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 2)
        elif len(self.buffer) == c.buffer_size:
            pg.draw.rect(c.screen, c.full_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 3)

    def render_tooltip(self):
        pg.draw.rect(c.screen, c.target_color, (self.target_col * c.cell_length - c.player_x, self.target_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)

        if w.grid[self.row][self.col] == 0:
            status = "NO ORE"
        elif len(self.buffer) == c.buffer_size:
            status = "FULL"
        elif self.progress < c.mine_time:
            status = "WORKING"
        else:
            status = "ERROR"
        
        ui.render_text(f"Mine [{status}]: (L/R) to rotate")

        if len(self.buffer) > 0:
            item_text = f"{len(self.buffer)} {reverse_id_map[self.buffer[0]].replace('_', ' ')}(s) in buffer"
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