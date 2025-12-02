import pygame
from pygame.locals import *

pygame.init()


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Battleship")

# colors
running = True
while running:
    
    
    # stop the game
    for event in pygame.event.get():
        if event.type == pygame.quit():
            running = False


pygame.quit()