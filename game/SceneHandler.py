from debug.logger import logger
import globalVars.PathConstants as PATH_CONSTANTS
from game.TileMap import TileMap
from game.Scenes.Area import Area
import os
import importlib
import pygame
import gamedata.Save.SavedData as SAVED_DATA
from game.Scenes.TitleScreen import TitleScreen
import globalVars.SceneConstants as SCENE_CONSTANTS
from game.Player import Player

class SceneHandler:
    def __init__(self, _player : Player):
        self.scenes = ()
        self.Areas = None
        self.player = None
        self.currentScene = None

        self.currentSceneIndex = 0
        self.SCENE_COUNT = 0
        self.timeLastChangedScene = pygame.time.get_ticks()
        self.TitleScreen = None
        try:
            logger.debug(f"Class {SceneHandler=} initializing....")
            self.Areas = self.loadAreas(_player= _player);
            self.player = _player
            self.TitleScreen = TitleScreen(background=pygame.image.load(os.getcwd() + '/images/test/titleScreenBackground.png'))
            self.currentScene = self.TitleScreen
            logger.debug(f"Class {SceneHandler=} intialized.")
        except Exception as e:
            logger.error(f"Failed {SceneHandler=} class initialization.\n Error: {e}")


    def loadAreas(self, _player) -> list[Area]:
        logger.info(f"Loading Areas........")
        areas = []
        try:
            pass
            # Code that loads areas
        except Exception as e:
            logger.error(f"Failed to load areas. Error: {e}")

        logger.info(f"Loaded all Areas.")

        # areas.append(Area(name="test", map_idx=0))
        return [Area(name="test", map_idx=0, _player= _player)]

    def loadArea(self, idx : int) -> Area:
        return self.Areas[idx];

    def loadCurrentScene(self, _type: str, index : int):
        if _type == PATH_CONSTANTS.AREA:
            return Area(map_idx= index, name="Test")
        elif _type == PATH_CONSTANTS.TITLE_SCREEN:
            return self.TitleScreen

    def checkSceneState(self, currentScene):
        if not currentScene.state == SCENE_CONSTANTS.STATE_FINISHED:
            return None
        self.currentScene = 0
        logger.debug(f"{currentScene=}")
        self.currentScene = self.loadArea(SAVED_DATA.CURRENT_AREA_INDEX)

    def run(self, screen):
        self.checkSceneState(currentScene=self.currentScene);
        self.currentScene.update(screen=screen)
