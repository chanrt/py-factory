from os import path
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
        self.ug_state = 3

        self.music_padding = 5
        self.ui_icon_size = 30

        self.set_colors()
        self.set_speeds()
        self.load_sounds()
        self.load_fonts()

    def set_colors(self):
        self.bg_color = pg.Color("#222222")
        self.grid_color = pg.Color("#999999")
        self.arm_color = pg.Color("#ffff00")
        self.action_color = pg.Color("#00ff00")
        self.error_color = pg.Color("#ff0000")
        self.source_color = pg.Color("#ff3131")
        self.target_color = pg.Color("#2196f3")
        self.working_color = pg.Color("#ffffff")
        self.full_color = pg.Color("#ffa500")

        self.ore_colors = dict(
            [
                (id_map["iron_ore"], pg.Color("#a19d94")),
                (id_map["copper_ore"], pg.Color("#b87333")),
            ]
        )

    def set_speeds(self):
        self.player_speed = 200
        self.conveyor_speed = self.cell_length
        self.arm_speed = 90 * 3.14 / 180

        self.mine_time = 2
        self.smelt_time = 3

    def load_sounds(self):
        pg.init()
        root = "data/sounds"
        self.structure_placed = pg.mixer.Sound(path.join(root, "structure_placed.wav"))
        self.arm_placed = pg.mixer.Sound(path.join(root, "arm_placed.wav"))
        self.mine_placed = pg.mixer.Sound(path.join(root, "mine_placed.wav"))
        self.furnace_placed = pg.mixer.Sound(path.join(root, "furnace_placed.wav"))
        self.factory_placed = pg.mixer.Sound(path.join(root, "factory_placed.wav"))

        self.item_pick_up = pg.mixer.Sound(path.join(root, "item_pick_up.wav"))
        self.structure_destroy = pg.mixer.Sound(
            path.join(root, "structure_destroy.mp3")
        )
        self.structure_destroy.set_volume(0.5)

        self.rotate = pg.mixer.Sound(path.join(root, "rotate.wav"))

    def load_fonts(self):
        self.title_font_size = 30
        self.orbitron = pg.font.Font(
            "data/fonts/Orbitron-Regular.ttf", self.title_font_size
        )

        self.text_font_size = 20
        self.merriweather = pg.font.Font(
            "data/fonts/Merriweather-Regular.ttf", self.text_font_size
        )

    def set_dt(self, dt):
        self.dt = dt

    def set_screen(self, screen):
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()

        self.button_width = self.sw / 5
        self.button_height = self.sh / 10

    def set_clock(self, clock):
        self.clock = clock

    def toggle_gridlines(self):
        self.show_gridlines = not self.show_gridlines

    def cycle_rot_state(self, direction):
        self.rot_state = (self.rot_state + direction) % 4

    def cycle_ug_state(self, direction):
        self.ug_state += direction
        if self.ug_state < 2:
            self.ug_state = 4
        elif self.ug_state > 4:
            self.ug_state = 2


consts = Constants()