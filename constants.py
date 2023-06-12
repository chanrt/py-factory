import pygame as pg
from id_mapping import id_map


class Constants:
    def __init__(self):
        self.fps = 30
        self.dt = 1.0 / self.fps

        self.num_cells = 100
        self.cell_length = 35

        self.player_x = 0
        self.player_y = 0
    
        self.show_gridlines = True
        self.const_state = 1
        self.rot_state = 0

        self.set_colors()
        self.set_speeds()

    def set_colors(self):
        self.bg_color = pg.Color("#222222")
        self.grid_color = pg.Color("#aaaaaa")
        self.arm_color = pg.Color("#ffff00")
        self.action_color = pg.Color("#00ff00")
        self.source_color = pg.Color("#ff0000")
        self.target_color = pg.Color("#2196f3")
        self.working_color = pg.Color("#ffffff")
        self.full_color = pg.Color("#ffa500")

        self.ore_colors = dict([
            (id_map["iron_ore"], pg.Color("#a19d94")),
            (id_map["copper_ore"], pg.Color("#b87333")),
        ])

    def set_speeds(self):
        self.player_speed = 200
        self.conveyor_speed = 25
        self.arm_speed = 90 * 3.14 / 180

        self.mine_time = 2
        self.smelt_time = 3

    def set_dt(self, dt):
        self.dt = dt

    def set_screen(self, screen):
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()

    def set_clock(self, clock):
        self.clock = clock

    def toggle_gridlines(self):
        self.show_gridlines = not self.show_gridlines

    def cycle_rot_state(self, direction):
        self.rot_state = (self.rot_state + direction) % 4


consts = Constants()