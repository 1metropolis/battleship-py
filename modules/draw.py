import pygame
from string import ascii_uppercase

WHITE = (255, 255, 255)
LABEL_GAP = 25
MARGIN = 40 # Minimum padding on all sides

# use to choose correct square size based on the chosen grid size
def compute_cell_size(rows, cols, width, height, instructions_height=60):
    """
    Returns the largest square cell size that fits the grid inside the screen.
    """
    available_width = width - 2 * MARGIN
    available_height = height - (instructions_height + LABEL_GAP + MARGIN)
    cell_w = available_width // cols
    cell_h = available_height // rows
    return min(cell_w, cell_h)

# find top left corner of the grid
def compute_grid_origin(rows, cols, cell_size, width, height, instructions_height=60):
    """
    Returns the top-left corner (x, y) of the grid to center it on screen.
    """
    grid_width = cell_size * cols
    x = (width - grid_width) // 2
    y = instructions_height + LABEL_GAP
    return x, y

# draw instructions at the top of the screen
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

# draw battleship grid
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


# draw ships placed on board using board variable
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

# draw highlighted ship for placement
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

# highlight selected square
def draw_cursor(screen, row, col, cell_size, origin_x, origin_y):
    """
    Draw a yellow outline at the current cursor position.
    """
    rect = pygame.Rect(origin_x + col * cell_size,
                       origin_y + row * cell_size,
                       cell_size, cell_size)
    pygame.draw.rect(screen, (255, 255, 0), rect, 3)

# show a splash message on screen
def show_splash(screen, text, duration=1000, font_size=72, bg_color=(25, 40, 60), text_color=(255, 255, 0)):
    """
    Display a full-screen message (splash) for a brief duration.
    
    Args:
        screen: pygame display surface
        text: message to display
        duration: time in milliseconds
        font_size: size of the font
        bg_color: background color
        text_color: color of the text
    """
    font = pygame.font.SysFont(None, font_size)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    text_surface = font.render(text, True, text_color)
    rect = text_surface.get_rect(center=screen.get_rect().center)

    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill(bg_color)
        screen.blit(text_surface, rect)
        pygame.display.flip()
        clock.tick(60)

# plane bombs the battleship
def animate_shot(screen, boat_manager, attacker, defender, target_row, target_col,
                 cell_size, origin_x, origin_y, speed=10):
    """
    Animate a plane flying across the target and spawn hit/miss effect.
    Only calls boat_manager.fire_at when the plane reaches the target.
    """
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    # Load assets
    plane_img = pygame.image.load("assets/plane.png").convert_alpha()
    explosion_img = pygame.image.load("assets/explosion.png").convert_alpha()
    smoke_img = pygame.image.load("assets/smoke.png").convert_alpha()

    # Scale plane to double size
    plane_width, plane_height = cell_size * 2, cell_size * 2
    plane_scaled = pygame.transform.scale(plane_img, (plane_width, plane_height))

    # Target position
    target_x = origin_x + target_col * cell_size
    target_y = origin_y + target_row * cell_size

    # Plane vertical centering
    plane_x = -plane_width
    plane_y = target_y - (plane_height - cell_size) // 2

    # Plane center target
    plane_center_target = target_x + cell_size // 2
    effect_spawned = False
    message_start_time = None
    message_duration = 1000

    # Keep track of displayed effects
    hits = boat_manager.player_hits[attacker]

    result = None

    while plane_x < screen.get_width():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((25, 40, 60))
        from modules.draw import draw_grid
        draw_grid(screen, boat_manager.rows, boat_manager.cols, cell_size, origin_x, origin_y)

        # Draw existing hits/misses
        for r in range(boat_manager.rows):
            for c in range(boat_manager.cols):
                x = origin_x + c * cell_size
                y = origin_y + r * cell_size
                if hits[r][c] == "X":
                    screen.blit(pygame.transform.scale(explosion_img, (cell_size, cell_size)), (x, y))
                elif hits[r][c] == "O":
                    screen.blit(pygame.transform.scale(smoke_img, (cell_size, cell_size)), (x, y))

        # Check if plane center reaches target center and fire
        plane_center_x = plane_x + plane_width // 2
        if not effect_spawned and plane_center_x >= plane_center_target:
            # Call boat_manager.fire_at to determine hit/miss/sunk
            result = boat_manager.fire_at(attacker, defender, target_row, target_col)
            effect_spawned = True
            message_start_time = pygame.time.get_ticks()

        # Draw floating message
        if message_start_time and result:
            elapsed = pygame.time.get_ticks() - message_start_time
            if elapsed < message_duration:
                if result.startswith("sunk:"):
                    ship_name = result.split(":")[1]
                    msg = f"Sunk their {ship_name.capitalize()}!"
                else:
                    msg = "Hit!" if result == "hit" else "Miss!"
                text_surf = font.render(msg, True, (255, 215, 0))
                text_rect = text_surf.get_rect(center=(target_x + cell_size // 2, target_y - 30))
                screen.blit(text_surf, text_rect)

        # Draw the bomb/effect only after plane reaches center
        if effect_spawned:
            effect_img = explosion_img if result == "hit" or (result and result.startswith("sunk:")) else smoke_img
            effect_scaled = pygame.transform.scale(effect_img, (cell_size, cell_size))
            screen.blit(effect_scaled, (target_x, target_y))
            
        # Draw plane
        screen.blit(plane_scaled, (plane_x, plane_y))

        pygame.display.flip()
        plane_x += speed
        clock.tick(60)

    pygame.time.wait(300)
    return result

