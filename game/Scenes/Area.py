from debug.logger import logger
from game.TileMap import TileMap
import pygame
from game.Scenes.BaseScene import Scene
import os
import importlib
import globalVars.PathConstants as PATH_CONSTANTS

class Area(Scene):
    def __init__(self, map_idx : int):
        self.currentMap = None
        self.maps = ()
        self.mapIdx = 0
        self.timeLastChangedArea = 0
        try:
            logger.debug(f"Class {Area=} initializing....")
            self.mapIdx = map_idx
            self.maps = self.initLoadMaps()
            self.currentMap = self.maps[self.mapIdx]
            logger.debug(f"Class {Area=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Area=} class initialization.\n Error: {e}")

    def update(self, screen):
        # self.player.update();
        AREA_SWITCH_COOLDOWN = 70
        self.displayMap(_map=self.currentMap, screen=screen)
        self.checkChangeAreaSignal(cool_down = AREA_SWITCH_COOLDOWN)

    def initLoadMaps(self) -> tuple:

        maps = []
        cwd = os.getcwd();
        file = None
        try:
            logger.debug(f"Importing scenes...")
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
        for spriteGroup in _map.spriteGroups:
            for tile in spriteGroup:
                screen.blit(tile.image, (tile.rect.x, tile.rect.y))


    def checkChangeAreaSignal(self, cool_down : int):
        timenow = pygame.time.get_ticks()
        if timenow - self.timeLastChangedArea <= cool_down:
            return None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.changeAreaByStep(time_now= timenow)
        elif keys[pygame.K_q]:
            self.changeAreaByStep(time_now= timenow, positive=False)

    def changeAreaByStep(self, time_now: int, step=1, positive=True):
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
