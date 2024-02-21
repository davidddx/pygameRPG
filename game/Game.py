from debug.logger import logger
import pygame
from SceneHandler import SceneHandler
class Game:
    def __init__(self):
        try:
            logger.debug(f"Class {Game=} initializing....")
            self.sceneHandler = SceneHandler();

            pass

            logger.debug(f"Class {Game=} intialized.")
        except Exception as e:
            logger.debug(f"Failed {Game=} class initialization.\n Error: {e}")

    def run(self, screen : pygame.Surface):
        screen.blit()

