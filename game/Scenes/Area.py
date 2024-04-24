import pytmx

import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
from game.TileMap import TileMap
import pygame
from game.Scenes.BaseScene import Scene
import os
import importlib
import globalVars.PathConstants as PATH_CONSTANTS
import globalVars.SceneConstants as SCENE_CONSTANTS
from game.Player import Player
import pytmx.util_pygame as PyTMXpg
import globalVars.TilemapConstants as MAP_CONSTS
from game.Door import Door

class Area(Scene):

    def __init__(self, name, starting_map_idx : int, _player : Player):

        logger.debug(f"Class {Area=} initializing....")
        super().__init__(name)
        self.state = SCENE_CONSTANTS.STATE_INITIALIZING
        self.timeLastChangedMap = 0
        self.player = _player
        self.mapIdx = starting_map_idx
        self.mapData = Area.loadMapTmxData()
        self.doors = Area.loadDoors(self.mapData)
        self.currentMap = Area.loadMapById(tmx_data= self.mapData, id= starting_map_idx)

        self.camera = Area.initializeCamera(player_rect = _player.rect)
        logger.debug(f"Class {Area=} intialized.")

    @staticmethod
    def loadMapTmxData() -> list[list[pytmx.TiledMap, str]]:
        TestMapDir = os.path.join(os.getcwd(),PATH_CONSTANTS.GAME_DATA, PATH_CONSTANTS.MAPS,PATH_CONSTANTS.TEST_MAPS)
        mapId = 0
        mapTmxData = []
        for file in os.listdir(TestMapDir):
            fileName = os.path.join(TestMapDir, file)
            tmxData = PyTMXpg.load_pygame(fileName)
            mapTmxData.append([tmxData, fileName])

        return mapTmxData

    @staticmethod
    def loadDoors(tmx_data: list[list[pytmx.TiledMap, str]]) -> list[Door]:
        ### Fetching the doors ###
        doors = []
        mapId = 0

        for data, fileName in tmx_data:
            visibleLayers = data.visible_layers
            for layer in visibleLayers:
                if not isinstance(layer, pytmx.TiledObjectGroup): continue
                name = "name"
                for _object in layer:
                    properties = _object.properties
                    if properties[name] == Door.strNAME:
                        doorId = properties[Door.strDOOR_ID]
                        doors.append(Door(DOOR_ID=doorId, image=_object.image,
                                               id_current_map=mapId,
                                               pos=(_object.x * _object.width, _object.y * _object.height)))
            mapId+=1

        doorAreaInfoDict = dict()
        for door in doors:
            if door.id in doorAreaInfoDict:
                doorList = doorAreaInfoDict[door.id]
                door.idDestinationMap = doorList[0].idCurrentMap
                doorList[0].idDestinationMap = door.idCurrentMap
                doorList.append(door.idCurrentMap)
            else:
                doorAreaInfoDict[door.id] = [door]
        for door in doors:
            door.writeOutput()
        return doors

    @staticmethod
    def loadMapById(tmx_data: list[list[pytmx.TiledMap, str]], id: int) -> TileMap:
        dataIdx = 0
        nameIdx = 1
        tmxData = tmx_data[id][dataIdx]
        fileName = tmx_data[id][nameIdx]

        return TileMap(tmx_data= tmxData, map_id= id, name= fileName)
        # return TileMap(tmx_data= tmxData, map_id=mapId, name=fileName)

    def clear(self):
        self.currentMap.clear()

    def displayMap(self, _map : TileMap, screen, camera: tuple[float, float]):
        for tile in _map.spriteGroups[TileMap.trueSpriteGroupID]:
            if abs(self.player.rect.x - tile.rect.x) - SETTINGS.TILE_SIZE > SETTINGS.SCREEN_WIDTH/2 or abs(self.player.rect.y - tile.rect.y) - SETTINGS.TILE_SIZE > SETTINGS.SCREEN_HEIGHT/2:
                continue
            screen.blit(tile.image, (tile.rect.x - camera[0], tile.rect.y - camera[1]))

        # for spriteGroup in _map.spriteGroups:
        #     logger.debug(f"{spriteGroup=}")
        #     for tile in spriteGroup:
        #         screen.blit(tile.image, (tile.rect.x, tile.rect.y))

    def playerCollisionHandler(self, player : Player, _map : TileMap):


        COLLISION_TOLERANCE = 10
        collisionOccured = False
        player.onCollision = False
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        for tile in _map.spriteGroups[MAP_CONSTS.COLLIDABLE_GROUP_ID]:
            if not player.rect.colliderect(tile):
                continue
            collisionOccured = True
            player.rectColor = BLACK
            player.onCollision = True

            if tile.collisionType == TileMap.COLLISION_TYPE_WALL_ID:
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

    def checkChangeMapSignal(self, cool_down : int):
        timenow = pygame.time.get_ticks()
        if timenow - self.timeLastChangedMap <= cool_down:
            return None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.changeMapByStep(time_now= timenow, step=1, positive=True)
        elif keys[pygame.K_q]:
            self.changeMapByStep(time_now= timenow, positive=False)

    def changeMapByStep(self, time_now: int, step=1, positive=True):
        if positive and step < 0:
            step = abs(step)
        elif (not positive) and step > 0:
            step = -step

        originalIdx = self.mapIdx

        self.mapIdx += step

        if self.mapIdx < 0:
            self.mapIdx=originalIdx
            logger.error(
                f"Issue changing area to previous: \n \t \t \twhen {self.mapIdx=} added by {step=}, self.mapIdx is out of range.")
            return None

        if self.mapIdx >= len(self.mapData):
            self.mapIdx = originalIdx
            logger.error(
                f"Issue changing area to previous: \n \t \t \twhen {self.mapIdx=} added by {step=}, self.mapIdx is out of range.")
            return None

        self.clear()
        self.currentMap = Area.loadMapById(tmx_data= self.mapData, id= self.mapIdx)
        logger.info(f"Successfully changed map to {self.currentMap=}")
        self.timeLastChangedMap = time_now

    @staticmethod
    def updateCameraPos(player_pos : tuple[float, float], player_rect : pygame.Rect, current_camera : tuple[float,float]) -> tuple[float, float]:
        return player_pos[0] - SETTINGS.SCREEN_WIDTH/2 + player_rect.width/2, player_pos[1] - SETTINGS.SCREEN_HEIGHT/2 + player_rect.height/2

    @staticmethod
    def initializeCamera(player_rect : pygame.Rect):
        return player_rect.x - SETTINGS.SCREEN_WIDTH/2 + player_rect.width/2, player_rect.y - SETTINGS.SCREEN_HEIGHT/2 + player_rect.height/2

    def update(self, screen):
        # self.player.update();
        AREA_SWITCH_COOLDOWN = 150
        self.displayMap(_map=self.currentMap, screen=screen, camera=self.camera)
        self.playerCollisionHandler(player=self.player, _map=self.currentMap)
        self.player.update(screen=screen, camera=self.camera)
        self.camera = Area.updateCameraPos(player_pos = self.player.getPlayerPos(), current_camera=self.camera, player_rect=self.player.rect)
        self.checkChangeMapSignal(cool_down = AREA_SWITCH_COOLDOWN)