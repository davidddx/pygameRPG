import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import globalVars.TilemapConstants as mapVars

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos : tuple[int, int], collidable : bool, size : int, image : pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.collision = collidable
        self.rect = image.get_rect(topleft=pos)
        self.isInRange = False
class TileMap:
    def __init__(self, tile_set: dict[str, dict], tile_map: tuple[tuple[tuple]]):
        # tile_map should be in the following form:
        # Layer0 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
        # Layer1 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
        # .......
        # .......
        # .......
        # Map = (Layer0, Layer1, ....)
        self.collidableGroup = TileMap.convertTupleToSpritegroup(tile_set=tile_set, tile_map = tile_map, tile_size= globalVars.TILE_SIZE)


    @staticmethod
    def convertTupleToSpritegroup(tile_set, tile_map : tuple[tuple[tuple]], tile_size):
        spriteGroup = pygame.sprite.Group();

        for layerNumber, layer in enumerate(tile_map):
            for yvalue, column in enumerate(layer):
                for xvalue, letter in enumerate(column):
                    if not letter in tile_set.keys():
                        logger.error(f"{letter=} in {xvalue=}, {yvalue=}, {layerNumber=} \n is not defined in {tile_set=}")


        pass
        
        return spriteGroup

class TileSet:

    # tile_set should be in the following form :
    # Letter1Properties = TileSet.createTileProperties(name= "Letter1", image = Letter1Directory,
    #                                       customProperties=aDictionaryOfCustomProperties, collision=True)
    # Letter2Properties = TileSet.createTileProperties(name= "Letter2", image = Letter2Directory,
    #                                       customProperties=aDictionaryOfCustomProperties, collision=False)
    # .........................
    # .........................
    # .........................
    # .........................
    #
    # tileset = {
    #   Letter1 : Letter1Properties
    #   Letter2 : Letter2Properties
    # .........................
    # .........................
    # .........................
    # .........................
    # }
    @staticmethod
    def createTileProperties(name : str, image : pygame.Surface, customProperties=None, collision=False):
        logger.debug(f"Creating properties for tile {name=}. ")
        properties = {}
        try:
            properties = {
                mapVars.NAME : name,
                mapVars.IMAGE : image,
                mapVars.COLLISION : collision,
                mapVars.CUSTOM : customProperties,
            }
        except Exception as e:
            logger.error(f"Failed creating properties for tile {name=}.\nException: {e}")
        return properties