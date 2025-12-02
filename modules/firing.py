import pygame
from modules import draw

def firing_phase(screen, boat_manager):
    pygame.font.init()
    clock = pygame.time.Clock()
    rows, cols = boat_manager.rows, boat_manager.cols

    # load all image assets needed for firing phase
    assets = draw.load_firing_assets()
    current_player = 1
    other_player = 2
    
    # show splash screen for current player at start of turn
    draw.show_firing_splash(screen, f"Player {current_player}'s turn!")

    # initialize crosshair position and game state
    cursor_row, cursor_col = 0, 0
    running = True
    winner = None

    while running:
        # calculate grid cell size and origin for current screen size
        cell_size = draw.compute_cell_size(rows, cols, screen.get_width(), screen.get_height())
        origin_x, origin_y = draw.compute_grid_origin(rows, cols, cell_size, screen.get_width(), screen.get_height())
        # get current player's hit and miss data
        hits = boat_manager.player_hits[current_player]
        # prepare instruction text for display
        instruction_text = f"Player {current_player}! Use Arrow Keys to lock your target, hit Space to fire!"

        # draw the entire firing phase screen including grid hits crosshair and instructions
        draw.draw_firing_screen(
            screen, rows, cols, cell_size, origin_x, origin_y,
            hits, cursor_row, cursor_col, instruction_text, assets
        )
        clock.tick(60)

        # handle user input events for quitting or moving and firing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # move crosshair up down left or right
                if event.key == pygame.K_UP:
                    cursor_row = max(0, cursor_row - 1)
                elif event.key == pygame.K_DOWN:
                    cursor_row = min(rows - 1, cursor_row + 1)
                elif event.key == pygame.K_LEFT:
                    cursor_col = max(0, cursor_col - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_col = min(cols - 1, cursor_col + 1)
                # fire at selected cell when space is pressed
                elif event.key == pygame.K_SPACE:
                    result = draw.animate_firing_shot(
                        screen, boat_manager, current_player, other_player,
                        cursor_row, cursor_col, cell_size, origin_x, origin_y, assets
                    )
                    # check if player hit missed or sunk a ship and update turn or end game
                    if result == "hit" or (result and result.startswith("sunk:")):
                        winner = boat_manager.check_win()
                        if winner:
                            running = False
                    elif result == "miss":
                        current_player, other_player = other_player, current_player
                        pygame.time.wait(1000)
                        draw.show_firing_splash(screen, f"Player {current_player}'s Turn")
    # return winner if there is one otherwise return none
    return f"Player {winner}" if winner else None
