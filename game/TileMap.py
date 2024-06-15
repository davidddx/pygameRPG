import pygame
from debug.logger import logger
import globalVars.SettingsConstants as globalVars
import globalVars.TilemapConstants as mapVars
import pytmx as pyTMX
from game.Door import Door
from game.Item import Item, ItemConstants
import globalVars.SettingsConstants as SETTINGS
import game.Player as Player
from game.Tile import Tile, TileTypes
import gamedata.playerdata.Inventory as Inventory
class MapObjectNames:
    ## Spawn related ##
    SPAWN_DEFAULT = "SPAWN_DEFAULT"
    DOOR = "Door"

class TileMap:
    trueSpriteGroupID = 0
    SPRITE_GROUP_NON_COLLISION_ID = 1
    SPRITE_GROUP_COLLISION_ID = 2
    COLLISION_TYPE_WALL_ID = 0
    COLLISION_TYPE_DOOR_ID = 1

    def __init__(self, tmx_data, map_id: int, _doors: list[Door], player: Player.Player, taken_items: list, player_pos= None, name=""):
        logger.debug(f"Class {TileMap=} initializing....")
        
        self.timeMapInitialized = pygame.time.get_ticks()
        self.playerSpawnPos = player_pos
        self.spriteGroups = ()
        self.doors = TileMap.initDoors(doors= _doors)
        self.collidedDoor = None
        self.player = player
        self.writeCurrentDoorsOutput()
        self.name = name
        self.mapID = map_id
        self.takenItems = taken_items
        self.spriteGroups = self.convertTMXToSpriteGroups(tmx_data= tmx_data)
        self.player.setPlayerPos(pos_x=self.playerSpawnPos[0], pos_y=self.playerSpawnPos[1])
        self.player.setPlayerMovability(False)
        self.camera = TileMap.initializeCamera(player_rect= player.rect)
        print(f"tilemap taken items {self.takenItems=}")
        print(f"{type(taken_items)=}")
        logger.debug(f"Class {TileMap=} initialized.")


    def writeCurrentDoorsOutput(self):
        logger.debug("Writing output for all doors in this map...")
        for door in self.doors:
            door.writeOutput()

        logger.debug("Finished writing output for all doors in map.")
    @staticmethod
    def initDoors(doors: list[Door]):
        group = pygame.sprite.Group()
        group.add(doors)
        return group

    @staticmethod
    def initializeCamera(player_rect : pygame.Rect):
        return player_rect.x - SETTINGS.SCREEN_WIDTH/2 + player_rect.width/2, player_rect.y - SETTINGS.SCREEN_HEIGHT/2 + player_rect.height/2



    def clear(self):
        for group in self.spriteGroups:
            group.empty()

    @staticmethod
    def collidePlayerWithTile(onCollision: list[bool], player: Player.Player, tile: Tile, offset= 0) -> None:
        if onCollision[Player.PlayerRectCollisionIDs.RIGHT]:
            player.rect.right = tile.rect.left + offset
        if onCollision[Player.PlayerRectCollisionIDs.LEFT]:
            player.rect.left = tile.rect.right - offset
        if onCollision[Player.PlayerRectCollisionIDs.DOWN]:
            player.rect.bottom = tile.rect.top + offset
        if onCollision[Player.PlayerRectCollisionIDs.UP]:
            player.rect.top = tile.rect.bottom - offset


    def playerCollisionHandler(self, player : Player.Player):
        COLLISION_TOLERANCE = 10
        collisionOccured = False
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        group = self.spriteGroups[TileMap.SPRITE_GROUP_COLLISION_ID]
        for tile in group:
            if not player.rect.colliderect(tile):
                continue
            collisionOccured = True
            player.rectColor = BLACK
            onCollision = [False, False, False, False]
            
            ### checking for collision ###
            if abs(player.rect.right - tile.rect.left) < COLLISION_TOLERANCE and player.movementDirection[0] > 0:
                onCollision[Player.PlayerRectCollisionIDs.RIGHT] = True
            if abs(player.rect.left - tile.rect.right) < COLLISION_TOLERANCE and player.movementDirection[0] < 0:
                onCollision[Player.PlayerRectCollisionIDs.LEFT] = True
            if abs(player.rect.bottom - tile.rect.top) < COLLISION_TOLERANCE and player.movementDirection[1] > 0:
                onCollision[Player.PlayerRectCollisionIDs.DOWN] = True
            if abs(player.rect.top - tile.rect.bottom) < COLLISION_TOLERANCE and player.movementDirection[1] < 0:
                onCollision[Player.PlayerRectCollisionIDs.UP] = True
            ### USING COLLISION INFO ###
            if tile.tileType == TileTypes.DOOR:
                self.collidedDoor = tile
                return None
            
            elif tile.tileType == TileTypes.WALL:
                TileMap.collidePlayerWithTile(onCollision= onCollision, player= player, tile= tile) 
            elif tile.tileType == TileTypes.ITEM:
                TileMap.collidePlayerWithTile(onCollision= onCollision, player= player, tile= tile, offset=1)
            if tile.tileType == TileTypes.ITEM:
                if player.getInputState() == Player.PossiblePlayerInputStates.SELECTION_INPUT:
                    self.takeItem(tile)
                    self.removeTileFromMap(tile)
                    self.addItemToInventory(item= tile)
                    continue



        if not collisionOccured:
            player.rectColor = WHITE
            return None
    def removeTileFromMap(self, tile: Tile):
        for spritegroup in self.spriteGroups:
            try:
                spritegroup.remove(tile)
            except:
                continue

    def convertTMXToSpriteGroups(self, tmx_data : pyTMX.TiledMap, spawn_default=None) -> tuple[pygame.sprite.Group,pygame.sprite.Group,pygame.sprite.Group,pygame.sprite.Group]:
        spriteGroupCollision = pygame.sprite.Group()
        spriteGroupCollisionList = []
        spriteGroupNonCollision = pygame.sprite.Group()
        spriteGroupNonCollisionList = []
        trueSpriteGroup = pygame.sprite.Group()
        items = []
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
                        tileType = props["type"]
                    except:
                        collision = False
                        tileType = None
                    tile = Tile(pos= pos, collidable= collision, image= surface, _type=tileType)
                    if collision:
                        spriteGroupCollisionList.append(tile)
                    else:
                        spriteGroupNonCollisionList.append(tile)

            elif isinstance(layer, pyTMX.TiledObjectGroup):
                name = "name"
                objType = "type"
                for _object in layer:
                    properties = _object.properties
                    
                    match properties[objType]:
                        case TileTypes.SPAWN:
                            if self.playerSpawnPos is None: self.playerSpawnPos = (_object.x, _object.y)
                        case TileTypes.ITEM:
                            if self.checkItemTaken(pos= (_object.x, _object.y), name = properties[name], takenItems= self.takenItems ):
                                continue
                            items.append(Item(sprite= _object.image, pos= (_object.x, _object.y), name= properties[name]))

            layerIndex += 1
        spriteGroupCollision.add(items)
        spriteGroupCollision.add(spriteGroupCollisionList)
        spriteGroupCollision.add(self.doors)
        spriteGroupNonCollision.add(spriteGroupNonCollisionList)
        trueSpriteGroup.add(spriteGroupNonCollision)
        trueSpriteGroup.add(spriteGroupCollision)


        logger.info(f"Converted map tmx data to spritegroups.")
        return (trueSpriteGroup, spriteGroupNonCollision, spriteGroupCollision)
   
    def takeItem(self, item : Item):
        self.takenItems.append({item.getName(), item.getPos()})
    
    def checkItemTaken(self, pos: tuple, name: str, takenItems):
        try:
            if {pos,name} in takenItems:
                return True
            return False
        except:
            return False

    def displayMap(self, screen, camera: tuple[float, float], player: Player.Player):
        renderAfterGroup = pygame.sprite.Group()
        for tile in self.spriteGroups[TileMap.trueSpriteGroupID]:
            if abs(self.player.rect.x - tile.rect.x) - SETTINGS.TILE_SIZE > SETTINGS.SCREEN_WIDTH/2 or abs(self.player.rect.y - tile.rect.y) - SETTINGS.TILE_SIZE > SETTINGS.SCREEN_HEIGHT/2:
                continue
            
            if player.rect.y < tile.rect.y:
                
                if tile.collision:
                    renderAfterGroup.add(tile)
                    continue
            
                    
            # logger.debug(f"Blitting tile of type: {type(tile)=}")
            screen.blit(tile.image, (tile.rect.x - camera[0], tile.rect.y - camera[1]))
        player.update(screen= screen, camera= camera)
        for tile in renderAfterGroup:
            screen.blit(tile.image, (tile.rect.x - camera[0], tile.rect.y - camera[1]))
        renderAfterGroup.empty()
        

    @staticmethod
    def updateCameraPos(player_pos : tuple[float, float], player_rect : pygame.Rect, current_camera : tuple[float,float]) -> tuple[float, float]:
        return player_pos[0] - SETTINGS.SCREEN_WIDTH/2 + player_rect.width/2, player_pos[1] - SETTINGS.SCREEN_HEIGHT/2 + player_rect.height/2

    def checkMapCooldownForPlayerMovement(self):
        if self.player.movable:
            return None
        timenow = pygame.time.get_ticks()
        cooldown = 1000
        if timenow - self.timeMapInitialized < cooldown:
            return None
        self.player.setPlayerMovability(True)

    @staticmethod
    def addItemToInventory(item : Item):
        if not Item.checkValidItem(item):
            logger.error(f"could not add the following item to inventory: \n {item.getId()=} \n {item.getName()=}")
        Inventory.addItemToInventory(item_id = item.getId(), item_category = ItemConstants.getCategoryById(item.getId())) 
        
    def getTakenItems(self): return self.takenItems
   
    def getId(self): return self.mapID

    def update(self, screen: pygame.Surface):
        self.checkMapCooldownForPlayerMovement()
        self.displayMap(screen=screen, camera=self.camera, player= self.player)
        self.playerCollisionHandler(player= self.player)
        self.camera = TileMap.updateCameraPos(player_pos = self.player.getPlayerPos(), current_camera=self.camera, player_rect=self.player.rect)
