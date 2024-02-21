import pygame
import sys, os
import globalVars.constants as constants
import game.Game as Game

def loop():
    pygame.init()
    running = True
    clock = pygame.time.Clock();
    screen = pygame.display.get_surface()
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    screenFillColor = "black"
    MAX_FPS = 45
    while running:
        clock.tick(MAX_FPS)
        keys = pygame.key.get_pressed()
        screen.fill(screenFillColor)

        Game.run(screen=screen)
        # render
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
