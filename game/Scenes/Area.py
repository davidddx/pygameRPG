import pytmx
from debug.logger import logger
from game.TileMap import TileMap
import pygame
from game.Scenes.BaseScene import Scene, SceneStates, SceneTypes
import os
import globalVars.PathConstants as PATH_CONSTANTS
from game.Player import Player
from game.Door import Door, DoorEntryPointIDs
from game.Tile import TileTypes
#import gamedata.playerdata.Inventory as Inventory
import json

class Area(Scene):

    def __init__(self, name, starting_map_idx : int, _player : Player, area_id = 0):
        timeInitStarted = pygame.time.get_ticks()
        logger.debug(f"Class {Area=} initializing....")
        super().__init__(name)
        self.areaID = area_id
        self.state = SceneStates.INITIALIZING
        self.timeLastChangedMap = 0
        self.player = _player
        self.mapIdx = starting_map_idx
        self.mapData = Area.loadMapTmxData()
        self.doors = Area.loadDoors(self.mapData)
        self.takenItems = Area.loadTakenItems(self.mapIdx, len(self.mapData))
        self.currentMap = self.loadMapById(tmx_data= self.mapData, id= starting_map_idx, _doors= self.doors, _player=self.player, area_id = self.areaID)
        self.timeLastPaused = 0        
        self.state = SceneStates.RUNNING
        logger.debug(f"Class {Area=} intialized. Time taken: {pygame.time.get_ticks() - timeInitStarted}")

    def updateTakenItems(self, current_map_idx: int):
        ''' TAKEN ITEM FORMAT 
        {
            AREA_ID0: {
                MAP_ID0 : [ [item0name, item0pos],
                            [item1name, item1pos],
                            ...
                            [itemNname, itemNpos]
                        ]
                MAP_ID1 : [ [item0name, item0pos],
                            [item1name, item1pos],
                            ...
                            [itemNname, itemNpos]
                        ]
                ...,

                MAP_IDN : [ [item0name, item0pos],
                            [item1name, item1pos],
                            ...
                            [itemNname, itemNpos]
                        ]
            },
            AREA_ID1: {
                ...
            },
            ...
            ,
            AREA_IDN : {
                ...
            }

        }

        '''
        #self.takenItems[str(current_map_idx)] = self.currentMap.getTakenItems()
        
    @staticmethod
    def loadTakenItems(area_id: int, map_len: int) -> dict: 
        takenItems = {}
        strPath = os.path.join(os.getcwd(), "gamedata", "Maps", "TakenItems.json")
        file = open(strPath, "r")
        takenItems = json.load(file)
        try:
            areaTakenItems = takenItems[str(area_id)]
        except:
            logger.info("No base list detected for {area_id=}. Creating now....")
            takenItems[str(area_id)] = {} 
            areaTakenItems = takenItems[str(area_id)]
        return areaTakenItems 

    def getTakenItemsPath(self): return os.path.join(os.getcwd(), "gamedata", "Maps", "TakenItems.json")

    def getTakenItemsDict(self):
        file = open(self.getTakenItemsPath(), 'r')
        dictionary = json.load(file)
        file.close()
        return dictionary

    def saveTakenItems(self, area_id: int, taken_items):
        logger.debug("SAVING TAKEN ITEMS...")
        allTakenItems = self.getTakenItemsDict()
        logger.debug(f"{taken_items=}, {allTakenItems=}")
        allTakenItems[str(area_id)] = taken_items
        logger.debug(f"{allTakenItems=}")
        file = open(self.getTakenItemsPath(), 'w')
        json.dump(allTakenItems, file)
        file.close()
        logger.debug("TAKEN ITEMS SAVED...")

    @staticmethod
    def loadMapTmxData() -> list[list]:
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

    def getCollidedEnemyName(self):
        return self.currentMap.getCollidedEnemyName()

    @staticmethod
    def loadDoors(tmx_data: list[list[pytmx.TiledMap, str]]) -> list[Door]:
        ### Fetching the doors ###
        doors = []
        mapId = 0

        for data, fileName in tmx_data:
            visibleLayers = data.visible_layers
            for layer in visibleLayers:
                if not isinstance(layer, pytmx.TiledObjectGroup): continue
                name = "NAME"
                _type = "TYPE"
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

    
    def loadMapById(self, tmx_data: list[list[pytmx.TiledMap, str]], id: int, _doors: list[Door], _player: Player, spawn_pos = None, area_id=0) -> TileMap:
        dataIdx = 0
        nameIdx = 1
        tmxData = tmx_data[id][dataIdx]
        fileName = tmx_data[id][nameIdx]
        doors = []
        for door in _doors:
            if door.idCurrentMap != id:
                continue
            doors.append(door)
        takenItems = self.checkTakenItemsForMap(map_id = id, area_id = self.areaID)
        logger.debug(f"{takenItems=}")
        if spawn_pos is None: return TileMap(tmx_data= tmxData, map_id= id,  _doors= doors, player=_player, taken_items= takenItems, name= fileName,area_id= area_id)
        else: return TileMap(tmx_data= tmxData, map_id= id, name= fileName, _doors= doors, player=_player, player_pos= spawn_pos, taken_items= takenItems, area_id= area_id)

    def checkTakenItemsForMap(self, map_id: int, area_id: int):
        #logger.debug(" checking taken items for map... ")
        #logger.debug(f"{self.takenItems=}")
        mapTakenItems = []
        try:
            mapTakenItems = self.takenItems[str(map_id)]
        except Exception as e:
            logger.info(f"{e}, No base list detected for {area_id=}, {map_id=}. Creating now....")
            self.takenItems[str(map_id)] = []
            mapTakenItems = self.takenItems[str(map_id)]
        logger.debug(f"{mapTakenItems=}")
        return mapTakenItems 

    def clear(self):
        self.currentMap.clear()

    def setEnemyLock(self, milliseconds):
        self.currentMap.setEnemyLock(milliseconds)

    def clearCollidedObject(self):
        self.currentMap.collidedObject = None

    def checkChangeMapSignal(self, cool_down : int):
        timenow = pygame.time.get_ticks()
        if timenow - self.timeLastChangedMap <= cool_down:
            return None
        if self.currentMap.collidedDoor:
            self.saveTakenItems(area_id= self.areaID, taken_items = self.takenItems)
            self.updateTakenItems(self.mapIdx)
            destinationId = self.currentMap.collidedDoor.getIdDestinationMap()
            self.changeMapById(time_now=timenow, id=destinationId,spawn_pos= Area.generatePlrSpawnPos(map_id=destinationId,doors=self.doors, collided_door=self.currentMap.collidedDoor))

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
        self.currentMap = self.loadMapById(tmx_data= self.mapData, id= self.mapIdx, _doors=self.doors, _player=self.player, area_id = self.areaID)
        logger.info(f"Successfully changed map to {self.currentMap=}")
        self.timeLastChangedMap = time_now

    def changeMapById(self, time_now: int, id: int, spawn_pos=None):
        self.updateTakenItems(self.currentMap.getId())
        self.clear()
        self.currentMap = self.loadMapById(tmx_data = self.mapData, id= id, _doors = self.doors, _player=self.player, spawn_pos=spawn_pos, area_id = self.areaID)

        self.mapIdx = id
        self.timeLastChangedMap = time_now

    AREA_SWITCH_COOLDOWN = 150

    def checkPauseSignal(self, state): 
        pauseCooldown = 300
        timenow = pygame.time.get_ticks()
        if timenow - self.timeLastPaused < pauseCooldown:
            return None
        if state == SceneStates.PAUSED:
            return None
        pauseKey = pygame.K_x 
        keys = pygame.key.get_pressed()
        if keys[pauseKey]:
            self.state = SceneStates.PAUSED
            self.setPtrNextScene(SceneTypes.PAUSE_MENU)
            self.timeLastPaused = timenow

    def setTimeLastPaused(self, timeLastPaused):
        self.timeLastPaused = timeLastPaused

    def getTimeLastPaused(self): return self.timeLastPaused

    def getCurrentMapId(self): return self.currentMap.mapID

    def getState(self): return self.state

    def setState(self, state: str): self.state = state

    def getPlayer(self): return self.player

    def checkEnemyCollision(self, collided_enemy_name):
        if collided_enemy_name is None: return None
        self.setPtrNextScene(SceneTypes.BATTLE)
        self.setState(SceneStates.PAUSED)

    def update(self, screen: pygame.Surface):
        #logger.debug(f"{self.mapIdx=}")
        #logger.debug(f"{self.takenItems=}") 
        self.currentMap.update(screen=screen) 
        self.checkChangeMapSignal(cool_down=Area.AREA_SWITCH_COOLDOWN)
        self.checkPauseSignal(state= self.state) 
        self.checkEnemyCollision(self.currentMap.getCollidedEnemyName())
