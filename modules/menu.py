import pygame
import math

WHITE = (255, 255, 255)
BUTTON_COLOR = (112, 128, 144)
BUTTON_HOVER_COLOR = (176, 196, 222)
BG_COLOR = (18, 32, 47)
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 70
FONT_SIZE = 40

def show_main_menu(screen, winner=None):
    pygame.mixer.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    # Load logo
    logo = pygame.image.load("assets/logo.png").convert_alpha()
    desired_width = min(600, screen.get_width() - 80)
    desired_height = int(desired_width * 66 / 398)
    logo = pygame.transform.smoothscale(logo, (desired_width, desired_height))
    logo_rect = logo.get_rect()
    logo_rect.centerx = screen.get_rect().centerx
    logo_rect.top = 125

    # Button setup
    screen_rect = screen.get_rect()
    button_rect = pygame.Rect(
        (screen_rect.centerx - BUTTON_WIDTH // 2, int(screen_rect.height * 0.75) - BUTTON_HEIGHT // 2),
        (BUTTON_WIDTH, BUTTON_HEIGHT)
    )

    hovered_last_frame = False
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BG_COLOR)

        # Draw logo
        screen.blit(logo, logo_rect)

        # Pulsing glow effect
        pulse = 10 + int(math.sin(pygame.time.get_ticks() * 0.005) * 5)
        glow_rect = button_rect.inflate(pulse, pulse)
        pygame.draw.rect(screen, (80, 180, 255, 80), glow_rect, border_radius=12)

        # Hover effect
        hovering = button_rect.collidepoint(mouse_pos)
        button_color = BUTTON_HOVER_COLOR if hovering else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=8)

        # Button text
        text_surface = font.render("Play", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Winner text if any
        if winner:
            winner_text = font.render(f"{winner} Wins!", True, (255, 215, 0))
            screen.blit(winner_text, (screen_rect.centerx - winner_text.get_width()//2, 400))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and hovering:
                    running = False  # Start game

        pygame.display.flip()
        clock.tick(60)
