#################################################
# FILE_HANDLING.py reads the settings.json and  #
# validates that the settings are valid.        #
#################################################

import json
import os

SHIP_LENGTHS = { # length
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}

# load settings from the json
def load_settings(path="settings.json"):
    
    # check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found.")

    # read json file, load json data
    with open(path, "r") as f:
        data = json.load(f)
    
    # if board or ships are not in json
    if "board" not in data or "ships" not in data:
        raise ValueError("settings.json must contain 'board' and 'ships' keys.")

    # set rows, cols, ships
    rows = data["board"].get("rows", 10)
    cols = data["board"].get("cols", 10)
    ships = data["ships"]

    validate_settings(rows, cols, ships) # make sure these are proper
    return rows, cols, ships


# make sure that you can place ships with the chosen board size and shipcounts
def validate_settings(rows, cols, ship_counts):
    # makesure ships in settings.json exist
    for name in ship_counts:
        if name not in SHIP_LENGTHS:
            raise ValueError(f"Unknown ship type in settings.json: {name}")

    # Check ships area vs board area
    area_required = sum(SHIP_LENGTHS[name] * count for name, count in ship_counts.items())
    board_size = rows * cols

    if area_required > board_size:
        raise ValueError(
            f"Impossible: Ships require {area_required} cells but board "
            f"has only {board_size} cells."
        )

    # Check ship mininmum length and board length
    max_dim = max(rows, cols)
    for name, length in SHIP_LENGTHS.items():
        if ship_counts.get(name, 0) > 0 and length > max_dim:
            raise ValueError(
                f"Impossible: Ship '{name}' of length {length} cannot fit on a "
                f"{rows}x{cols} board in any orientation."
            )

    # brute force orientation checker, to check whether a set of ships can be placed on a given grid without overlap
    lengths = []
    for name, count in ship_counts.items():
        lengths.extend([SHIP_LENGTHS[name]] * count)

    if not can_place_all_ships(rows, cols, lengths):
        raise ValueError("Impossible board: Ships cannot be arranged without overlap.")

    return True



# Backtracking algorithm to bruteforce ship placement

def can_place_all_ships(rows, cols, ship_lengths):
    # Start with an empty grid
    grid = [[0] * cols for _ in range(rows)]

    # Place largest ships first (helps pruning)
    ship_lengths = sorted(ship_lengths, reverse=True)

    return place_ship(grid, ship_lengths, 0)


def place_ship(grid, ships, index):
    if index == len(ships):
        return True  # all ships placed successfully

    ship_len = ships[index]
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):

            # Try horizontal placement
            if c + ship_len <= cols and all(grid[r][cc] == 0 for cc in range(c, c + ship_len)):
                for cc in range(c, c + ship_len):
                    grid[r][cc] = 1

                if place_ship(grid, ships, index + 1):
                    return True

                for cc in range(c, c + ship_len):
                    grid[r][cc] = 0

            # Try vertical placement
            if r + ship_len <= rows and all(grid[rr][c] == 0 for rr in range(r, r + ship_len)):
                for rr in range(r, r + ship_len):
                    grid[rr][c] = 1

                if place_ship(grid, ships, index + 1):
                    return True

                for rr in range(r, r + ship_len):
                    grid[rr][c] = 0

    return False