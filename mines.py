from constants import consts as c
from grid import grid_manager as gm
from items import item_manager as im
from world import world as w


class Mine:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction

        if direction == 1:
            self.target_row = row - 1
            self.target_col = col
        elif direction == 2:
            self.target_row = row
            self.target_col = col + 1
        elif direction == 3:
            self.target_row = row + 1
            self.target_col = col
        elif direction == 4:
            self.target_row = row
            self.target_col = col - 1

        self.mining = None
        self.progress = 0

    def update(self):
        if self.mining is None:
            if w.world[self.row][self.col] > 0:
                self.mining = w.world[self.row][self.col]
                self.progress = 0
        else:
            if self.progress < c.mine_time:
                self.progress += c.dt
            elif im.item_grid[self.target_row][self.target_col] == 0 and gm.item_can_be_placed((self.target_row, self.target_col)):
                if self.mining == 1:
                    im.add_item(7, self.target_row, self.target_col)
                if self.mining == 2:
                    im.add_item(9, self.target_row, self.target_col)
                self.mining = None
                    

class MineManager:
    def __init__(self):
        self.mines = []

    def add_mine(self, row, col, direction):
        self.mines.append(Mine(row, col, direction))

    def remove_mine(self, row, col):
        for mine in self.mines:
            if mine.row == row and mine.col == col:
                self.mines.remove(mine)

    def update(self):
        for mine in self.mines:
            mine.update()


mine_manager = MineManager()