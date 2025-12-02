# firing.py
import curses

# Symbols used across the project
WATER = "~"
SHIP = "S"
HIT = "X"
MISS = "O"

def draw_firing_screen(stdscr, history_board, cursor_row, cursor_col, attacker_name, msg=""):
    """
    Draw the firing screen as a coordinate plane using the given history_board.

    history_board: 2D list of chars with same size as your game board:
        '~' = no shot yet, 'X' = hit, 'O' = miss.
    cursor_row, cursor_col: current aiming position (y, x).
    """
    rows = len(history_board)
    cols = len(history_board[0])

    # x-axis labels: A, B, C, ... up to number of columns
    col_labels = [chr(ord("A") + i) for i in range(cols)]

    stdscr.clear()
    stdscr.addstr(0, 0, f"{attacker_name}'s Firing Phase (↑↓←→ move, Enter fire, q quit)")
    if msg:
        stdscr.addstr(1, 0, msg)

    # x-axis (letters)
    header = "   " + " ".join(col_labels)
    stdscr.addstr(3, 0, header)

    # y-axis (numbers) down the side
    for r in range(rows):
        line = f"{r:2} "
        for c in range(cols):
            line += history_board[r][c] + " "
        stdscr.addstr(4 + r, 0, line)

    # Highlight current cursor position
    y = 4 + cursor_row
    x = 3 + cursor_col * 2
    stdscr.move(y, x)
    stdscr.refresh()

def choose_target_with_arrows(stdscr, history_board, attacker_name):
    """
    Use arrow keys to pick a target on the existing board.

    history_board: 2D list you already made for this player.
    Returns (row, col) or None if 'q' is pressed.
    """
    rows = len(history_board)
    cols = len(history_board[0])

    curses.curs_set(1)
    stdscr.keypad(True)

    row, col = 0, 0
    msg = ""

    while True:
        draw_firing_screen(stdscr, history_board, row, col, attacker_name, msg)
        key = stdscr.getch()

        if key == ord('q'):
            return None
        elif key == curses.KEY_UP:
            row = max(0, row - 1)
        elif key == curses.KEY_DOWN:
            row = min(rows - 1, row + 1)
        elif key == curses.KEY_LEFT:
            col = max(0, col - 1)
        elif key == curses.KEY_RIGHT:
            col = min(cols - 1, col + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            return row, col

def apply_shot_and_update_history(enemy_board, history_board, row, col):
    """
    Apply a shot at (row, col) and update history.

    enemy_board: 2D list with the real ships for the defender:
        'S' = ship, '~' = water, 'X' = hit ship, 'O' = fired-on water.
    history_board: 2D list for the attacker:
        '~' = unknown, 'X' = hit, 'O' = miss.

    Returns "repeat" if already fired here, otherwise "hit" or "miss".
    """
    # Already fired here? Check the attacker's history.
    if history_board[row][col] in (HIT, MISS):
        return "repeat"

    cell = enemy_board[row][col]

    if cell == SHIP:
        enemy_board[row][col] = HIT
        history_board[row][col] = HIT
        return "hit"
    else:
        if cell == WATER:
            enemy_board[row][col] = MISS
        history_board[row][col] = MISS
        return "miss"

def firing_phase_for_turn(stdscr, attacker, defender):
    """
    Run one firing phase for 'attacker' against 'defender'.

    attacker: dict like {"name": str, "firing_history": 2D list}
    defender: dict like {"own_board": 2D list}

    Returns:
      "hit", "miss", "repeat" or "quit".
    """
    history_board = attacker["firing_history"]
    enemy_board = defender["own_board"]

    while True:
        target = choose_target_with_arrows(stdscr, history_board, attacker["name"])
        if target is None:
            return "quit"

        row, col = target
        result = apply_shot_and_update_history(enemy_board, history_board, row, col)

        # Build feedback message with correct coordinates: x = letter, y = number
        cols = len(history_board[0])
        col_labels = [chr(ord("A") + i) for i in range(cols)]
        coord_str = f"{col_labels[col]}{row}"

        if result == "repeat":
            msg = "The area you chose has already been shot. Select a new location."
        elif result == "hit":
            msg = f"Hit at {coord_str}! (stored as X)"
        else:  # "miss"
            msg = f"Miss at {coord_str}. (stored as O)"

        draw_firing_screen(stdscr, history_board, row, col, attacker["name"], msg)
        stdscr.getch()

        if result in ("hit", "miss"):
            return result
