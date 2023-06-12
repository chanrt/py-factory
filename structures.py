from arm import Arm
from conveyor import Conveyor, ConveyorUnderground
from factory import Factory
from furnace import Furnace
from mine import Mine

from constants import consts as c
from id_mapping import id_map
from items import item_manager as im


class StructureManager:
    def __init__(self):
        self.grid = []
        for _ in range(c.num_cells):
            new_row = [0 for _ in range(c.num_cells)]
            self.grid.append(new_row)
        self.structures = []

    def update(self):
        for structure in self.structures:
            structure.update(self, im)

    def render(self):
        for structure in self.structures:
            structure.render()

    def add(self, row, col, structure_type, direction):
        if self.grid[row][col] == 0:
            if structure_type == id_map["conveyor"]:
                new_structure = Conveyor(row, col, direction)
            elif structure_type == id_map["conveyor_underground"]:
                new_structure = ConveyorUnderground(row, col, direction)
            elif structure_type == id_map["arm"]:
                new_structure = Arm(row, col, direction)
                c.arm_placed.play()
            elif structure_type == id_map["mine"]:
                new_structure = Mine(row, col, direction)
                c.mine_placed.play()
            elif structure_type == id_map["furnace"]:
                new_structure = Furnace(row, col, direction)
                c.furnace_placed.play()
            elif structure_type == id_map["factory"]:
                new_structure = Factory(row, col, direction)
                c.factory_placed.play()

            if im.grid[row][col] != 0:
                im.remove(row, col)

            self.grid[row][col] = new_structure
            if isinstance(new_structure, ConveyorUnderground):
                self.grid[new_structure.target_row][new_structure.target_col] = new_structure

            self.structures.append(new_structure)

    def remove(self, row, col):
        if self.grid[row][col] != 0:
            structure_to_be_removed = self.grid[row][col]

            if isinstance(structure_to_be_removed, Arm):
                structure_to_be_removed.safely_drop_item(im)

            if not isinstance(structure_to_be_removed, Conveyor) and not isinstance(structure_to_be_removed, ConveyorUnderground):
                c.structure_destroy.play()

            if isinstance(structure_to_be_removed, ConveyorUnderground):
                self.grid[structure_to_be_removed.target_row][structure_to_be_removed.target_col] = 0

            self.grid[row][col] = 0
            self.structures.remove(structure_to_be_removed)

    def rotate(self, row, col, direction = 1):
        if self.grid[row][col] != 0:
            if not isinstance(self.grid[row][col], ConveyorUnderground):
                self.grid[row][col].rotate(direction)
                c.rotate.play()

    def item_can_be_placed(self, row, col):
        return self.grid[row][col] == 0 or isinstance(self.grid[row][col], Conveyor) or isinstance(self.grid[row][col], ConveyorUnderground)
    
    def apply_zoom(self):
        for structure in self.structures:
            structure.calc_position()


structure_manager = StructureManager()