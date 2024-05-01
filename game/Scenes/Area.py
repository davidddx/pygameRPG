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
        self.currentMap = Area.loadMapById(tmx_data= self.mapData, id= starting_map_idx, _doors= self.doors, _player=self.player)
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
                        entryPoint = (properties[Door.strENTRY_POINT_X], properties[Door.strENTRY_POINT_Y])

                        doorId = properties[Door.strDOOR_ID]
                        doors.append(Door(DOOR_ID=doorId, image=_object.image,
                                               id_current_map=mapId,
                                               pos=(_object.x * _object.width, _object.y * _object.height), entry_point = entryPoint))
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
    def loadMapById(tmx_data: list[list[pytmx.TiledMap, str]], id: int, _doors: list[Door], _player: Player) -> TileMap:
        dataIdx = 0
        nameIdx = 1
        tmxData = tmx_data[id][dataIdx]
        fileName = tmx_data[id][nameIdx]
        doors = []
        for door in _doors:
            if not door.idCurrentMap == id:
                continue
            doors.append(door)

        return TileMap(tmx_data= tmxData, map_id= id, name= fileName, _doors= doors, player=_player)
        # return TileMap(tmx_data= tmxData, map_id=mapId, name=fileName)

    def clear(self):
        self.currentMap.clear()


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
        self.currentMap = Area.loadMapById(tmx_data= self.mapData, id= self.mapIdx, _doors=self.doors, _player=self.player)
        logger.info(f"Successfully changed map to {self.currentMap=}")
        self.timeLastChangedMap = time_now

    def changeMapById(self, time_now: int, id: int):
        self.clear()
        self.currentMap = Area.loadMapById(tmx_data = self.mapData, id= self.mapIdx, _doors = self.doors, _player=self.player)

        self.timeLastChangedMap = time_now

    AREA_SWITCH_COOLDOWN = 150

    def update(self, screen):

        self.currentMap.update(screen=screen)
        self.checkChangeMapSignal(cool_down=Area.AREA_SWITCH_COOLDOWN)