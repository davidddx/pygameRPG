import pygame
from debug.logger import logger

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