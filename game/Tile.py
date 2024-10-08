import pygame
from debug.logger import logger
class TileTypes:
    DOOR = "DOOR"
    SPAWN = "SPAWN"
    ITEM = "ITEM"
    VISUAL = "VISUAL"
    WALL = "WALL"
    ENEMY = "ENEMY"

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], collidable: bool, image: pygame.Surface,_type=None):
        pygame.sprite.Sprite.__init__(self)
        #Tiled uses gids to reference and differentiate tiles from eachother 
        self.collision = collidable
        self.tileType = _type
        self.image = image
        self.rect = image.get_rect(topleft=pos)
        self.inRange = False

    def getPos(self) -> tuple:
        return self.rect.x, self.rect.y

    def writeOutput(self):
        logger.debug(f"{self.collision=}")
        logger.debug(f"{self.tileType=}")
        logger.debug(f"{self.rect=}")
