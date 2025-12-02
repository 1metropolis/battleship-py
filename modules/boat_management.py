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
        self.player_boards = {1: self._empty_board(), 2: self._empty_board()}
        self.player_hits = {1: self._empty_board(), 2: self._empty_board()}
        self.sunk_ships = {1: [], 2: []}

    def _empty_board(self):
        return [["~" for _ in range(self.cols)] for _ in range(self.rows)]


    def set_player_ships(self, player, board):
        # board is a 2d list with ships already placed
        self.player_boards[player] = board


    def fire_at(self, attacker, defender, row, col):
        board = self.player_boards[defender]
        hits = self.player_hits[attacker]
        if hits[row][col] in ("X", "O"):
            return "repeat"
        if board[row][col] == "S":
            board[row][col] = "X"
            hits[row][col] = "X"
            if self._is_ship_sunk(board, row, col):
                self.sunk_ships[defender].append((row, col))
            return "hit"
        else:
            board[row][col] = "O"
            hits[row][col] = "O"
            return "miss"

    def _is_ship_sunk(self, board, row, col):
        # Simple sunk detection: check if all cells of the ship are hit
        # (You may want to improve this logic for real ship tracking)
        return False

    def check_win(self):
        for player in [1, 2]:
            board = self.player_boards[player]
            if all(cell != "S" for row in board for cell in row):
                return 2 if player == 1 else 1
        return None
