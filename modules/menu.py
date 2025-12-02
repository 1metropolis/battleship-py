import pygame
import math

# Colors and sizes
WHITE = (255, 255, 255)
BUTTON_COLOR = (112, 128, 144)
BUTTON_HOVER_COLOR = (176, 196, 222)
BG_COLOR = (18, 32, 47)
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 70
FONT_SIZE = 40
INSTRUCTION_FONT_SIZE = 28

def show_how_to_play(screen):
    """Display the instructions screen."""
    font = pygame.font.SysFont(None, INSTRUCTION_FONT_SIZE)
    clock = pygame.time.Clock()
    running = True

    instructions = [
        "Battleship Instructions:",
        "",
        "1. Each player places their ships on their grid.",
        "2. Ships cannot overlap and must fit within the grid.",
        "3. Players take turns firing at the opponent's grid.",
        "4. A hit is marked and a miss is ignored.",
        "5. The first player to sink all enemy ships wins.",
        "",
        "Click 'Back' to return to the main menu."
    ]

    # Back button
    screen_rect = screen.get_rect()
    back_rect = pygame.Rect(
        (screen_rect.centerx - BUTTON_WIDTH // 2, screen_rect.bottom - 100),
        (BUTTON_WIDTH, BUTTON_HEIGHT)
    )

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BG_COLOR)

        # Draw instructions
        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, WHITE)
            screen.blit(text_surface, (50, 50 + i * 35))

        # Glow effect for Back button
        pulse = 10 + int(math.sin(pygame.time.get_ticks() * 0.005) * 5)
        glow_surf = pygame.Surface((BUTTON_WIDTH + pulse, BUTTON_HEIGHT + pulse), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (80, 180, 255, 80), glow_surf.get_rect(), border_radius=12)
        screen.blit(glow_surf, (back_rect.x - pulse//2, back_rect.y - pulse//2))

        # Draw back button
        hovering = back_rect.collidepoint(mouse_pos)
        button_color = BUTTON_HOVER_COLOR if hovering else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, back_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, back_rect, 3, border_radius=8)

        # Draw Back text
        text_surface = font.render("Back", True, WHITE)
        text_rect = text_surface.get_rect(center=back_rect.center)
        screen.blit(text_surface, text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hovering:
                running = False  # Return to main menu

        pygame.display.flip()
        clock.tick(60)

def show_main_menu(screen, winner=None):
    """Main menu with Play and How to Play buttons, with glow effect."""
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    # Load logo
    logo = pygame.image.load("assets/logo.png").convert_alpha()
    desired_width = min(600, screen.get_width() - 80)
    desired_height = int(desired_width * 66 / 398)
    logo = pygame.transform.smoothscale(logo, (desired_width, desired_height))
    logo_rect = logo.get_rect()
    logo_rect.centerx = screen.get_rect().centerx
    logo_rect.top = 100

    # Button positions
    screen_rect = screen.get_rect()
    play_rect = pygame.Rect(screen_rect.centerx - BUTTON_WIDTH//2, 330, BUTTON_WIDTH, BUTTON_HEIGHT)
    how_to_play_rect = pygame.Rect(screen_rect.centerx - BUTTON_WIDTH//2, 430, BUTTON_WIDTH, BUTTON_HEIGHT)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BG_COLOR)

        # Draw logo
        screen.blit(logo, logo_rect)

        # Winner text
        if winner:
            winner_text = font.render(f"{winner} Wins!", True, (255, 215, 0))
            screen.blit(winner_text, (screen_rect.centerx - winner_text.get_width() // 2, 400))

        # Pulsing glow
        pulse = 10 + int(math.sin(pygame.time.get_ticks() * 0.005) * 5)

        # Glow for Play button
        glow_play = pygame.Surface((BUTTON_WIDTH + pulse, BUTTON_HEIGHT + pulse), pygame.SRCALPHA)
        pygame.draw.rect(glow_play, (80, 180, 255, 80), glow_play.get_rect(), border_radius=12)
        screen.blit(glow_play, (play_rect.x - pulse//2, play_rect.y - pulse//2))

        # Glow for How to Play button
        glow_htp = pygame.Surface((BUTTON_WIDTH + pulse, BUTTON_HEIGHT + pulse), pygame.SRCALPHA)
        pygame.draw.rect(glow_htp, (80, 180, 255, 80), glow_htp.get_rect(), border_radius=12)
        screen.blit(glow_htp, (how_to_play_rect.x - pulse//2, how_to_play_rect.y - pulse//2))

        # Draw buttons
        hovering_play = play_rect.collidepoint(mouse_pos)
        hovering_htp = how_to_play_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if hovering_play else BUTTON_COLOR, play_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, play_rect, 3, border_radius=8)
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if hovering_htp else BUTTON_COLOR, how_to_play_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, how_to_play_rect, 3, border_radius=8)

        # Draw button text
        text_surface_play = font.render("Play", True, WHITE)
        screen.blit(text_surface_play, text_surface_play.get_rect(center=play_rect.center))
        text_surface_htp = font.render("How to Play", True, WHITE)
        screen.blit(text_surface_htp, text_surface_htp.get_rect(center=how_to_play_rect.center))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovering_play:
                    running = False  # Start game
                elif hovering_htp:
                    show_how_to_play(screen)

        pygame.display.flip()
        clock.tick(60)
