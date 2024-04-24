import pygame
from debug.logger import logger

class Door(pygame.sprite.Sprite):
    strNAME = "door"
    strDOOR_ID = "DOOR_ID"

    def __init__(self, DOOR_ID: int, image: pygame.surface.Surface, id_current_map : int, pos : tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.idDestinationMap = None
        self.id = DOOR_ID
        self.image = image
        self.idCurrentMap = id_current_map
        self.rect = image.get_rect(topleft=pos)

    def writeOutput(self):
        logger.debug(f"Writing door output")
        logger.debug(f"{self.idDestinationMap=}")
        logger.debug(f"{self.id=}")
        logger.debug(f"{self.idCurrentMap=}")