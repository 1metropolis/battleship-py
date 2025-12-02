import pygame
import sys
from modules.file_handling import load_settings
from modules.menu import show_main_menu
from modules.placement import placement_phase
from modules.firing import firing_phase
from modules.boat_management import BoatManager

# Load settings
rows, cols, ships = load_settings()

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 850, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load assets and colors
windowicon = pygame.image.load("assets/icon.png")
bg = pygame.image.load("assets/battlemap.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Window icon and title
pygame.display.set_icon(windowicon)
pygame.display.set_caption("Battleship")

def main():
    running = True
    
    while running:
        # Quit logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Show main menu
        show_main_menu(screen)

        # Initialize BoatManager for this game
        boat_manager = BoatManager(rows, cols, ships)

        # Start placement phase for both players
        for player in [1, 2]:
            placement_phase(screen, rows, cols, ships, f"Player {player}", boat_manager, player)

        # Start firing phase
        winner = firing_phase(screen, boat_manager)

        # Show winner and loop back to menu
        show_main_menu(screen, winner=winner)

if __name__ == "__main__":
    main()
