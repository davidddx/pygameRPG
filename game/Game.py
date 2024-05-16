import game.SceneHandler as SceneHandler
import pygame
import sys, os
import globalVars.SettingsConstants as constants
from debug.logger import logger

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
    sceneHandler = SceneHandler.SceneHandler()
    while running:
        logger.debug(f"CURRENT FPS: {clock.get_fps()}")
        clock.tick(MAX_FPS)
        screen.fill(screenFillColor)

        sceneHandler.run(screen=screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
