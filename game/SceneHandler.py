from debug.logger import logger
import globalVars.PathConstants as PATH_CONSTANTS
from game.TileMap import TileMap
from game.Area import Area
import os
import importlib
import pygame
import gamedata.Save.SavedData as SAVED_DATA
class SceneHandler:
    def __init__(self):
        self.scenes = ()
        self.Areas = None
        self.currentScene = None
        self.currentSceneIndex = 0
        self.SCENE_COUNT = 0
        self.timeLastChangedScene = pygame.time.get_ticks()
        try:
            logger.debug(f"Class {SceneHandler=} initializing....")
            self.Areas = self.getAreas()
            self.scenes = self.Areas
            self.SCENE_COUNT = len(self.Areas)
            logger.debug(f"{self.SCENE_COUNT=}")
            self.currentSceneIndex = SAVED_DATA.CURRENT_SCENE_INDEX
            self.currentScene = self.Areas[self.currentSceneIndex]
            logger.debug(f"Class {SceneHandler=} intialized.")
        except Exception as e:
            logger.error(f"Failed {SceneHandler=} class initialization.\n Error: {e}")

    def getAreas(self):
        def getTileMaps():
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
                        if fileName.endswith(".py") and not fileName.startswith("__"):
                            mapModuleName = fileName[:-3]  # Remove the ".py" extension
                            mapModulePath = f'{PATH_CONSTANTS.GAME_DATA}.{PATH_CONSTANTS.MAPS}.{folder}.{mapModuleName}'
                            logger.debug(f"Fetching maps from {folder=} \n Current Map: {mapModulePath=}")
                            try:

                                mapModule = importlib.import_module(mapModulePath)
                                logger.debug(f"Loading map module: {mapModule=}")
                                tileMap = TileMap(tile_set=mapModule.TileSet, tile_map=mapModule.Map)
                                maps.append(tileMap)
                                logger.debug(f"Loaded map module: {mapModule}")
                            except Exception as e:
                                file_path = os.path.abspath(os.path.join(mapsDirectory, folder))
                                logger.error(f"Failed to load scene module {mapModulePath} in file {file_path}: {e}")
                # modulePath = Directory
                # file = importlib.import_module(modulePath)
            except Exception as e:
                logger.error(f"Failed to import scenes.\nException: {e}")
            scenes = tuple(maps)

            return scenes

        areas = []
        maps = getTileMaps()
        areas.append(Area(maps=maps))
        return tuple(areas)

    def run(self, screen):
        self.currentScene.update(screen=screen)