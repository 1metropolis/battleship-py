import pygame
from pygame.locals import *
import sys

# load modules
from modules.file_handling import load_settings
from modules.draw import draw_grid
from modules.menu import show_main_menu
from modules.placement import placement_phase, start_game


# load settings
rows, cols, ships = load_settings()

# initalize pygame
pygame.init()

# screen dimensions
WIDTH, HEIGHT = 850, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# load assets and colors
windowicon = pygame.image.load("assets/icon.png")
bg = pygame.image.load("assets/battlemap.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)

# window icon and title
pygame.display.set_icon(windowicon)
pygame.display.set_caption("Battleship")


# main program
def main():
    # Show main menu first
    show_main_menu(screen)
    start_game(screen, rows, cols, ships)

    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.blit(bg, (0, 0))

        # Draw grid
        draw_grid(screen, rows, cols, WIDTH, HEIGHT)

        # Game logic goes here
        # TODO: implement ship placement, turns, hits/misses

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
