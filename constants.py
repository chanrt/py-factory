from os import path
import pygame as pg

from id_mapping import id_map
from loader import get_resource_path


class Constants:

    def __init__(self):
        self.fps = 120
        self.frame = 0
        self.dt = 1.0 / self.fps

        self.num_cells = 100
        self.cell_length = 35

        self.player_x = 0
        self.player_y = 0
    
        self.show_gridlines = True
        self.const_state = 1
        self.rot_state = 0
        self.ug_state = 3
        self.buffer_size = 4

        self.music_padding = 5
        self.ui_icon_size = 30

        self.set_colors()
        self.set_speeds()
        self.load_sounds()
        self.load_fonts()

    def set_colors(self):
        self.bg_color = pg.Color("#222222")
        self.grid_color = pg.Color("#666666")

        self.arm_color = pg.Color("#ffff00")
        self.action_color = pg.Color("#00ff00")
        self.error_color = pg.Color("#ff0000")
        self.source_color = pg.Color("#ff3131")
        self.target_color = pg.Color("#2196f3")
        self.working_color = pg.Color("#00ff00")
        self.full_color = pg.Color("#ff0000")

        self.ore_colors = dict([
            (id_map["coal"], pg.Color("#151716")),
            (id_map["iron_ore"], pg.Color("#a19d94")),
            (id_map["copper_ore"], pg.Color("#b87333")),
        ])

    def set_speeds(self):
        self.player_speed = 200
        self.conveyor_speed = self.cell_length
        self.arm_speed = 90 * 3.14 / 180

        self.mine_time = 2
        self.smelt_time = 3

    def load_sounds(self):
        pg.init()
        root = "sounds"
        self.conveyor_placed = pg.mixer.Sound(get_resource_path(path.join(root, "conveyor_placed.wav")))
        self.conveyor_placed.set_volume(0.33)
        self.structure_placed = pg.mixer.Sound(get_resource_path(path.join(root, "structure_placed.wav")))
        self.arm_placed = pg.mixer.Sound(get_resource_path(path.join(root, "arm_placed.wav")))
        self.mine_placed = pg.mixer.Sound(get_resource_path(path.join(root, "mine_placed.wav")))
        self.furnace_placed = pg.mixer.Sound(get_resource_path(path.join(root, "furnace_placed.wav")))
        self.factory_placed = pg.mixer.Sound(get_resource_path(path.join(root, "factory_placed.wav")))

        self.conveyor_pick_up = pg.mixer.Sound(get_resource_path(path.join(root, "conveyor_pick_up.wav")))
        self.conveyor_pick_up.set_volume(0.33)
        self.item_pick_up = pg.mixer.Sound(get_resource_path(path.join(root, "item_pick_up.wav")))
        self.structure_destroy = pg.mixer.Sound(get_resource_path(path.join(root, "structure_destroy.mp3")))
        self.structure_destroy.set_volume(0.5)

        self.rotate = pg.mixer.Sound(get_resource_path(path.join(root, "rotate.wav")))

    def load_fonts(self):
        self.title_font_size = 30
        self.orbitron = pg.font.Font(get_resource_path("fonts/Orbitron-Regular.ttf"), self.title_font_size)

        self.text_font_size = 20
        self.merriweather = pg.font.Font(get_resource_path("fonts/Merriweather-Regular.ttf"), self.text_font_size)

    def set_dt(self, dt):
        self.dt = dt
        self.frame += 1
        if self.frame == self.fps:
            self.frame = 0

    def set_screen(self, screen):
        self.screen = screen
        self.sw, self.sh = self.screen.get_size()

        self.button_width = self.sw / 5
        self.button_height = self.sh / 10

    def set_clock(self, clock):
        self.clock = clock

    def toggle_gridlines(self):
        self.show_gridlines = not self.show_gridlines

    def cycle_const_state(self, direction):
        self.const_state += direction
        if self.const_state < 1:
            self.const_state = 7
        elif self.const_state > 7:
            self.const_state = 1

    def cycle_rot_state(self, direction):
        self.rot_state = (self.rot_state + direction) % 4

    def cycle_ug_state(self, direction):
        self.ug_state += direction
        if self.ug_state < 2:
            self.ug_state = 4
        elif self.ug_state > 4:
            self.ug_state = 2


consts = Constants()