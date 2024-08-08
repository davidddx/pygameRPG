import pygame
from game.Tile import Tile, TileTypes
from debug.logger import logger

class DoorEntryPointIDs:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
class Door(Tile):
    strNAME = "DOOR"
    strDOOR_ID = "DOOR_ID"
    strENTRY_POINT = "entryPoint"
    intCOLLISION_TYPE = 1

    def __init__(self, DOOR_ID: int, image: pygame.surface.Surface, id_current_map : int, pos : tuple[int, int], entry_point: int):
        super().__init__(pos= pos, collidable=True, image= image, _type = TileTypes.DOOR)
        self.idDestinationMap = None
        self.id = DOOR_ID
        self.idCurrentMap = id_current_map
        self.entryPoint = entry_point

    def setIdDestinationMap(self, idDestinationMap: int):
        self.idDestinationMap = idDestinationMap

    def getIdDestinationMap(self):
        return self.idDestinationMap

    def getDoorId(self):
        return self.id

    def getIdCurrentMap(self):
        return self.idCurrentMap

    def getPosition(self):
        return self.rect.x, self.rect.y

    def writeOutput(self):
        logger.debug(f"Writing door output")
        logger.debug(f"{self.idDestinationMap=}")
        logger.debug(f"{self.id=}")
        logger.debug(f"{self.idCurrentMap=}")
        logger.debug(f"{self.entryPoint=}")
        logger.debug(f"{self.image=}")
        logger.debug(f"{(self.rect.x, self.rect.y)=}")

