import game.SceneHandler as SceneHandler
from debug.DebugMenu import DebugMenu
import pygame
import sys, os
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger

def loop():
    pygame.init()
    running = True
    clock = pygame.time.Clock();
    screen = pygame.display.get_surface()
    pygame.init()
    screen = pygame.display.set_mode((SETTINGS.SCREEN_WIDTH, SETTINGS.SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True
    screenFillColor = "black"
    MAX_FPS = 45
    scale = 1
    sceneHandler = SceneHandler.SceneHandler(DEBUG=True)
    while running:
        logger.debug(f"CURRENT FPS: {clock.get_fps()}")
        clock.tick(MAX_FPS)
        screen.fill(screenFillColor)

        sceneHandler.runDebug(screen=screen, clock= clock, scale= scale)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
