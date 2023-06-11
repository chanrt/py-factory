import pygame as pg


class Constants:
    def __init__(self):
        self.fps = 30
        self.dt = 1.0 / self.fps

        self.num_cells = 100
        self.cell_length = 25

        self.player_x = 0
        self.player_y = 0
    
        self.show_gridlines = True
        self.const_state = 1

        self.conveyor_state = 1
        self.arm_state = 1
        self.mine_state = 1
        self.furnace_state = 1

        self.set_colors()
        self.set_speeds()

    def set_colors(self):
        self.bg_color = pg.Color("#222222")
        self.grid_color = pg.Color("#aaaaaa")
        self.arm_color = pg.Color("#ffff00")
        self.action_color = pg.Color("#00ff00")
        self.source_color = pg.Color("#ff0000")
        self.sink_color = pg.Color("#0000ff")
        self.working_color = pg.Color("#ffffff")
        self.full_color = pg.Color("#ffa500")

        self.ore_colors = [None, pg.Color("#a19d94"), pg.Color("#b87333")]

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

    def cycle_conveyor_state(self, direction = 1):
        self.conveyor_state += direction
        if self.conveyor_state > 4:
            self.conveyor_state = 1
        elif self.conveyor_state < 1:
            self.conveyor_state = 4

    def cycle_arm_state(self, direction = 1):
        self.arm_state += direction
        if self.arm_state > 4:
            self.arm_state = 1
        elif self.arm_state < 1:
            self.arm_state = 4

    def cycle_mine_state(self, direction = 1):
        self.mine_state += direction
        if self.mine_state > 4:
            self.mine_state = 1
        elif self.mine_state < 1:
            self.mine_state = 4

    def cycle_furnace_state(self, direction = 1):
        self.furnace_state += direction
        if self.furnace_state > 4:
            self.furnace_state = 1
        elif self.furnace_state < 1:
            self.furnace_state = 4


consts = Constants()