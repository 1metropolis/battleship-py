import pygame
from modules.draw import draw_grid
import curses
import firing

# Symbols for internal board
WATER = "~"
SHIP = "S"

def create_empty_board(rows, cols):
    return [[WATER for _ in range(cols)] for _ in range(rows)]

def placement_phase(screen, rows, cols, ships, player_name):
    """
    Let one player place their ships.
    ships: dict {"carrier":1, "battleship":1, ...}
    Returns: board 2D list with ships placed
    """
    board = create_empty_board(rows, cols)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    # Flatten ships into list with names for placement order
    ship_list = []
    for name, count in ships.items():
        for _ in range(count):
            ship_list.append(name)

    # Fixed lengths
    SHIP_LENGTHS = {"carrier":5,"battleship":4,"cruiser":3,"submarine":3,"destroyer":2}

    # Grid position helpers (similar to draw_grid)
    MARGIN = 50
    available_width = screen.get_width() - 2*MARGIN
    available_height = screen.get_height() - 2*MARGIN
    cell_width = available_width // cols
    cell_height = available_height // rows
    CELL_SIZE = min(cell_width, cell_height)
    grid_origin_x = (screen.get_width() - CELL_SIZE*cols)//2
    grid_origin_y = (screen.get_height() - CELL_SIZE*rows)//2 + 25

    ship_index = 0
    orientation = "H"  # default orientation, can toggle with R key

    bg = pygame.image.load("assets/battlemap.png")
    bg = pygame.transform.scale(bg, (850, 700))
    
    while ship_index < len(ship_list):
        screen.blit(bg, (0, 0))
        
        ship_name = ship_list[ship_index]
        ship_len = SHIP_LENGTHS[ship_name]

        mouse_pos = pygame.mouse.get_pos()
        row = (mouse_pos[1] - grid_origin_y) // CELL_SIZE
        col = (mouse_pos[0] - grid_origin_x) // CELL_SIZE

        # screen.fill((25,40,60))
        draw_grid(screen, rows, cols, screen.get_width(), screen.get_height())

        # Draw already placed ships
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == SHIP:
                    rect = pygame.Rect(grid_origin_x + c*CELL_SIZE, grid_origin_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (150,150,150), rect)

        # Draw preview of current ship
        if 0 <= row < rows and 0 <= col < cols:
            valid = True
            preview_cells = []
            for i in range(ship_len):
                r = row + i if orientation=="V" else row
                c = col + i if orientation=="H" else col
                if r >= rows or c >= cols or board[r][c]==SHIP:
                    valid = False
                    break
                preview_cells.append((r,c))
            color = (0,200,0) if valid else (200,0,0)
            for r,c in preview_cells:
                rect = pygame.Rect(grid_origin_x + c*CELL_SIZE, grid_origin_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)

        # Instruction text
        instruction = f"{player_name}: Place {ship_name} (R to rotate)"
        text_surface = font.render(instruction, True, (255,255,255))
        text_rect = text_surface.get_rect()
        # Place text above the grid, centered horizontally
        text_rect.centerx = screen.get_width() // 2
        text_rect.bottom = grid_origin_y - 35  # 10 pixels above the grid
        screen.blit(text_surface, text_rect)


        pygame.display.flip()
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    orientation = "V" if orientation=="H" else "H"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if valid:
                    for r,c in preview_cells:
                        board[r][c] = SHIP
                    ship_index += 1

    return board


def start_game(screen, rows, cols, ships):
    # Player 1 placement
    player1_board = placement_phase(screen, rows, cols, ships, "Player 1")
    # Player 2 placement
    player2_board = placement_phase(screen, rows, cols, ships, "Player 2")

    # Initialize history boards for firing
    player1 = {"name":"Player 1", "firing_history":[["~"]*cols for _ in range(rows)]}
    player2 = {"name":"Player 2", "firing_history":[["~"]*cols for _ in range(rows)]}
    defender1 = {"own_board":player1_board}
    defender2 = {"own_board":player2_board}

    # Start firing turns in terminal
    def firing_loop(stdscr):
        turn = 0
        while True:
            if turn%2==0:
                res = firing.firing_phase_for_turn(stdscr, player1, defender2)
            else:
                res = firing.firing_phase_for_turn(stdscr, player2, defender1)
            if res=="quit":
                break
            turn += 1

    curses.wrapper(firing_loop)
