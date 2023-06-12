from id_mapping import id_map


recipes = []
recipes.append({
    "name": "gear",
    "inputs": {id_map["iron"]: 1},
    "output": id_map["gear"],
    "time": 1
})

recipes.append({
    "name": "copper wire",
    "inputs": {id_map["copper"]: 1},
    "output": id_map["copper_wire"],
    "time": 1
})

recipes.append({
    "name": "circuit",
    "inputs": {id_map["copper_wire"]: 2, id_map["iron"]: 1},
    "output": id_map["circuit"],
    "time": 1
})