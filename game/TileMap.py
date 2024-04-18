import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import globalVars.TilemapConstants as mapVars
import pytmx as pyTMX


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], collidable: bool, image: pygame.Surface, custom_properties=None):
        pygame.sprite.Sprite.__init__(self)

        self.collision = collidable
        self.image = image
        self.rect = image.get_rect(topleft=pos)
        self.inRange = False
        self.customProperties = custom_properties


class TileMap:
    trueSpriteGroupID = 0
    def __init__(self, tmx_data, MAP_ID: int):

        self.spriteGroups = ()
        self.mapID = 0
        try:
            logger.debug(f"Class {TileMap=} initializing....")
            self.spriteGroups = TileMap.convertTMXToSpriteGroups(tmx_data= tmx_data)
            self.mapID = MAP_ID
            logger.debug(f"Class {TileMap=} initialized.")
        except Exception as e:
            logger.error(f"Failed {TileMap=} class initialization.\n Error: {e}")

    @staticmethod
    def convertTMXToSpriteGroups(tmx_data : pyTMX.TiledMap) -> tuple[pygame.sprite.Group,pygame.sprite.Group]:
        spriteGroupCollision = pygame.sprite.Group()
        spriteGroupNonCollision = pygame.sprite.Group()
        trueSpriteGroup = pygame.sprite.Group()
        try:
            logger.info(f"Converting map tmx data to spritegroups...")
            visibleLayers = tmx_data.visible_layers
            layerIndex = 0
            for layer in visibleLayers:

                if not hasattr(layer, "data"):
                    continue
                logger.debug(dir(layer))
                for x, y, surface in layer.tiles():
                    pos = (globalVars.TILE_SIZE * x, globalVars.TILE_SIZE * y)
                    props = tmx_data.get_tile_properties(x, y, layerIndex);
                    collision = None
                    try:
                        collision = props["collision"]
                    except Exception as e:
                        collision = False
                    tile = Tile(pos= pos, collidable= collision, image= surface)
                    if collision:
                        spriteGroupCollision.add(tile)
                    else:
                        spriteGroupNonCollision.add(tile)
                    trueSpriteGroup.add(tile)

                layerIndex += 1
        except Exception as e:
            logger.error(f"Failed tmx to sprite.Group conversion: {e}")

        logger.info(f"Converted map tmx data to spritegroups.")
        return (trueSpriteGroup, spriteGroupNonCollision, spriteGroupCollision)

class TileSet:
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
