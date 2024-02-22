import pygame
from debug.logger import logger
import globalVars.constants as globalVars

class Player:
    def __init__(self, pos : tuple[int,int,int], head_img : pygame.Surface, shirt_img : pygame.Surface, pants_img : pygame.Surface):
        try:
            logger.debug(f"class {Player=} initializing....")
            self.head = head_img
            self.shirt = shirt_img
            self.pants = pants_img

            self.pos = pos

            logger.debug(f"class {Player=} intialized.")

        except Exception as e:
            logger.info(f"Failed to intialize class {Player=}.\n Error: {e}")
    def update(self):
        globalVars.SCREEN.blit(self.head, (self.pos[0], self.pos[1] + self.shirt.get_height()))
        globalVars.SCREEN.blit(self.shirt, (self.pos[0], self.pos[1]))
        globalVars.SCREEN.blit(self.pants, (self.pos[0], self.pos[1] - self.shirt.get_height()))