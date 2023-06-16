from structures.arm import Arm
from structures.conveyor import Conveyor, ConveyorUnderground
from structures.factory import Factory
from structures.furnace import Furnace
from structures.mine import Mine
from structures.splitter import Splitter

from constants import consts as c
from id_mapping import id_map
from items import item_manager as im
from ui.recipe_selection import select_recipe


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
                c.conveyor_placed.play()
            elif structure_type == id_map["conveyor_underground"]:
                new_structure = ConveyorUnderground(row, col, direction)
                c.conveyor_placed.play()
            elif structure_type == id_map["splitter"]:
                new_structure = Splitter(row, col, direction)
                c.conveyor_placed.play()
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

            if im.grid[row][col] != 0 and not isinstance(new_structure, Conveyor):
                im.remove(row, col)

            self.grid[row][col] = new_structure
            if isinstance(new_structure, ConveyorUnderground):
                self.grid[new_structure.target_row][new_structure.target_col] = new_structure

            self.structures.append(new_structure)

        elif isinstance(self.grid[row][col], Factory):
            factory = self.grid[row][col]
            selected_recipe = select_recipe()
            factory.set_recipe(selected_recipe)

    def remove(self, row, col):
        if self.grid[row][col] != 0:
            structure = self.grid[row][col]

            if isinstance(structure, Arm):
                structure.safely_drop_item(im)

            if type(structure) not in [Conveyor, ConveyorUnderground, Splitter]:
                c.structure_destroy.play()
            else:
                c.conveyor_pick_up.play()

            if isinstance(structure, ConveyorUnderground):
                self.grid[structure.source_row][structure.source_col] = 0
                self.grid[structure.target_row][structure.target_col] = 0

            self.grid[row][col] = 0
            self.structures.remove(structure)

    def rotate(self, row, col, direction = 1):
        if self.grid[row][col] != 0:
            structure = self.grid[row][col]
            if type(structure) == Arm:
                structure.safely_drop_item(im)
                structure.rotate(direction)
                c.rotate.play()

            elif type(structure) != ConveyorUnderground:
                structure.rotate(direction)
                c.rotate.play()

    def item_can_be_placed(self, row, col):
        return self.grid[row][col] == 0 or type(self.grid[row][col]) in [Conveyor, ConveyorUnderground, Splitter]
    
    def apply_zoom(self):
        for structure in self.structures:
            structure.calc_position()


structure_manager = StructureManager()