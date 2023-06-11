import pygame as pg
from numpy import cos, pi, sin

from grid import grid_manager as gm
from items import item_manager as im
from constants import consts as c
from images import img as i


class Arm:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.calc_position()
        self.direction = direction
        self.init_direction()

    def init_direction(self):
        if self.direction == 1:
            self.start_angle = pi / 2
            self.stop_angle = 3 * pi / 2
            self.source_row = self.row -1
            self.source_col = self.col
            self.target_row = self.row + 1
            self.target_col = self.col

        elif self.direction == 2:
            self.start_angle = 0
            self.stop_angle = pi
            self.source_row = self.row
            self.source_col = self.col + 1
            self.target_row = self.row
            self.target_col = self.col - 1

        elif self.direction == 3:
            self.start_angle = 3 * pi / 2
            self.stop_angle = pi / 2
            self.source_row = self.row + 1
            self.source_col = self.col
            self.target_row = self.row - 1
            self.target_col = self.col

        elif self.direction == 4:
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

    def update(self):
        self.calc_coords()

        if self.caught_item is None:
            if self.angle == self.start_angle:
                if im.item_grid[self.source_row][self.source_col] != 0:
                    # furnace check
                    if gm.grid[self.target_row][self.target_col] == 11:
                        if im.contains_ore(self.source_row, self.source_col):
                            self.caught_item = im.fetch_item(self.source_row, self.source_col)

                    else:
                        self.caught_item = im.fetch_item(self.source_row, self.source_col)
            else:
                self.angle += c.arm_speed * c.dt

                if self.angle > 2 * pi:
                    self.angle -= 2 * pi
                elif self.angle < 0:
                    self.angle += 2 * pi

                if abs(self.angle - self.start_angle) % (2 * pi) < c.arm_speed * c.dt:
                    self.angle = self.start_angle
        else:
            self.angle -= c.arm_speed * c.dt

            if self.angle < 0:
                self.angle += 2 * pi

            self.calc_coords()
            self.caught_item.x = self.end_x
            self.caught_item.y = self.end_y

            if abs(self.angle - self.stop_angle) % (2 * pi) < c.arm_speed * c.dt:
                if im.item_grid[self.target_row][self.target_col] == 0:
                    im.drop_item(self.caught_item, self.end_x, self.end_y)
                    self.caught_item = None
                    

    def calc_coords(self):
        self.pivot_x = self.x - c.player_x + c.cell_length // 2
        self.pivot_y = self.y - c.player_y + c.cell_length // 2

        self.end_x = self.pivot_x + c.cell_length * cos(self.angle)
        self.end_y = self.pivot_y - c.cell_length * sin(self.angle)

    def render(self):
        pg.draw.line(c.screen, c.arm_color, (self.pivot_x, self.pivot_y), (self.end_x, self.end_y), 2)

        if self.caught_item is not None:
            c.screen.blit(i.images[self.caught_item.item], (self.end_x - c.cell_length // 2, self.end_y - c.cell_length // 2))


class ArmManager:
    def __init__(self):
        self.arms = []

    def add_arm(self, row, col, direction):
        self.arms.append(Arm(row, col, direction))

    def remove_arm(self, row, col):
        for arm in self.arms:
            if arm.row == row and arm.col == col:
                if arm.caught_item is not None:
                    im.drop_item(arm.caught_item, arm.end_x, arm.end_y)
                self.arms.remove(arm)

    def toggle_rotation(self, row, col, direction = 1):
        for arm in self.arms:
            if arm.row == row and arm.col == col:
                new_direction = arm.direction + direction
                if new_direction > 3:
                    new_direction = 0
                elif new_direction < 0:
                    new_direction = 3
                    
                arm.direction = new_direction
                arm.init_direction()

    def update(self):
        for arm in self.arms:
            arm.update()

    def render(self):
        for arm in self.arms:
            arm.render()

    def apply_zoom(self):
        for arm in self.arms:
            arm.calc_position()


arm_manager = ArmManager()