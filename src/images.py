from os import path
import pygame as pg

from constants import consts as c
from id_mapping import id_map


class Images:
    def __init__(self):
        self.images = []

        for key, value in id_map.items():
            if value == 0:
                self.images.append(
                    Images.load_all_rotated_images(["data/sprites/conveyor.png"])
                )
            elif value == 1:
                self.images.append(
                    Images.load_all_rotated_images(
                        [
                            "data/sprites/conveyor_ug_source.png",
                            "data/sprites/conveyor_ug_target.png",
                        ]
                    )
                )
            elif value == 2:
                self.images.append(
                    Images.load_all_rotated_images(["data/sprites/splitter.png"])
                )
            else:
                image_file_name = key + ".png"
                image_path = path.join("data/sprites", image_file_name)
                self.images.append(Images.load_scale_image(image_path))

    @staticmethod
    def load_all_rotated_images(image_paths):
        images_list = []

        for image_path in image_paths:
            for direction in range(4):
                raw_image = pg.image.load(image_path)
                rotated_image = pg.transform.rotate(raw_image, -direction * 90)
                scaled_image = pg.transform.smoothscale(
                    rotated_image, (c.cell_length, c.cell_length)
                )
                images_list.append(scaled_image)

        return images_list

    @staticmethod
    def load_scale_image(image_path):
        raw_image = pg.image.load(image_path)
        scaled_image = pg.transform.smoothscale(
            raw_image, (c.cell_length, c.cell_length)
        )
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
