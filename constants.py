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
        self.highlight_color = pg.Color("#ff0000")

        self.show_gridlines = True
        self.const_state = 1
        self.conveyor_state = 1

    def set_screen(self, screen):
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()

    def toggle_gridlines(self):
        self.show_gridlines = not self.show_gridlines

    def cycle_conveyor_state(self):
        self.conveyor_state += 1
        if self.conveyor_state > 4:
            self.conveyor_state = 1


consts = Constants()