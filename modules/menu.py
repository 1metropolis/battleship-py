import pygame
import math
import time

WHITE = (255, 255, 255)

# Button colors
BUTTON_COLOR = (112, 128, 144)
BUTTON_HOVER_COLOR = (176, 196, 222)

# Dark naval steel background
BG_COLOR = (18, 32, 47)

FONT_SIZE = 40
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 70

# Optional: load button click sound (place wav/ogg in assets/)
CLICK_SOUND_PATH = "assets/click.wav"
HOVER_SOUND_PATH = "assets/hover.wav"


def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None


def show_main_menu(screen):
    pygame.mixer.init()

    click_sound = load_sound(CLICK_SOUND_PATH)
    hover_sound = load_sound(HOVER_SOUND_PATH)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)

    # Load logo
    logo = pygame.image.load("assets/logo.png").convert_alpha()
    desired_width = min(600, screen.get_width() - 80)
    desired_height = int(desired_width * 66 / 398)
    logo = pygame.transform.smoothscale(logo, (desired_width, desired_height))
    logo_rect = logo.get_rect()
    logo_rect.centerx = screen.get_rect().centerx
    logo_rect.top = 125  # Top margin


    # Button centered under logo
    screen_rect = screen.get_rect()
    button_rect = pygame.Rect(
        (screen_rect.centerx - BUTTON_WIDTH // 2, int(screen_rect.height * 0.75) - BUTTON_HEIGHT // 2),
        (BUTTON_WIDTH, BUTTON_HEIGHT)
    )

    hovered_last_frame = False

    # Fade-in animation
    start_time = time.time()
    FADE_DURATION = 1.2  # seconds

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        dt = clock.tick(60) / 1000.0

        screen.fill(BG_COLOR)

        # -----------------------------
        # 1. Fade-in animation for logo
        # -----------------------------
        elapsed = time.time() - start_time
        fade_alpha = min(255, int((elapsed / FADE_DURATION) * 255))
        logo_fade = logo.copy()
        logo_fade.set_alpha(fade_alpha)

        screen.blit(logo_fade, logo_rect)

        # ------------------------------------
        # 3. Pulsing glow effect for the button
        # ------------------------------------
        pulse = 10 + int(math.sin(time.time() * 3) * 5)
        glow_rect = button_rect.inflate(pulse, pulse)
        pygame.draw.rect(
            screen,
            (80, 180, 255, 80),
            glow_rect,
            border_radius=12
        )

        # Hover effect + hover sound
        hovering = button_rect.collidepoint(mouse_pos)
        if hovering and not hovered_last_frame:
            if hover_sound:
                hover_sound.play()
        hovered_last_frame = hovering

        button_color = BUTTON_HOVER_COLOR if hovering else BUTTON_COLOR

        # Draw actual button
        pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=8)

        # Button text
        text_surface = font.render("Play", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and hovering:
                    if click_sound:
                        click_sound.play()
                    return  # Start game

        pygame.display.flip()
