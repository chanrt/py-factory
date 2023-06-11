import numpy as np

from constants import consts as c
from conveyor import Conveyor
from id_mapping import id_map
from images import img as i


class Item:
    def __init__(self, row, col, item):
        self.item = item
        self.row = row
        self.col = col
        self.calc_position()

        self.last_dir = None
        self.caught = False
        self.display = True

    def move(self, direction):
        if self.last_dir is not None and direction != self.last_dir:
            self.calc_position()

        if direction == "left":
            self.x -= c.conveyor_speed * c.dt
        elif direction == "right":
            self.x += c.conveyor_speed * c.dt
        elif direction == "up":
            self.y -= c.conveyor_speed * c.dt
        elif direction == "down":
            self.y += c.conveyor_speed * c.dt

        self.last_dir = direction

        self.row = int(self.y / c.cell_length)
        self.col = int(self.x / c.cell_length)

    def calc_position(self):
        self.x = self.col * c.cell_length + c.cell_length // 2
        self.y = self.row * c.cell_length + c.cell_length // 2

    def render(self):
        if self.display:
            c.screen.blit(i.images[self.item], (self.x - c.player_x - c.cell_length // 2, self.y - c.player_y - c.cell_length // 2))


class ItemManager:
    def __init__(self):
        self.grid = []
        for _ in range(c.num_cells):
            new_row = [0 for _ in range(c.num_cells)]
            self.grid.append(new_row)
        self.items = []

    def update(self, sm):
        for item in self.items:
            old_row, old_col = item.row, item.col

            if not item.caught and isinstance(sm.grid[old_row][old_col], Conveyor):
                conveyor_direction = sm.grid[old_row][old_col].direction

                if conveyor_direction == 0 and self.grid[old_row - 1][old_col] == 0:
                    item.move("up")
                elif conveyor_direction == 1 and self.grid[old_row][old_col + 1] == 0:
                    item.move("right")
                elif conveyor_direction == 2 and self.grid[old_row + 1][old_col] == 0:
                    item.move("down")
                elif conveyor_direction == 3 and self.grid[old_row][old_col - 1] == 0:
                    item.move("left")

                new_row, new_col = item.row, item.col
                if old_row != new_row or old_col != new_col:
                    self.grid[old_row][old_col] = 0
                    self.grid[new_row][new_col] = item

    def render(self):
        for item in self.items:
            item.render()

    def add(self, row, col, item):
        new_item = Item(row, col, item)
        self.grid[row][col] = new_item
        self.items.append(new_item)

    def remove(self, row, col):
        if self.grid[row][col] != 0:
            item_to_be_removed = self.grid[row][col]
            self.grid[row][col] = 0
            self.items.remove(item_to_be_removed)

    def fetch_item(self, row, col):
        if self.grid[row][col] != 0:
            item_to_be_fetched = self.grid[row][col]
            self.grid[row][col] = 0
            return item_to_be_fetched
        
    def drop_item(self, item, x, y):
        row = int(y / c.cell_length)
        col = int(x / c.cell_length)
        self.grid[row][col] = item
        
        item.row = row
        item.col = col
        item.calc_position()

    def contains_ore(self, row, col):
        if self.grid[row][col] != 0 and self.grid[row][col].item in [id_map["iron_ore"], id_map["copper_ore"]]:
            return True
        else:
            return False

item_manager = ItemManager()