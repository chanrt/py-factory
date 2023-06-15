id_map = {}

objects = []

# structures
objects.extend([
    "conveyor", "conveyor_underground", "splitter", "arm", "mine", "furnace", "factory",
])

# ores
objects.extend([
    "coal", "iron_ore", "copper_ore"
])

# resources
objects.extend([
    "iron", "copper"
])

# first derivative products
objects.extend([
    "gear", "pipe", "copper_wire", "circuit"
])

for object_ in objects:
    id_map[object_] = len(id_map)


reverse_id_map = {v: k for k, v in id_map.items()}