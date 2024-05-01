import pygame
from debug.logger import logger


class Door(pygame.sprite.Sprite):
    strNAME = "door"
    strDOOR_ID = "DOOR_ID"
    strENTRY_POINT_X = "entryPointx"
    strENTRY_POINT_Y = "entryPointy"
    intCOLLISION_TYPE = 1

    def __init__(self, DOOR_ID: int, image: pygame.surface.Surface, id_current_map : int, pos : tuple[int, int], entry_point = None):
        pygame.sprite.Sprite.__init__(self)
        self.idDestinationMap = None
        self.id = DOOR_ID
        self.image = image
        self.idCurrentMap = id_current_map
        self.rect = image.get_rect(topleft=pos)
        self.entryPoint = entry_point

    def writeOutput(self):
        logger.debug(f"Writing door output")
        logger.debug(f"{self.idDestinationMap=}")
        logger.debug(f"{self.id=}")
        logger.debug(f"{self.idCurrentMap=}")
        logger.debug(f"{self.entryPoint=}")
        logger.debug(f"{(self.rect.x, self.rect.y)=}")