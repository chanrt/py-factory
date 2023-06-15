from id_mapping import id_map


recipes = []
recipes.append({
    "name": "Gear",
    "inputs": {id_map["iron"]: 1},
    "output": id_map["gear"],
    "time": 1
})

recipes.append({
    "name": "Pipe",
    "inputs": {id_map["iron"]: 1},
    "output": id_map["pipe"],
    "time": 1
})

recipes.append({
    "name": "Wire",
    "inputs": {id_map["copper"]: 1},
    "output": id_map["copper_wire"],
    "time": 1
})

recipes.append({
    "name": "Circuit",
    "inputs": {id_map["copper_wire"]: 2, id_map["iron"]: 1},
    "output": id_map["circuit"],
    "time": 2
})