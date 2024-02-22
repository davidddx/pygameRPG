from debug.logger import logger
import pygame
from game.SceneHandler import SceneHandler
import os
class Game:
    def __init__(self):
        try:
            logger.debug(f"Class {Game=} initializing....")
            self.sceneHandler = SceneHandler();
            cwd = os.getcwd()
            imagedir = cwd + '/images/test/YellowBlock.png'
            self.testImage = pygame.image.load(imagedir)

            pass

            logger.debug(f"Class {Game=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Game=} class initialization.\n Error: {e}")

    def run(self, screen : pygame.Surface):
        self.sceneHandler.run()

