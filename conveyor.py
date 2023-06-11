from constants import consts as c
from id_mapping import id_map
from images import img as i


class Conveyor:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.x = col * c.cell_length
        self.y = row * c.cell_length
        self.direction = direction

    def update(self, sm, im):
        pass

    def render(self):
        c.screen.blit(i.images[id_map["conveyor"]][self.direction], (self.x - c.player_x, self.y - c.player_y))

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 4

    