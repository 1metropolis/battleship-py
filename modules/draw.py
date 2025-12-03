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

SHIP_COLORS = {
    "C": (200, 0, 0),      # Carrier - Red
    "B": (255, 165, 0),    # Battleship - Orange
    "R": (0, 200, 0),      # Cruiser - Green
    "U": (0, 100, 255),    # Submarine - Blueish
    "D": (160, 82, 45)     # Destroyer - Brown
}

def draw_placed_ships(screen, board, cell_size, origin_x, origin_y):
    """
    Draw all ships already placed on the board with unique warship designs.
    """
    plane_img = pygame.image.load("assets/plane.png").convert_alpha()

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == "~":
                continue

            rect = pygame.Rect(origin_x + c * cell_size,
                               origin_y + r * cell_size,
                               cell_size, cell_size)

            if cell == "C":  # Carrier
                orientation = "H"
                if (r > 0 and board[r-1][c] == "C") or \
                   (r < len(board)-1 and board[r+1][c] == "C"):
                    orientation = "V"
                draw_carrier_cell(screen, rect, plane_img, orientation)

            elif cell == "B":  # Battleship
                draw_battleship_cell(screen, rect)

            elif cell == "R":  # Cruiser
                draw_cruiser_cell(screen, rect)

            elif cell == "U":  # Submarine
                draw_submarine_cell(screen, rect)

            elif cell == "D":  # Destroyer
                draw_destroyer_cell(screen, rect)


def draw_battleship_cell(screen, rect):
    """Battleship: dark grey with diagonal deck plates"""
    base_color = (120, 120, 120)
    accent = (85, 85, 85)
    pygame.draw.rect(screen, base_color, rect)
    # Diagonal plate lines (like armored hull plating)
    pygame.draw.line(screen, accent, rect.topleft, rect.bottomright, 2)
    pygame.draw.line(screen, accent, rect.topright, rect.bottomleft, 2)


def draw_cruiser_cell(screen, rect):
    """Cruiser: medium grey with horizontal deck lines"""
    base_color = (135, 135, 135)
    line_color = (95, 95, 95)
    pygame.draw.rect(screen, base_color, rect)
    # Two horizontal deck lines
    y1 = rect.top + rect.height * 0.33
    y2 = rect.top + rect.height * 0.66
    pygame.draw.line(screen, line_color, (rect.left, y1), (rect.right, y1), 2)
    pygame.draw.line(screen, line_color, (rect.left, y2), (rect.right, y2), 2)


def draw_submarine_cell(screen, rect):
    """Submarine: blue-grey with rounded ends feel (center dot)"""
    hull_color = (100, 110, 125)
    pygame.draw.rect(screen, hull_color, rect)
    # Small porthole
    pygame.draw.circle(screen, (75, 85, 100), rect.center, int(rect.width * 0.15))


def draw_destroyer_cell(screen, rect):
    """Destroyer: light grey with single center stripe"""
    base_color = (145, 145, 145)
    stripe = (105, 105, 105)
    pygame.draw.rect(screen, base_color, rect)
    # Vertical center stripe
    cx = rect.centerx
    pygame.draw.line(screen, stripe, (cx, rect.top), (cx, rect.bottom), 3)


def draw_carrier_cell(screen, rect, plane_img, orientation):
    """Carrier: grey flight deck with runway and plane"""
    deck_color = (115, 115, 115)
    pygame.draw.rect(screen, deck_color, rect)
    draw_carrier_plane(screen, rect, plane_img, orientation)


def draw_carrier_plane(screen, rect, plane_img, orientation):
    """
    Draw planes onto the carrier boat
    """
    # Scale plane ~70% of tile
    plane_size = int(rect.width * 0.7)
    plane_scaled = pygame.transform.scale(plane_img, (plane_size, plane_size))

    # Rotate plane 45°
    plane_rotated = pygame.transform.rotate(plane_scaled, 45)

    # Get rotated rect for centering
    plane_rect = plane_rotated.get_rect()

    if orientation == "H":
        # Carrier is horizontal → runway goes left-to-right
        # Put plane slightly toward the top to leave room for runway line
        plane_rect.center = (
            rect.centerx,
            rect.centery + rect.height * 0.11  # small downward offset
        )
    else:
        # Carrier vertical → runway goes top-to-bottom
        # Put plane slightly left
        plane_rect.center = (
            rect.centerx - rect.width * 0.11,
            rect.centery
        )

    screen.blit(plane_rotated, plane_rect.topleft)

    # Draw runway
    runway_color = (180, 180, 180)

    if orientation == "H":
        # Horizontal carrier → horizontal runway line
        pygame.draw.line(
            screen, runway_color,
            (rect.left, rect.centery - rect.height * 0.22),
            (rect.right, rect.centery - rect.height * 0.22),
            2
        )
    else:
        # Vertical carrier → vertical runway line
        pygame.draw.line(
            screen, runway_color,
            (rect.centerx + rect.width * 0.22, rect.top),
            (rect.centerx + rect.width * 0.22, rect.bottom),
            2
        )


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
                 cell_size, origin_x, origin_y, speed=20):
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

def load_firing_assets():
    CROSSHAIR_PATH = "assets/crosshair.png"
    SMOKE_PATH = "assets/smoke.png"
    EXPLOSION_PATH = "assets/explosion.png"
    PLANE_PATH = "assets/plane.png"
    return {
        "crosshair": pygame.image.load(CROSSHAIR_PATH).convert_alpha(),
        "smoke": pygame.image.load(SMOKE_PATH).convert_alpha(),
        "explosion": pygame.image.load(EXPLOSION_PATH).convert_alpha(),
        "plane": pygame.image.load(PLANE_PATH).convert_alpha(),
    }

def draw_firing_screen(screen, rows, cols, cell_size, origin_x, origin_y, hits, crosshair_row, crosshair_col, instruction_text, assets):
    screen.fill((25, 40, 60))
    draw_grid(screen, rows, cols, cell_size, origin_x, origin_y)
    # Draw hits/misses
    for r in range(rows):
        for c in range(cols):
            x = origin_x + c * cell_size
            y = origin_y + r * cell_size
            if hits[r][c] == "X":
                img = pygame.transform.scale(assets["explosion"], (cell_size, cell_size))
                screen.blit(img, (x, y))
            elif hits[r][c] == "O":
                img = pygame.transform.scale(assets["smoke"], (cell_size, cell_size))
                screen.blit(img, (x, y))
    # Draw crosshair
    crosshair_scaled = pygame.transform.scale(assets["crosshair"], (cell_size, cell_size))
    screen.blit(crosshair_scaled, (origin_x + crosshair_col * cell_size, origin_y + crosshair_row * cell_size))
    # Draw instructions
    font = pygame.font.SysFont(None, 32)
    instr_text = font.render(instruction_text, True, (255,255,255))
    screen.blit(instr_text, (20, 20))
    pygame.display.flip()

def show_firing_splash(screen, text, duration=1000):
    font = pygame.font.SysFont(None, 72)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    text_surface = font.render(text, True, (255, 255, 0))
    rect = text_surface.get_rect(center=screen.get_rect().center)
    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((25, 40, 60))
        screen.blit(text_surface, rect)
        pygame.display.flip()
        clock.tick(60)

def animate_firing_shot(screen, boat_manager, attacker, defender, target_row, target_col,
                        cell_size, origin_x, origin_y, assets, speed=20):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    plane_width, plane_height = cell_size * 2, cell_size * 2
    plane_scaled = pygame.transform.scale(assets["plane"], (plane_width, plane_height))
    target_x = origin_x + target_col * cell_size
    target_y = origin_y + target_row * cell_size
    plane_x = -plane_width
    plane_y = target_y - (plane_height - cell_size) // 2
    plane_center_target = target_x + cell_size // 2
    effect_spawned = False
    message_start_time = None
    message_duration = 1000
    hits = boat_manager.player_hits[attacker]
    result = None
    while plane_x < screen.get_width():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((25, 40, 60))
        draw_grid(screen, boat_manager.rows, boat_manager.cols, cell_size, origin_x, origin_y)
        # Draw hits/misses
        for r in range(boat_manager.rows):
            for c in range(boat_manager.cols):
                x = origin_x + c * cell_size
                y = origin_y + r * cell_size
                if hits[r][c] == "X":
                    img = pygame.transform.scale(assets["explosion"], (cell_size, cell_size))
                    screen.blit(img, (x, y))
                elif hits[r][c] == "O":
                    img = pygame.transform.scale(assets["smoke"], (cell_size, cell_size))
                    screen.blit(img, (x, y))
        plane_center_x = plane_x + plane_width // 2
        if not effect_spawned and plane_center_x >= plane_center_target:
            result = boat_manager.fire_at(attacker, defender, target_row, target_col)
            effect_spawned = True
            message_start_time = pygame.time.get_ticks()
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
        if effect_spawned:
            effect_img = assets["explosion"] if result == "hit" or (result and result.startswith("sunk:")) else assets["smoke"]
            effect_scaled = pygame.transform.scale(effect_img, (cell_size, cell_size))
            screen.blit(effect_scaled, (target_x, target_y))
        screen.blit(plane_scaled, (plane_x, plane_y))
        pygame.display.flip()
        plane_x += speed
        clock.tick(60)
    pygame.time.wait(300)
    return result
