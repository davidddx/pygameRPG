import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import globalVars.TilemapConstants as mapVars


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], collidable: bool, image: pygame.Surface, custom_properties=None):
        pygame.sprite.Sprite.__init__(self)

        self.collision = collidable
        self.image = image
        self.rect = image.get_rect(topleft=pos)
        self.isInRange = False
        self.customProperties = custom_properties


class TileMap:
    def __init__(self, tile_set: dict[str, dict], tile_map: tuple[tuple[tuple[str]]]):
        # tile_map should be in the following form:
        # Layer0 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
        # Layer1 = ( (uniqueTileCharA0, uniqueTileCharB0, .... ), (uniqueTileCharA1, uniqueTileCharB1, ....), ...)
        # .......
        # .......
        # .......
        # Map = (Layer0, Layer1, ....)
        self.collidableSpriteGroup = pygame.sprite.Group()
        self.nonCollidableSpriteGroup = pygame.sprite.Group()
        try:
            logger.debug(f"Class {TileMap=} initializing....")
            logger.debug(f"{tile_map=}")
            spriteGroups = TileMap.convertTupleToSpriteGroups(tile_set=tile_set,
                                                                     tile_map=tile_map,
                                                                     tile_size=globalVars.TILE_SIZE)
            self.collidableSpriteGroup = spriteGroups[0]
            self.nonCollidableSpriteGroup = spriteGroups[1]
            logger.debug(f"Class {TileMap=} initialized.")
        except Exception as e:
            logger.error(f"Failed {TileMap=} class initialization.\n Error: {e}")

    @staticmethod
    def convertTupleToSpriteGroups(tile_set : dict, tile_map: tuple[tuple[tuple[str]]], tile_size) \
            -> tuple[pygame.sprite.Group, pygame.sprite.Group]:
        spriteGroupCollision = pygame.sprite.Group()
        spriteGroupNonCollision = pygame.sprite.Group()
        tileListCollision = []
        tileListNonCollision = []

        for yvalue, layer in enumerate(tile_map):
            for xvalue, column in enumerate(layer):
                for layerNumber, letter in enumerate(column):
                    # logger.debug(f"{xvalue=}, {yvalue=}, {layerNumber=}")
                    if not letter in tile_set.keys():
                        logger.error(
                            f"{letter=} in {xvalue=}, {yvalue=}, {layerNumber=} \n is not defined in {tile_set=}")
                        continue
                    tileProperties = tile_set[letter]
                    image = tileProperties[mapVars.IMAGE]
                    collidable = tileProperties[mapVars.COLLISION]
                    tile = Tile(pos=(xvalue * globalVars.TILE_SIZE, yvalue * globalVars.TILE_SIZE), collidable=collidable,
                                image=image)
                    if tile.collision:
                        tileListCollision.append(tile)
                    else:
                        tileListNonCollision.append(tile)
        spriteGroupCollision.add(tileListCollision)
        spriteGroupNonCollision.add(tileListNonCollision)
        return (spriteGroupCollision, spriteGroupNonCollision)

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
    def createTileProperties(name: str, image: pygame.Surface, customProperties=None, collision=False) -> dict:
        logger.debug(f"Creating properties for tile {name=}. ")
        properties = {}
        try:
            properties = {
                mapVars.NAME: name,
                mapVars.IMAGE: image,
                mapVars.COLLISION: collision,
                mapVars.CUSTOM: customProperties,
            }
        except Exception as e:
            logger.error(f"Failed creating properties for tile {name=}.\nException: {e}")
        return properties
