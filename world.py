from numpy import zeros
import pygame as pg

from constants import consts as c
from id_mapping import id_map


class World:
    def __init__(self):
        self.world = zeros((c.num_cells, c.num_cells), dtype=int)
        self.ore_locations = []

        self.world[15:17, 15:17] = id_map["iron_ore"]
        self.world[15:17, 20:23] = id_map["copper_ore"]
        self.populate_ore_locations()

    def populate_ore_locations(self):
        for row in range(c.num_cells):
            for col in range(c.num_cells):
                if self.world[row, col] > 0:
                    self.ore_locations.append((row, col))

    def render(self):
        for loc in self.ore_locations:
            row, col = loc
            x = col * c.cell_length - c.player_x
            y = row * c.cell_length - c.player_y
            pg.draw.rect(c.screen, c.ore_colors[self.world[loc]], (x, y, c.cell_length, c.cell_length))


world = World()