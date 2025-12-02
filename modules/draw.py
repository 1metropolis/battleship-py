import pygame
from string import ascii_uppercase

WHITE = (255, 255, 255)
LABEL_GAP = 25
MARGIN = 40 # Minimum padding on all sides


def compute_cell_size(rows, cols, width, height, instructions_height=60):
    """
    Returns the largest square cell size that fits the grid inside the screen.
    """
    available_width = width - 2 * MARGIN
    available_height = height - (instructions_height + LABEL_GAP + MARGIN)
    cell_w = available_width // cols
    cell_h = available_height // rows
    return min(cell_w, cell_h)


def compute_grid_origin(rows, cols, cell_size, width, height, instructions_height=60):
    """
    Returns the top-left corner (x, y) of the grid to center it on screen.
    """
    grid_width = cell_size * cols
    x = (width - grid_width) // 2
    y = instructions_height + LABEL_GAP
    return x, y


def draw_instructions(screen, text, width, top_padding = 15):
    """
    Draws multi-line instructions centered horizontally.
    Returns the bottom y-coordinate after drawing the text.
    """
    font = pygame.font.SysFont(None, 32)
    y = top_padding
    for line in text.split("\n"):
        surf = font.render(line, True, WHITE)
        x = (width - surf.get_width()) // 2
        screen.blit(surf, (x, y))
        y += surf.get_height() + 2
    return y + 15


def draw_grid(screen, rows, cols, cell_size, origin_x, origin_y):
    """
    Draws labeled grid and grid lines.
    """
    font = pygame.font.SysFont(None, 22)

    # Column labels
    for c in range(cols):
        label = ascii_uppercase[c % 26]
        surf = font.render(label, True, WHITE)
        cx = origin_x + c * cell_size + cell_size // 2 - surf.get_width() // 2
        cy = origin_y - LABEL_GAP
        screen.blit(surf, (cx, cy))

    # Row labels
    for r in range(rows):
        label = str(r + 1)
        surf = font.render(label, True, WHITE)
        cx = origin_x - LABEL_GAP
        cy = origin_y + r * cell_size + cell_size // 2 - surf.get_height() // 2
        screen.blit(surf, (cx, cy))

    # Grid lines
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(origin_x + c * cell_size,
                               origin_y + r * cell_size,
                               cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 1)


def draw_placed_ships(screen, board, cell_size, origin_x, origin_y):
    """
    Draw all ships already placed on the board.
    """
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == "S":
                rect = pygame.Rect(origin_x + c * cell_size,
                                   origin_y + r * cell_size,
                                   cell_size, cell_size)
                pygame.draw.rect(screen, (150, 150, 150), rect)


def draw_ship_preview(screen, preview_cells, cell_size, origin_x, origin_y, valid):
    """
    Draw the preview of the ship being placed.
    Green if valid, red if invalid.
    """
    color = (0, 220, 0) if valid else (220, 0, 0)
    for r, c in preview_cells:
        rect = pygame.Rect(origin_x + c * cell_size,
                           origin_y + r * cell_size,
                           cell_size, cell_size)
        pygame.draw.rect(screen, color, rect)


def draw_cursor(screen, row, col, cell_size, origin_x, origin_y):
    """
    Draw a yellow outline at the current cursor position.
    """
    rect = pygame.Rect(origin_x + col * cell_size,
                       origin_y + row * cell_size,
                       cell_size, cell_size)
    pygame.draw.rect(screen, (255, 255, 0), rect, 3)
