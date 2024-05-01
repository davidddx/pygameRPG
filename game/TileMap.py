import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import globalVars.TilemapConstants as mapVars
import pytmx as pyTMX
from game.Door import Door
import globalVars.SettingsConstants as SETTINGS
import game.Player as Player
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
    COLLISION_TYPE_DOOR_ID = 1

    def __init__(self, tmx_data, map_id: int, _doors: list[Door], player: Player, name=""):
        logger.debug(f"Class {TileMap=} initializing....")
        self.spriteGroups = ()
        self.doors = TileMap.initDoors(doors= _doors)
        self.player = player
        print(self.doors)
        self.name = name
        self.mapID = map_id
        self.spriteGroups = self.convertTMXToSpriteGroups(tmx_data= tmx_data)
        self.camera = TileMap.initializeCamera(player_rect = player.rect)
        logger.debug(f"Class {TileMap=} initialized.")

    @staticmethod
    def initDoors(doors: list[Door]):
        group = pygame.sprite.Group()
        group.add(doors)
        return group

    @staticmethod
    def initializeCamera(player_rect : pygame.Rect):
        return player_rect.x - SETTINGS.SCREEN_WIDTH/2 + player_rect.width/2, player_rect.y - SETTINGS.SCREEN_HEIGHT/2 + player_rect.height/2



    def clear(self):
        pass

    def playerCollisionHandler(self, player : Player):


        COLLISION_TOLERANCE = 10
        collisionOccured = False
        player.onCollision = False
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        for tile in self.spriteGroups[TileMap.SPRITE_GROUP_COLLISION_ID]:
            if not player.rect.colliderect(tile):
                continue
            collisionOccured = True
            player.rectColor = BLACK
            player.onCollision = True

            if not tile.collisionType == TileMap.COLLISION_TYPE_WALL_ID:
                return None
            elif tile.collisionType == TileMap.COLLISION_TYPE_DOOR_ID:
                pass
            else:
                if abs(player.rect.right - tile.rect.left) < COLLISION_TOLERANCE and player.movementDirection[0] > 0:
                    player.rect.right = tile.rect.left
                if abs(player.rect.left - tile.rect.right) < COLLISION_TOLERANCE and player.movementDirection[0] < 0:
                    player.rect.left = tile.rect.right
                if abs(player.rect.bottom - tile.rect.top) < COLLISION_TOLERANCE and player.movementDirection[1] > 0:
                    player.rect.bottom = tile.rect.top
                if abs(player.rect.top - tile.rect.bottom) < COLLISION_TOLERANCE and player.movementDirection[1] < 0:
                    player.rect.top = tile.rect.bottom


        if not collisionOccured:
            player.rectColor = WHITE
            return None

        ## handling collision ##

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

                trueSpriteGroup.add(spriteGroupNonCollision)
                trueSpriteGroup.add(self.doors)
                trueSpriteGroup.add(spriteGroupCollision)
            elif isinstance(layer, pyTMX.TiledObjectGroup):
                pass
                # name = "name"
                # for _object in layer:
                #     properties = _object.properties
                #     if properties[name] == Door.strNAME:
                #         doorId = properties[Door.strDOOR_ID]
                #         self.doors.append(Door(DOOR_ID=doorId, image=_object.image,
                #                                id_current_map= self.mapID, pos= (_object.x * _object.width, _object.y * _object.height)  ))

            layerIndex += 1




        logger.info(f"Converted map tmx data to spritegroups.")
        return (trueSpriteGroup, spriteGroupNonCollision, spriteGroupCollision)

    def displayMap(self, screen, camera: tuple[float, float]):
        for tile in self.spriteGroups[TileMap.trueSpriteGroupID]:
            if abs(self.player.rect.x - tile.rect.x) - SETTINGS.TILE_SIZE > SETTINGS.SCREEN_WIDTH/2 or abs(self.player.rect.y - tile.rect.y) - SETTINGS.TILE_SIZE > SETTINGS.SCREEN_HEIGHT/2:
                continue
            screen.blit(tile.image, (tile.rect.x - camera[0], tile.rect.y - camera[1]))

    @staticmethod
    def updateCameraPos(player_pos : tuple[float, float], player_rect : pygame.Rect, current_camera : tuple[float,float]) -> tuple[float, float]:
        return player_pos[0] - SETTINGS.SCREEN_WIDTH/2 + player_rect.width/2, player_pos[1] - SETTINGS.SCREEN_HEIGHT/2 + player_rect.height/2

    def update(self, screen):
        self.displayMap(screen=screen, camera=self.camera)
        self.playerCollisionHandler(player= self.player)
        self.camera = TileMap.updateCameraPos(player_pos = self.player.getPlayerPos(), current_camera=self.camera, player_rect=self.player.rect)
        self.player.update(screen= screen, camera= self.camera)
