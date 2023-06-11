import pygame as pg

from constants import consts as c


class Images:
    def __init__(self):
        self.images = []

        # images should be loaded in the same order as the id_map in id_mapping.py
        conveyor_list = []
        for direction in range(4):
            raw_image = pg.image.load("sprites/conveyor.png")
            rotated_image = pg.transform.rotate(raw_image, -direction * 90)
            scaled_image = pg.transform.smoothscale(rotated_image, (c.cell_length, c.cell_length))
            conveyor_list.append(scaled_image)
        self.images.append(conveyor_list)
        self.images.append(self.load_scale_image("sprites/arm.png"))
        self.images.append(self.load_scale_image("sprites/mine.png"))
        self.images.append(self.load_scale_image("sprites/furnace.png"))
        self.images.append(self.load_scale_image("sprites/factory.png"))

        self.images.append(self.load_scale_image("sprites/iron.png"))
        self.images.append(self.load_scale_image("sprites/iron_ore.png"))
        self.images.append(self.load_scale_image("sprites/copper.png"))
        self.images.append(self.load_scale_image("sprites/copper_ore.png"))

    def load_scale_image(self, path):
        raw_image = pg.image.load(path)
        scaled_image = pg.transform.smoothscale(raw_image, (c.cell_length, c.cell_length))
        return scaled_image
    
    def convert_alpha(self):
        for i in range(1, len(self.images)):
            if type(self.images[i]) == list:
                for j in range(len(self.images[i])):
                    self.images[i][j] = self.images[i][j].convert_alpha()
            else:
                self.images[i] = self.images[i].convert_alpha()
    
    def reload_images(self):
        self.__init__()

img = Images()