import pygame
import sys
from modules.draw import (
    draw_instructions,
    compute_cell_size,
    compute_grid_origin,
    draw_grid,
    draw_placed_ships,
    draw_ship_preview,
    draw_cursor,
    show_splash
)

SHIP_LENGTHS = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}


def placement_phase(screen, rows, cols, ships, player_label, boat_manager, player_num):
    """
    Handles ship placement for a single player.
    Updates boat_manager with the final board.
    """
    show_splash(screen, f"{player_label} - Assemble your Navy!", duration=2000)
    
    pygame.font.init()
    clock = pygame.time.Clock()

    # Build ship queue
    ship_queue = [name for name, count in ships.items() for _ in range(count)]

    # Temporary player board
    board = [["~"] * cols for _ in range(rows)]

    # Cursor & orientation
    cursor_row, cursor_col = 0, 0
    orientation = "H"

    current_ship_index = 0
    total_ships = len(ship_queue)

    running = True
    while running:
        screen.fill((15, 30, 50))

        # Current ship info
        ship_name = ship_queue[current_ship_index]
        ship_len = SHIP_LENGTHS[ship_name]

        # Draw instructions
        instructions = (
            f"{player_label}, position your {ship_name.capitalize()}!\n"
            "Use Arrow Keys to navigate, \"R\" to turn, and Space to anchor in place!"
        )
        instructions_bottom = draw_instructions(screen, instructions, screen.get_width())

        # Grid geometry
        cell_size = compute_cell_size(rows, cols, screen.get_width(), screen.get_height(), instructions_bottom)
        origin_x, origin_y = compute_grid_origin(rows, cols, cell_size, screen.get_width(), screen.get_height(), instructions_bottom)

        # DRAWING
        draw_grid(screen, rows, cols, cell_size, origin_x, origin_y)
        draw_placed_ships(screen, board, cell_size, origin_x, origin_y)

        # Compute ship preview
        preview_cells = []
        valid = True
        for i in range(ship_len):
            r = cursor_row + (i if orientation == "V" else 0)
            c = cursor_col + (i if orientation == "H" else 0)
            if r >= rows or c >= cols or board[r][c] == "S":
                valid = False
                break
            preview_cells.append((r, c))

        draw_ship_preview(screen, preview_cells, cell_size, origin_x, origin_y, valid)
        draw_cursor(screen, cursor_row, cursor_col, cell_size, origin_x, origin_y)

        pygame.display.flip()
        clock.tick(60)

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    orientation = "V" if orientation == "H" else "H"
                elif event.key == pygame.K_UP:
                    cursor_row = max(0, cursor_row - 1)
                elif event.key == pygame.K_DOWN:
                    cursor_row = min(rows - 1, cursor_row + 1)
                elif event.key == pygame.K_LEFT:
                    cursor_col = max(0, cursor_col - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_col = min(cols - 1, cursor_col + 1)
                elif event.key == pygame.K_SPACE and valid:
                    # Commit ship placement
                    for r, c in preview_cells:
                        board[r][c] = "S"
                    current_ship_index += 1

                    if current_ship_index >= total_ships:
                        boat_manager.set_player_ships(player_num, board)
                        return

                    # Reset cursor for next ship
                    cursor_row, cursor_col = 0, 0
                    orientation = "H"
