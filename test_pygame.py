import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1080,720))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
# time.sleep(5)