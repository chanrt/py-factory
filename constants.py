import pygame as pg


class Constants:
    def __init__(self):
        self.num_cells = 100
        self.cell_length = 25

        self.player_x = 0
        self.player_y = 0
        self.player_speed = 1

        self.bg_color = pg.Color("#222222")
        self.grid_color = pg.Color("#aaaaaa")
        self.arm_color = pg.Color("#ffff00")

        self.show_gridlines = True
        self.const_state = 1

        self.conveyor_state = 1
        self.conveyor_speed = 0.2

        self.arm_state = 1
        self.arm_speed = 1 * 3.14 / 180

    def set_screen(self, screen):
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()

    def toggle_gridlines(self):
        self.show_gridlines = not self.show_gridlines

    def cycle_conveyor_state(self):
        self.conveyor_state += 1
        if self.conveyor_state > 4:
            self.conveyor_state = 1

    def cycle_arm_state(self):
        self.arm_state += 1
        if self.arm_state > 4:
            self.arm_state = 1


consts = Constants()