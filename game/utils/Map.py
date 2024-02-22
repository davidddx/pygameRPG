import pygame
from debug.logger import logger
import globalVars.constants as globalVars


class TileMap:
    def __init__(self, tile_set: dict[str, pygame.Surface], tile_map: tuple[tuple]):
        self.collidableGroup = TileMap.convertTupleToSpritegroup(tile_set=tile_set, tile_map = tile_map, tile_size= globalVars.TILE_SIZE)


    @staticmethod
    def convertTupleToSpritegroup(tile_set, tile_map, tile_size):
        spriteGroup = pygame.sprite.Group();

        pass
        
        return spriteGroup