import numpy as np

from constants import consts as c
from grid import grid_manager as gm
from images import img as i


class Item:
    def __init__(self, item, row, col):
        self.item = item
        self.row = row
        self.col = col
        self.calc_position()

        self.last_dir = None
        self.caught = False

    def move(self, direction):
        if self.last_dir is not None and direction != self.last_dir:
            self.calc_position()

        if direction == "left":
            self.x -= c.conveyor_speed
        elif direction == "right":
            self.x += c.conveyor_speed
        elif direction == "up":
            self.y -= c.conveyor_speed
        elif direction == "down":
            self.y += c.conveyor_speed

        self.last_dir = direction

        self.row = int(self.y / c.cell_length)
        self.col = int(self.x / c.cell_length)

    def calc_position(self):
        self.x = self.col * c.cell_length + c.cell_length // 2
        self.y = self.row * c.cell_length + c.cell_length // 2

    def render(self):
        c.screen.blit(i.images[self.item], (self.x - c.player_x - c.cell_length // 2, self.y - c.player_y - c.cell_length // 2))


class ItemManager:
    def __init__(self):
        self.item_grid = np.zeros((c.num_cells, c.num_cells), dtype=int)
        self.items = []

    def add_item(self, item, row, col):
        self.items.append(Item(item, row, col))
        self.item_grid[row, col] = item

    def remove_item(self, row, col):
        for item in self.items:
            if item.row == row and item.col == col:
                self.items.remove(item)
                self.item_grid[row, col] = 0
                return

    def fetch_item(self, row, col):
        for item in self.items:
            if item.row == row and item.col == col:
                item.caught = True
                self.item_grid[row, col] = 0
                return item
            
    def drop_item(self, item, end_x, end_y):
        item.caught = False
        item.row = int(end_y / c.cell_length)
        item.col = int(end_x / c.cell_length)

        if self.item_grid[item.row, item.col] == 0:
            item.calc_position()
            self.item_grid[item.row, item.col] = item.item
        else:
            self.items.remove(item)

    def update(self):
        for item in [item for item in self.items if not item.caught]:
            old_row, old_col = item.row, item.col

            if 0 < gm.grid[old_row, old_col] < 5:
                if gm.grid[old_row, old_col] == 1 and self.item_grid[old_row - 1, old_col] == 0:
                    item.move("up")
                elif gm.grid[old_row, old_col] == 2 and self.item_grid[old_row, old_col + 1] == 0:
                    item.move("right")
                elif gm.grid[old_row, old_col] == 3 and self.item_grid[old_row + 1, old_col] == 0:
                    item.move("down")
                elif gm.grid[old_row, old_col] == 4 and self.item_grid[old_row, old_col - 1] == 0:
                    item.move("left")

                new_row, new_col = item.row, item.col
                if old_row != new_row or old_col != new_col:
                    self.item_grid[old_row, old_col] = 0
                    self.item_grid[new_row, new_col] = item.item

    def render(self):
        for item in self.items:
            item.render()

    def apply_zoom(self):
        for item in self.items:
            item.calc_position()


item_manager = ItemManager()