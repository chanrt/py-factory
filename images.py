import pygame as pg

from constants import consts as c


class Images:
    def __init__(self):
        self.images = [None]

        # 1 - 4: conveyor belts (up, right, down, left)
        for direction in range(4):
            raw_image = pg.image.load("sprites/conveyor.png")
            rotated_image = pg.transform.rotate(raw_image, -direction * 90)
            scaled_image = pg.transform.smoothscale(rotated_image, (c.cell_length, c.cell_length))
            self.images.append(scaled_image)

        # 5: iron
        self.images.append(self.load_scale_image("sprites/iron.png"))

        # 6: arm
        self.images.append(self.load_scale_image("sprites/arm.png"))

    def load_scale_image(self, path):
        raw_image = pg.image.load(path)
        scaled_image = pg.transform.smoothscale(raw_image, (c.cell_length, c.cell_length))
        return scaled_image
    
    def reload_images(self):
        self.__init__()

img = Images()