import pygame as pg

from constants import consts as c


class Images:
    def __init__(self):
        self.images = []
        for direction in ["up", "right", "down", "left"]:
            raw_image = pg.image.load(f"sprites/conveyor_{direction}.png")
            scaled_image = pg.transform.scale(raw_image, (c.cell_length, c.cell_length))
            self.images.append(scaled_image)


img = Images()