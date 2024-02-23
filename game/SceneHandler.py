from debug.logger import logger
import globalVars.PathConstants as PATH_CONSTANTS
from game.utils.TileMap import TileMap
from game.Level import Level
import os
import importlib
class SceneHandler:
    def __init__(self):
        self.scenes = ()
        self.currentLevel = None
        try:
            logger.debug(f"Class {SceneHandler=} initializing....")
            self.Levels = self.getLevels()
            self.currentLevel = self.Levels[0]
            logger.debug(f"Class {SceneHandler=} intialized.")
        except Exception as e:
            logger.error(f"Failed {SceneHandler=} class initialization.\n Error: {e}")

    def getLevels(self):
        levels = []
        maps = self.getMaps()
        for map in maps:
            levels.append(Level(map=map))
        return tuple(levels)
    def getMaps(self):
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

    def changeSceneToNext(self):
        pass
    def changeSceneToPrevious(self):
        pass
    def changeSceneByName(self, scene_name):
        pass
    def run(self, screen):
        self.currentLevel.update(screen=screen)