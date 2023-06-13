from os import path
import pygame as pg

from constants import consts as c


class UI:
    def __init__(self):
        self.root = "sprites"
        self.sprite_names = [
            "conveyor",
            "conveyor_ug_source",
            "splitter",
            "arm",
            "mine",
            "furnace",
            "factory",
        ]
        self.sprites = []
        for name in self.sprite_names:
            self.sprites.append(self.load_scale_image(name))

    def load_scale_image(self, name):
        image = pg.image.load(path.join(self.root, name + ".png"))
        return pg.transform.smoothscale(image, (c.ui_icon_size, c.ui_icon_size))
    
    def update_selection(self, selection):
        self.current_selection = selection
    
    def render(self):
        partition = (c.sw // (len(self.sprites) + 1)) / 2

        for i in range(len(self.sprites)):
            x = c.sw // 2 + (i + 1) * partition
            y = c.sh - 1.5 * c.ui_icon_size
            c.screen.blit(self.sprites[i], (x, y))

            if i + 1 == c.const_state:
                pg.draw.rect(c.screen, pg.Color("white"), (x, y, c.ui_icon_size, c.ui_icon_size), 3)

            number = c.orbitron.render(str(i + 1), True, pg.Color("white"))
            c.screen.blit(number, (x, y - 1.5 * c.ui_icon_size))

ui = UI()