import pygame as pg
from numpy import cos, pi, sin

from constants import consts as c
from id_mapping import id_map
from images import img as i


class Arm:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()
        self.init_direction()

    def update(self, sm, im):
        self.calc_arm_coords()

        if self.caught_item is None:
            if self.angle == self.start_angle:
                if im.grid[self.source_row][self.source_col] != 0:
                    self.caught_item = im.fetch_item(self.source_row, self.source_col)
            else:
                self.angle += c.arm_speed * c.dt
                self.constrain_angle()
                if abs(self.angle - self.start_angle) < c.arm_speed * c.dt:
                    self.angle = self.start_angle
        else:
            self.angle -= c.arm_speed * c.dt
            self.constrain_angle()
            self.caught_item.x = self.end_x
            self.caught_item.y = self.end_y

            if abs(self.angle - self.stop_angle) < c.arm_speed * c.dt:
                if im.grid[self.target_row][self.target_col] == 0:
                    im.drop_item(self.caught_item, self.end_x, self.end_y)
                    self.caught_item = None      

    def render(self):
        c.screen.blit(i.images[id_map["arm"]], (self.x - c.player_x, self.y - c.player_y))
        pg.draw.line(c.screen, c.arm_color, (self.pivot_x, self.pivot_y), (self.end_x, self.end_y), 2)

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 4
        self.init_direction()

    def constrain_angle(self):
        while self.angle > 2 * pi:
                self.angle -= 2 * pi
        while self.angle < 0:
            self.angle += 2 * pi

    def init_direction(self):
        if self.direction == 0:
            self.start_angle = pi / 2
            self.stop_angle = 3 * pi / 2
            self.source_row = self.row - 1
            self.source_col = self.col
            self.target_row = self.row + 1
            self.target_col = self.col

        elif self.direction == 1:
            self.start_angle = 0
            self.stop_angle = pi
            self.source_row = self.row
            self.source_col = self.col + 1
            self.target_row = self.row
            self.target_col = self.col - 1

        elif self.direction == 2:
            self.start_angle = 3 * pi / 2
            self.stop_angle = pi / 2
            self.source_row = self.row + 1
            self.source_col = self.col
            self.target_row = self.row - 1
            self.target_col = self.col

        elif self.direction == 3:
            self.start_angle = pi
            self.stop_angle = 0
            self.source_row = self.row
            self.source_col = self.col - 1
            self.target_row = self.row
            self.target_col = self.col + 1

        self.angle = self.start_angle
        self.caught_item = None

    def calc_position(self):
        self.x = self.col * c.cell_length
        self.y = self.row * c.cell_length

    def calc_arm_coords(self):
        self.pivot_x = self.x - c.player_x + c.cell_length // 2
        self.pivot_y = self.y - c.player_y + c.cell_length // 2

        self.end_x = self.pivot_x + c.cell_length * cos(self.angle)
        self.end_y = self.pivot_y - c.cell_length * sin(self.angle)

    def safely_drop_item(self, im):
        if self.caught_item is not None:
            im.drop_item(self.caught_item, self.end_x, self.end_y)
            self.caught_item = None