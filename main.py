import pygame
from pygame.locals import *

pygame.init()

# screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# window icon and title
windowicon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(windowicon)
pygame.display.set_caption("Battleship")

running = True
while running:

    pass
    # # stop the game
    # for event in pygame.event.get():
    #     if event.type == pygame.quit():
    #         running = False


pygame.quit()