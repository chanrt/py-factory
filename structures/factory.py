import pygame as pg

from constants import consts as c
from id_mapping import id_map, reverse_id_map
from images import img as i
from recipes import recipes
from ui.game_ui import ui


class Factory:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
        self.calc_position()
        self.init_target()

        self.recipe = None
        self.storage = []
        self.buffer = []
        self.progress = 0
        
    def update(self, sm, im):
        if self.recipe is None:
            im.remove(self.row, self.col)

        if im.grid[self.row][self.col] != 0:
            item_inside = im.grid[self.row][self.col]
            if self.will_accept_item(item_inside.item):
                self.storage.append(item_inside.item)
            im.remove(self.row, self.col)

        if self.recipe_fulfilled():
            self.progress += c.dt

            if self.progress > recipes[self.recipe]["time"]:
                if len(self.buffer) < c.buffer_size:
                    self.progress = 0
                    self.buffer.append(recipes[self.recipe]["output"])
                    self.storage = []
        
        if len(self.buffer) > 0:
            if im.grid[self.target_row][self.target_col] == 0 and sm.item_can_be_placed(self.target_row, self.target_col):
                im.add(self.target_row, self.target_col, self.buffer.pop(0))

    def render(self):
        c.screen.blit(i.images[id_map["factory"]], (self.x - c.player_x, self.y - c.player_y))

        if self.recipe is not None:
            if self.progress != 0 and self.progress < recipes[self.recipe]["time"]:
                pg.draw.rect(c.screen, c.working_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 2)
            elif len(self.buffer) == c.buffer_size:
                pg.draw.rect(c.screen, c.full_color, (self.x - c.player_x, self.y - c.player_y, c.cell_length, c.cell_length), 3)
        else:
            pg.draw.circle(c.screen, c.error_color, (self.x - c.player_x + c.cell_length // 2, self.y - c.player_y + c.cell_length // 2), 4 * c.cell_length // 5, 2)

    def render_tooltip(self):
        pg.draw.rect(c.screen, c.target_color, (self.target_col * c.cell_length - c.player_x, self.target_row * c.cell_length - c.player_y, c.cell_length, c.cell_length), 3)

        if self.recipe is None:
            status = "NO RECIPE"
            ui.render_text(f"Factory [{status}]: (L/R) to rotate, (LMB) to select recipe")
        else: 
            if len(self.buffer) == c.buffer_size:
                status = "FULL"
            elif self.progress == 0:
                status = "WAITING"
            elif self.progress < recipes[self.recipe]["time"]:
                status = "WORKING"
            else:
                status = "ERROR"

            producing_item = recipes[self.recipe]["name"]
            ui.render_text(f"Factory [{status}]: Producing {producing_item} (L/R) to rotate, (LMB) to select recipe")
        
        self.render_recipe()

        if len(self.buffer) > 0:
            item_text = f"{len(self.buffer)} {reverse_id_map[self.buffer[0]].replace('_', ' ')}(s) in buffer"
            ui.render_desc(item_text)

    def render_recipe(self):
        if self.recipe is not None:
            rel_x = self.x - c.player_x + (c.cell_length - self.recipe_text.get_width()) // 2

            if self.direction == 0:
                rel_y = self.y - c.player_y + 1.5 * c.cell_length
            else:
                rel_y = self.y - c.player_y - c.cell_length
            pg.draw.rect(c.screen, pg.Color("black"), (rel_x - 5, rel_y - 5, self.recipe_text.get_width() + 10, self.recipe_text.get_height() + 10))
            c.screen.blit(self.recipe_text, (rel_x, rel_y))

    def set_recipe(self, recipe):
        if self.recipe is None or recipe is not None:
            self.recipe = recipe
            self.compose_recipe_text()
            self.storage = []
            self.progress = 0

    def compose_recipe_text(self):
        if self.recipe is not None:
            text = f"{recipes[self.recipe]['name']} requires "
            for item in recipes[self.recipe]["inputs"]:
                text += f"{reverse_id_map[item].replace('_', ' ')} ({recipes[self.recipe]['inputs'][item]}) "
            self.recipe_text = c.merriweather.render(text, True, pg.Color("white"))
    
    def will_accept_item(self, item):
        if self.recipe is None:
            return False
        
        if len(self.buffer) == c.buffer_size:
            return False

        if item in recipes[self.recipe]["inputs"]:
            num_in_storage = sum([1 for stored_item in self.storage if stored_item == item])
            if num_in_storage < recipes[self.recipe]["inputs"][item]:
                return True
            else:
                return False
        else:
            return False
        
    def recipe_fulfilled(self):
        if self.recipe is None:
            return False
        
        for item in recipes[self.recipe]["inputs"]:
            num_in_storage = sum([1 for stored_item in self.storage if stored_item == item])

            if num_in_storage < recipes[self.recipe]["inputs"][item]:
                return False

        return True

    def rotate(self, direction):
        self.direction = (self.direction + direction) % 4
        self.init_target()

    def init_target(self):
        if self.direction == 0:
            self.target_row = self.row - 1
            self.target_col = self.col
        elif self.direction == 1:
            self.target_row = self.row
            self.target_col = self.col + 1
        elif self.direction == 2:
            self.target_row = self.row + 1
            self.target_col = self.col
        elif self.direction == 3:
            self.target_row = self.row
            self.target_col = self.col - 1

    def calc_position(self):
        self.x = self.col * c.cell_length
        self.y = self.row * c.cell_length