import pygame
from modules.draw import draw_grid, compute_cell_size, compute_grid_origin, show_splash, animate_shot

CROSSHAIR_PATH = "assets/crosshair.png"
SMOKE_PATH = "assets/smoke.png"
EXPLOSION_PATH = "assets/explosion.png"

def firing_phase(screen, boat_manager):
    pygame.font.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    rows, cols = boat_manager.rows, boat_manager.cols

    # load assets
    crosshair_img = pygame.image.load(CROSSHAIR_PATH).convert_alpha()
    smoke_img = pygame.image.load(SMOKE_PATH).convert_alpha()
    explosion_img = pygame.image.load(EXPLOSION_PATH).convert_alpha()

    current_player = 1
    other_player = 2

    show_splash(screen, f"Player {current_player}'s turn!")
    
    # Crosshair initial position
    cursor_row, cursor_col = 0, 0

    running = True
    winner = None

    while running:
        screen.fill((25, 40, 60))

        # Compute grid
        cell_size = compute_cell_size(rows, cols, screen.get_width(), screen.get_height())
        origin_x, origin_y = compute_grid_origin(rows, cols, cell_size, screen.get_width(), screen.get_height())

        # Draw the grid
        draw_grid(screen, rows, cols, cell_size, origin_x, origin_y)

        # Draw hits and misses
        hits = boat_manager.player_hits[current_player]
        for r in range(rows):
            for c in range(cols):
                x = origin_x + c * cell_size
                y = origin_y + r * cell_size
                if hits[r][c] == "X":
                    screen.blit(pygame.transform.scale(explosion_img, (cell_size, cell_size)), (x, y))
                elif hits[r][c] == "O":
                    screen.blit(pygame.transform.scale(smoke_img, (cell_size, cell_size)), (x, y))

        # Draw crosshair
        crosshair_scaled = pygame.transform.scale(crosshair_img, (cell_size, cell_size))
        screen.blit(crosshair_scaled, (origin_x + cursor_col*cell_size, origin_y + cursor_row*cell_size))

        # Draw instructions
        instr_text = font.render(f"Player {current_player}! You must use your Arrow Keys to lock your target, hit Space to fire!", True, (255,255,255))
        screen.blit(instr_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                # Move crosshair
                if event.key == pygame.K_UP:
                    cursor_row = max(0, cursor_row - 1)
                elif event.key == pygame.K_DOWN:
                    cursor_row = min(rows - 1, cursor_row + 1)
                elif event.key == pygame.K_LEFT:
                    cursor_col = max(0, cursor_col - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_col = min(cols - 1, cursor_col + 1)
                elif event.key == pygame.K_SPACE:
                    # Fire at selected cell
                    result = boat_manager.fire_at(current_player, other_player, cursor_row, cursor_col)
                    if result == "hit" or result.startswith("sunk:"):
                        
                        animate_shot(screen, boat_manager, current_player, cursor_row, cursor_col, cell_size, origin_x, origin_y, "hit")
                        
                        # Check for win
                        winner = boat_manager.check_win()
                        if winner:
                            running = False
                        # Player gets another turn on hit
                        
                    elif result == "miss":
                        
                        animate_shot(screen, boat_manager, current_player, cursor_row, cursor_col, cell_size, origin_x, origin_y, result)
                        
                        current_player, other_player = other_player, current_player
                        pygame.time.wait(1000)
                        show_splash(screen, f"Player {current_player}'s Turn")
                    # Repeat → do nothing

    return f"Player {winner}" if winner else None