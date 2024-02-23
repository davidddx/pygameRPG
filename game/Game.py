from debug.logger import logger
import pygame
from game.SceneHandler import SceneHandler
import os
class Game:
    def __init__(self):
        try:
            logger.debug(f"Class {Game=} initializing....")
            self.sceneHandler = SceneHandler();
            logger.debug(f"Class {Game=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Game=} class initialization.\n Error: {e} \n File: Game.py")

    def run(self, screen):
        self.sceneHandler.run(screen=screen)

