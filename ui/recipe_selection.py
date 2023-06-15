import pygame as pg

from constants import consts as c
from id_mapping import reverse_id_map
from recipes import recipes
from ui.button import Button


def select_recipe():
    num_columns = 3
    num_recipes = len(recipes)
    num_rows_req = num_recipes // num_columns + 1
    buttons = []

    for i in range(num_recipes):
        row = i // num_columns
        col = i % num_columns

        x = c.sw * (col + 1) / (num_columns + 1)
        y = c.sh * (row + 1) / (num_rows_req + 1)

        new_button = Button(x, y, c.button_width, c.button_height, c.screen, recipes[i]["name"])
        buttons.append(new_button)

    title_text = c.orbitron.render("Select a recipe", True, "white")

    for button in buttons:
        button.set_font(c.orbitron)

    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return None
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(num_recipes):
                    buttons[i].check_clicked(mouse_pos, event.button)
                    if buttons[i].left_clicked or buttons[i].right_clicked:
                        return i
        
        for button in buttons:
            button.update(mouse_pos)

        c.screen.fill(c.bg_color)

        c.screen.blit(title_text, ((c.sw - title_text.get_width()) / 2, c.title_font_size / 2))

        for button in buttons:
            button.render()

        for i, button in enumerate(buttons):
            if button.is_hovering:
                text = f"{recipes[i]['name']} requires "
                for item in recipes[i]["inputs"]:
                    text += f"{reverse_id_map[item].replace('_', ' ')} ({recipes[i]['inputs'][item]}) "

                recipe_text = c.merriweather.render(text, True, pg.Color("white"))
                x, y = pg.mouse.get_pos()
                c.screen.blit(recipe_text, (button.x - recipe_text.get_width() // 2, button.y - button.height))


        pg.display.flip()


if __name__ == '__main__':
    # this leads to the recipe selection screen
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    c.set_screen(screen)
    c.set_clock(clock)
    result = select_recipe()

    print("Recipe selected:", recipes[result]["name"])