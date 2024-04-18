from debug.logger import logger
from game.TileMap import TileMap
import pygame
from game.Scenes.BaseScene import Scene
import os
import importlib
import globalVars.PathConstants as PATH_CONSTANTS
import globalVars.SceneConstants as SCENE_CONSTANTS
from game.Player import Player
import numpy as np
import pytmx.util_pygame as PyTMXpg
import globalVars.TilemapConstants as MAP_CONSTS

class Area(Scene):
    def __init__(self, name, map_idx : int, _player : Player):
        super().__init__(name)
        self.state = SCENE_CONSTANTS.STATE_INITIALIZING
        self.currentMap = None
        self.maps = ()
        self.mapIdx = 0
        self.timeLastChangedArea = 0
        self.player = _player
        self.camera = None
        try:
            logger.debug(f"Class {Area=} initializing....")
            self.mapIdx = map_idx
            self.maps = self.loadTestMaps()
            self.currentMap = self.maps[self.mapIdx]
            self.camera = np.array([])
            logger.debug(f"Class {Area=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Area=} class initialization.\n Error: {e}")

    def update(self, screen):
        # self.player.update();
        AREA_SWITCH_COOLDOWN = 70
        self.displayMap(_map=self.currentMap, screen=screen)
        self.playerCollisionHandler(player=self.player, _map=self.currentMap)
        self.player.update(screen=screen)
        self.checkChangeAreaSignal(cool_down = AREA_SWITCH_COOLDOWN)

    def loadTestMaps(self) -> tuple:
        maps = []
        TestMapDir = os.path.join(os.getcwd(),PATH_CONSTANTS.GAME_DATA, PATH_CONSTANTS.MAPS,PATH_CONSTANTS.TEST_MAPS)
        mapId = 0
        for file in os.listdir(TestMapDir):
            tmxData = PyTMXpg.load_pygame(os.path.join(TestMapDir, file))
            maps.append(TileMap(tmx_data= tmxData, MAP_ID=mapId))
            mapId += 1
        return tuple(maps)

    def initLoadMaps(self) -> tuple:

        maps = []
        cwd = os.getcwd();
        file = None
        try:
            logger.info(f"Loading Maps for area {self.name=}...")
            mapsDirectory = os.path.join(cwd, 'gamedata/Maps')
            logger.debug(f"Mapsdirectory: {os.listdir(mapsDirectory)=}")
            for folder in os.listdir(mapsDirectory):
                folderPath = os.path.join(os.path.join(mapsDirectory, folder))
                for fileName in os.listdir(folderPath):
                    if not (fileName.endswith(".py") and not fileName.startswith("__")):
                        continue
                    mapModuleName = fileName[:-3]  # Remove the ".py" extension
                    mapModulePath = f'{PATH_CONSTANTS.GAME_DATA}.{PATH_CONSTANTS.MAPS}.{folder}.{mapModuleName}'
                    logger.debug(f"Fetching maps from {folder=} \n Current Map: {mapModulePath=}")
                    try:
                        mapModule = importlib.import_module(mapModulePath)
                        logger.debug(f"Loading map module: {mapModule=}")

                        maps.append(TileMap(tile_set=mapModule.TileSet, tile_map=mapModule.Map,
                                          MAP_ID=mapModule.MAP_ID))
                        logger.debug(f"Loaded map module: {mapModule}")
                    except Exception as e:
                        file_path = os.path.abspath(os.path.join(mapsDirectory, folder))
                        logger.error(f"Failed to load scene module {mapModulePath} in file {file_path}: {e}")
            logger.info(f"Successfully loaded all Maps for area {self.name=}.")

        except Exception as e:
            logger.error(f"Failed to load maps.\nException: {e}")
        maps = tuple(maps)

        return maps

    def loadScene(self, map_id : int, maps : tuple):
        for _map in maps:
            if _map.mapID == map_id:
                return _map

    def clearScene(self):
        self.currentMap = 0

    def displayMap(self, _map : TileMap, screen):
        for tile in _map.spriteGroups[TileMap.trueSpriteGroupID]:
            # if not tile.inRange: continue
            screen.blit(tile.image, (tile.rect.x, tile.rect.y))

        # for spriteGroup in _map.spriteGroups:
        #     logger.debug(f"{spriteGroup=}")
        #     for tile in spriteGroup:
        #         screen.blit(tile.image, (tile.rect.x, tile.rect.y))

    def playerCollisionHandler(self, player : Player, _map : TileMap):


        COLLISION_TOLERANCE = 10
        collisionOccured = False
        player.onCollision = False
        for tile in _map.spriteGroups[MAP_CONSTS.COLLIDABLE_GROUP_ID]:
            # if not tile.inRange: continue

            if not player.rect.colliderect(tile):
                continue
            collisionOccured = True
            player.rectColor = (0,0,0)
            player.onCollision = True
        if not collisionOccured:
            player.rectColor = (255,255,255)
            return None

        ## handling collision ##

    def checkChangeAreaSignal(self, cool_down : int):
        timenow = pygame.time.get_ticks()
        if timenow - self.timeLastChangedArea <= cool_down:
            return None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.changeMapByStep(time_now= timenow)
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

        if self.mapIdx >= len(self.maps):
            self.mapIdx = originalIdx
            logger.error(
                f"Issue changing area to previous: \n \t \t \twhen {self.mapIdx=} added by {step=}, self.mapIdx is out of range.")
            return None

        self.clearScene()
        self.currentMap = self.loadScene(maps= self.maps, map_id= self.mapIdx)
        logger.info(f"Succefully changed map to {self.maps[self.mapIdx]=}")

