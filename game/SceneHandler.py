from debug.logger import logger
import globalVars.PathConstants as PATH_CONSTANTS
from game.TileMap import TileMap
from game.Scenes.Area import Area
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
            self.scenes = self.loadScenes();
            self.currentScene = self.loadCurrentScene(_type = SAVED_DATA.CURRENT_SCENE_TYPE, index= SAVED_DATA.CURRENT_SCENE_INDEX);
            logger.debug(f"Class {SceneHandler=} intialized.")
        except Exception as e:
            logger.error(f"Failed {SceneHandler=} class initialization.\n Error: {e}")

    def getTitleScreen(self):
        pass

    def loadScenes(self):
        pass

    def loadCurrentScene(self, _type: str, index : int):
        if _type == PATH_CONSTANTS.AREA:
            return Area(map_idx= index)

    def run(self, screen):
        self.currentScene.update(screen=screen)