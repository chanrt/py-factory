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
        c.screen.blit(i.images[self.item], (self.x - c.player_x - c.cell_length // 2, self.y - c.player_y - c.cell_length // 2))


class ItemManager:
    def __init__(self):
        self.item_grid = []
        for _ in range(c.num_cells):
            new_row = [0 for _ in range(c.num_cells)]
            self.item_grid.append(new_row)
        self.locations = []

    def add_item(self, item, row, col):
        self.item_grid[row][col] = Item(item, row, col)
        self.locations.append((row, col))

    def remove_item(self, row, col):
        if (row, col) in self.locations:
            self.locations.remove((row, col))
            self.item_grid[row][col] = 0

    def fetch_item(self, row, col):
        item = self.item_grid[row][col]
        item.caught = True

        self.item_grid[row][col] = 0
        self.locations.remove((row, col))
        return item
            
    def drop_item(self, item, end_x, end_y):
        item.caught = False
        item.row = int(end_y / c.cell_length)
        item.col = int(end_x / c.cell_length)
        item.calc_position()
        
        self.item_grid[item.row][item.col] = item
        self.locations.append((item.row, item.col))

    def update(self):
        for loc in self.locations:
            old_row, old_col = loc
            item = self.item_grid[old_row][old_col]

            if not item.caught and 0 < gm.grid[old_row, old_col] < 5:
                if gm.grid[old_row, old_col] == 1 and self.item_grid[old_row - 1][old_col] == 0:
                    item.move("up")
                elif gm.grid[old_row, old_col] == 2 and self.item_grid[old_row][old_col + 1] == 0:
                    item.move("right")
                elif gm.grid[old_row, old_col] == 3 and self.item_grid[old_row + 1][old_col] == 0:
                    item.move("down")
                elif gm.grid[old_row, old_col] == 4 and self.item_grid[old_row][old_col - 1] == 0:
                    item.move("left")

                new_row, new_col = item.row, item.col
                if old_row != new_row or old_col != new_col:
                    self.item_grid[old_row][old_col] = 0
                    self.item_grid[new_row][new_col] = item
                    self.locations.remove((old_row, old_col))
                    self.locations.append((new_row, new_col))

    def render(self):
        for loc in self.locations:
            row, col = loc
            item = self.item_grid[row][col]
            item.render()

    def apply_zoom(self):
        for loc in self.locations:
            row, col = loc
            item = self.item_grid[row][col]
            item.calc_position()


item_manager = ItemManager()