import pytmx
import globalVars.SettingsConstants as SETTINGS
from debug.logger import logger
from game.TileMap import TileMap
import pygame
from game.Scenes.BaseScene import Scene, SceneStates
import os
import globalVars.PathConstants as PATH_CONSTANTS
from game.Player import Player
from game.Door import Door, DoorEntryPointIDs
from game.Tile import TileTypes

class Area(Scene):

    def __init__(self, name, starting_map_idx : int, _player : Player):

        logger.debug(f"Class {Area=} initializing....")
        super().__init__(name)
        self.state = SceneStates.INITIALIZING
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
        mapNames = []
        fileName = ""
        for file in os.listdir(TestMapDir):
            fileName = os.path.join(TestMapDir, file)
            mapNames.append(fileName)
        mapNames.sort()
        for mapName in mapNames:
            tmxData = pytmx.load_pygame(mapName)
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
                _type = "type"
                for _object in layer:
                    properties = _object.properties
                    if not properties[_type] == TileTypes.DOOR:
                        continue
                    entryPoint = properties[Door.strENTRY_POINT]

                    doorId = properties[Door.strDOOR_ID]
                    doors.append(Door(DOOR_ID=doorId, image=_object.image,
                                           id_current_map=mapId,
                                           pos=(_object.x, _object.y), entry_point = entryPoint))
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
    def loadMapById(tmx_data: list[list[pytmx.TiledMap, str]], id: int, _doors: list[Door], _player: Player, spawn_pos = None) -> TileMap:
        dataIdx = 0
        nameIdx = 1
        tmxData = tmx_data[id][dataIdx]
        fileName = tmx_data[id][nameIdx]
        doors = []
        for door in _doors:
            if not door.idCurrentMap == id:
                continue
            doors.append(door)

        if spawn_pos is None: return TileMap(tmx_data= tmxData, map_id= id, name= fileName, _doors= doors, player=_player)
        else: return TileMap(tmx_data= tmxData, map_id= id, name= fileName, _doors= doors, player=_player, player_pos= spawn_pos)
        # return TileMap(tmx_data= tmxData, map_id=mapId, name=fileName)

    def clear(self):
        self.currentMap.clear()


    def checkChangeMapSignal(self, cool_down : int):
        timenow = pygame.time.get_ticks()
        if timenow - self.timeLastChangedMap <= cool_down:
            return None
        keys = pygame.key.get_pressed()
        if self.currentMap.collidedDoor:
            destinationId = self.currentMap.collidedDoor.getIdDestinationMap()
            self.changeMapById(time_now=timenow, id=destinationId,
                               spawn_pos= Area.generatePlrSpawnPos(map_id=destinationId,
                                                                   doors=self.doors,
                                                                   collided_door=self.currentMap.collidedDoor))

    @staticmethod
    def generatePlrSpawnPos(map_id: int, doors: list[Door], collided_door: Door):
        for door in doors:
            if collided_door == door:
                continue
            if door.id != collided_door.id:
                continue
            doorPos = door.getPosition()
            spawnPos = None
            match door.entryPoint:
                case DoorEntryPointIDs.LEFT:
                    spawnPos = (doorPos[0] - door.rect.w, doorPos[1])
                case DoorEntryPointIDs.RIGHT:
                    spawnPos = (doorPos[0] + door.rect.w, doorPos[1])
                case DoorEntryPointIDs.UP:
                    spawnPos = (doorPos[0], doorPos[1] - door.rect.h)
                case DoorEntryPointIDs.DOWN:
                    spawnPos = (doorPos[0], doorPos[1] + door.rect.h)
                case _:
                    spawnPos = (doorPos[0], doorPos[1] + door.rect.h)
            return spawnPos

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

    def changeMapById(self, time_now: int, id: int, spawn_pos=None):
        self.clear()
        self.currentMap = Area.loadMapById(tmx_data = self.mapData, id= id, _doors = self.doors, _player=self.player, spawn_pos=spawn_pos)

        self.timeLastChangedMap = time_now

    AREA_SWITCH_COOLDOWN = 150

    def checkPauseSignal(self, state): 
        
        if state == SceneStates.PAUSED:
            pass
    def update(self, screen):
         
        self.currentMap.update(screen=screen) 
        self.checkChangeMapSignal(cool_down=Area.AREA_SWITCH_COOLDOWN)
        self.checkPauseSignal(state= self.state) 
