import pygame
from modules.draw import draw_grid

def firing_phase(screen, boat_manager):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    current_player = 1
    other_player = 2
    rows, cols = boat_manager.rows, boat_manager.cols
    running = True
    winner = None
    while running:
        # Draw boards and get shot
        screen.fill((25,40,60))
        draw_grid(screen, rows, cols, screen.get_width(), screen.get_height())
        hits = boat_manager.player_hits[current_player]
        for r in range(rows):
            for c in range(cols):
                if hits[r][c] == "X":
                    rect = pygame.Rect(100 + c*30, 100 + r*30, 30, 30)
                    pygame.draw.rect(screen, (255,0,0), rect)
                elif hits[r][c] == "O":
                    rect = pygame.Rect(100 + c*30, 100 + r*30, 30, 30)
                    pygame.draw.rect(screen, (0,0,255), rect)
        instruction = font.render(f"Player {current_player}'s turn: Click to fire", True, (255,255,255))
        screen.blit(instruction, (100, 50))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                row = (my - 100) // 30
                col = (mx - 100) // 30
                if 0 <= row < rows and 0 <= col < cols:
                    result = boat_manager.fire_at(current_player, other_player, row, col)
                    if result == "hit":
                        # Check win
                        winner = boat_manager.check_win()
                        if winner:
                            running = False
                        # Player gets another turn
                    elif result == "miss":
                        # Switch players
                        current_player, other_player = other_player, current_player
                    # If repeat, do nothing
    return f"Player {winner}" if winner else None
