from constants import consts as c
from id_mapping import id_map
from images import img as i


class Conveyor:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()

    def update(self, sm, im):
        pass

    def render(self):
        c.screen.blit(i.images[id_map["conveyor"]][self.direction], (self.x - c.player_x, self.y - c.player_y))

    def render_tooltip(self):
        pass

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 4

    def calc_position(self):
        self.x = self.col * c.cell_length
        self.y = self.row * c.cell_length