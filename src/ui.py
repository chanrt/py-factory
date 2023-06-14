from os import path
import pygame as pg

from constants import consts as c


class UI:
    def __init__(self):
        self.root = "data/sprites"
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

        self.numbers = []
        for i in range(len(self.sprites)):
            self.numbers.append(
                c.merriweather.render(str(i + 1), True, pg.Color("white"))
            )

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
                pg.draw.rect(
                    c.screen,
                    pg.Color("white"),
                    (x, y, c.ui_icon_size, c.ui_icon_size),
                    3,
                )

            c.screen.blit(
                self.numbers[i],
                (x + self.numbers[i].get_width() // 2, y - 1 * c.ui_icon_size),
            )

    def render_text(self, text):
        text = c.merriweather.render(text, True, pg.Color("white"))
        c.screen.blit(
            text,
            (1.5 * c.ui_icon_size, 3 * c.title_font_size),
        )


ui = UI()