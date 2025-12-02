import pygame
from string import ascii_uppercase

WHITE = (255, 255, 255)
LABEL_GAP = 24
MARGIN = 50

# draw grid
def draw_grid(screen, rows, cols, width, height):
    """
    Draws a battleship grid centered in the given width/height area.
    Includes row (1,2,3...) and column (A,B,C...) labels.
    """
    # Compute cell size dynamically
    available_width = width - 2*MARGIN
    available_height = height - 2*MARGIN
    cell_width = available_width // cols
    cell_height = available_height // rows
    CELL_SIZE = min(cell_width, cell_height)

    grid_origin_x = (width - CELL_SIZE*cols) // 2
    grid_origin_y = (height - CELL_SIZE*rows) // 2 + 25

    font = pygame.font.SysFont(None, 20)

    # Draw cells
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(
                grid_origin_x + col*CELL_SIZE,
                grid_origin_y + row*CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, WHITE, rect, 1)

    # Draw column labels (A, B, C...)
    for col in range(cols):
        label = font.render(ascii_uppercase[col % 26], True, WHITE)
        x = grid_origin_x + col*CELL_SIZE + CELL_SIZE//2 - label.get_width()//2
        y = grid_origin_y - LABEL_GAP
        screen.blit(label, (x, y))

    # Draw row labels (1, 2, 3...)
    for row in range(rows):
        label = font.render(str(row+1), True, WHITE)
        x = grid_origin_x - LABEL_GAP
        y = grid_origin_y + row*CELL_SIZE + CELL_SIZE//2 - label.get_height()//2
        screen.blit(label, (x, y))
