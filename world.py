import pygame as pg
from numpy import zeros

from constants import consts as c
from id_mapping import id_map


def get_ore_from_value(value):
    for key in id_map:
        if id_map[key] == value:
            return key


class World:
    def __init__(self):
        self.grid = zeros((c.num_cells, c.num_cells), dtype=int)
        self.ore_locations = []

        self.grid[10:13, 10:12] = id_map["coal"]
        self.grid[15:17, 15:17] = id_map["iron_ore"]
        self.grid[15:17, 20:23] = id_map["copper_ore"]
        self.populate_ore_locations()

    def populate_ore_locations(self):
        for row in range(c.num_cells):
            for col in range(c.num_cells):
                if self.grid[row, col] > 0:
                    self.ore_locations.append((row, col))

    def render(self):
        for loc in self.ore_locations:
            row, col = loc
            x = col * c.cell_length - c.player_x
            y = row * c.cell_length - c.player_y
            pg.draw.rect(c.screen, c.ore_colors[self.grid[loc]], (x, y, c.cell_length, c.cell_length))

    def render_tooltip(self, row, col):
        x, y = pg.mouse.get_pos()
        ore = get_ore_from_value(self.grid[row, col]).replace("_", " ").title()
        ore_text = c.merriweather.render(ore, True, pg.Color("white"))
        c.screen.blit(ore_text, (x + 20, y + 20))


world = World()