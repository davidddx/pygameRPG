import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import globalVars.TilemapConstants as mapVars
import pytmx as pyTMX
from game.Door import Door

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], collidable: bool, image: pygame.Surface,
                 collision_type=None):
        pygame.sprite.Sprite.__init__(self)

        self.collision = collidable
        self.collisionType = collision_type
        self.image = image
        self.rect = image.get_rect(topleft=pos)
        self.inRange = False


class TileMap:
    trueSpriteGroupID = 0
    SPRITE_GROUP_NON_COLLISION_ID = 1
    SPRITE_GROUP_COLLISION_ID = 2
    COLLISION_TYPE_WALL_ID = 0
    COLLISION_TYPE_MARKER_ID = 1

    def __init__(self, tmx_data, map_id: int, name=""):
        logger.debug(f"Class {TileMap=} initializing....")
        self.spriteGroups = ()
        self.doors = []
        self.name = name
        self.mapID = map_id
        self.spriteGroups = self.convertTMXToSpriteGroups(tmx_data= tmx_data)
        logger.debug(f"Class {TileMap=} initialized.")


    def clear(self):
        pass

    def convertTMXToSpriteGroups(self, tmx_data : pyTMX.TiledMap) -> tuple[pygame.sprite.Group,pygame.sprite.Group,pygame.sprite.Group,pygame.sprite.Group]:
        spriteGroupCollision = pygame.sprite.Group()
        spriteGroupNonCollision = pygame.sprite.Group()
        trueSpriteGroup = pygame.sprite.Group()
        logger.info(f"Converting map tmx data to spritegroups...")
        visibleLayers = tmx_data.visible_layers
        logger.debug(f"{visibleLayers=}")
        layerIndex = 0
        for layer in visibleLayers:
            if isinstance(layer, pyTMX.TiledTileLayer):
                for x, y, surface in layer.tiles():
                    pos = (globalVars.TILE_SIZE * x, globalVars.TILE_SIZE * y)
                    props = tmx_data.get_tile_properties(x, y, layerIndex)
                    collision = None
                    collisionType = None
                    try:
                        collision = props["collision"]
                        collisionType = props["collisionType"]
                    except Exception as e:
                        collision = False
                        collisionType = None
                    tile = Tile(pos= pos, collidable= collision, image= surface, collision_type=collisionType)
                    if collision:
                        spriteGroupCollision.add(tile)
                    else:
                        spriteGroupNonCollision.add(tile)
                    trueSpriteGroup.add(tile)
            elif isinstance(layer, pyTMX.TiledObjectGroup):
                name = "name"
                for _object in layer:
                    properties = _object.properties
                    if properties[name] == Door.strNAME:
                        doorId = properties[Door.strDOOR_ID]
                        self.doors.append(Door(DOOR_ID=doorId, image=_object.image,
                                               id_current_map= self.mapID, pos= (_object.x * _object.width, _object.y * _object.height)  ))

            layerIndex += 1




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
