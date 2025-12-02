#################################################
# boat_management.py - handles boat placement, #
# hit/miss tracking, and sunk ship detection   #
#################################################

SHIP_LENGTHS = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}

class BoatManager:
    def __init__(self, rows, cols, ships):
        self.rows = rows
        self.cols = cols
        self.ships = ships

        # Board representation
        self.player_boards = {1: self._empty_board(), 2: self._empty_board()}
        self.player_hits = {1: self._empty_board(), 2: self._empty_board()}

        # Ship coordinate tracking
        self.player_ship_coords = {1: {}, 2: {}}

        # Sunk ships per player
        self.sunk_ships = {1: [], 2: []}

    def _empty_board(self):
        return [["~" for _ in range(self.cols)] for _ in range(self.rows)]

    # ------------------------------
    # Place ships for a player
    # ------------------------------
    def set_player_ships(self, player, board):
        """
        board: 2D list with "S" for ship cells, "~" for empty
        """
        self.player_boards[player] = board
        self.player_ship_coords[player] = {}
        self.sunk_ships[player] = []

        visited = [[False]*self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                if board[r][c] == "S" and not visited[r][c]:
                    ship_cells = self._flood_fill_ship(board, r, c, visited)
                    length = len(ship_cells)
                    ship_name = None
                    # Find ship name by length that is not already assigned
                    for name, l in SHIP_LENGTHS.items():
                        if l == length and name not in self.player_ship_coords[player]:
                            ship_name = name
                            break
                    if ship_name:
                        self.player_ship_coords[player][ship_name] = ship_cells

    def _flood_fill_ship(self, board, r, c, visited):
        """
        Collect all connected 'S' cells horizontally or vertically.
        """
        stack = [(r, c)]
        ship_cells = []
        while stack:
            row, col = stack.pop()
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if board[row][col] == "S" and not visited[row][col]:
                    visited[row][col] = True
                    ship_cells.append((row, col))
                    # Only horizontal/vertical neighbors
                    stack.extend([(row+1, col), (row-1, col), (row, col+1), (row, col-1)])
        return ship_cells

    # ------------------------------
    # Fire at a cell
    # ------------------------------
    def fire_at(self, attacker, defender, row, col):
        """
        Returns:
            "hit" if hit a ship
            "miss" if missed
            "repeat" if already shot
            "sunk:ship_name" if ship sunk
        """
        board = self.player_boards[defender]
        hits = self.player_hits[attacker]

        # Already shot here
        if hits[row][col] in ("X", "O"):
            return "repeat"

        if board[row][col] == "S":
            board[row][col] = "X"
            hits[row][col] = "X"
            sunk_ship = self._is_ship_sunk(defender, row, col)
            if sunk_ship:
                self.sunk_ships[defender].append(sunk_ship)
                return f"sunk:{sunk_ship}"
            return "hit"
        else:
            board[row][col] = "O"
            hits[row][col] = "O"
            return "miss"

    def _is_ship_sunk(self, player, row, col):
        """
        Checks if the ship containing (row, col) is fully hit.
        Returns the ship name if sunk, else None.
        """
        for ship_name, coords in self.player_ship_coords[player].items():
            if (row, col) in coords:
                if all(self.player_boards[player][r][c] == "X" for r, c in coords):
                    return ship_name
        return None

    # ------------------------------
    # Check if a player has won
    # ------------------------------
    def check_win(self):
        """
        Returns the winning player (1 or 2) if all ships of a player are sunk.
        Else returns None.
        """
        for player in [1, 2]:
            board = self.player_boards[player]
            if all(cell != "S" for row in board for cell in row):
                return 2 if player == 1 else 1
        return None
