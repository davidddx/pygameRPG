from debug.logger import logger
from game.Scenes.Area import Area
import os
import pygame
import importlib
import gamedata.Save.SavedData as SAVED_DATA
from game.Scenes.TitleScreen import TitleScreen
import globalVars.SceneConstants as SCENE_CONSTANTS
from game.Player import Player, PlayerPart

class SceneHandler:
    def __init__(self):
        self.scenes = ()
        self.timeLastChangedScene = pygame.time.get_ticks() 
        logger.debug(f"Class {SceneHandler=} initializing....")
        self.player = SceneHandler.loadPlayer()
        self.Areas = self.loadTestArea(_player= self.player);
        self.TitleScreen = TitleScreen(background=pygame.image.load(os.getcwd() + '/images/test/titleScreenBackground.png'))
        self.currentScene = self.TitleScreen
        logger.debug(f"Class {SceneHandler=} intialized.")

    @staticmethod
    def loadPlayer() -> Player:
        cwd = os.getcwd()
        playerSpriteDir = cwd + "/images/test/PlrSpriteTest/AnimationTesting/Parts"
        playerDirectionDirs = {
            Player.FACING_FRONT_ID: playerSpriteDir + "/Front",
            Player.FACING_FRONT_RIGHT_ID: playerSpriteDir + "/FrontRight",
            Player.FACING_SIDE_RIGHT_ID: playerSpriteDir + "/Right",
            Player.FACING_BACK_RIGHT_ID: playerSpriteDir + "/BackRight",
            Player.FACING_BACK_ID: playerSpriteDir + "/Back",
            Player.FACING_BACK_LEFT_ID: playerSpriteDir + "/BackLeft",
            Player.FACING_SIDE_LEFT_ID: playerSpriteDir + "/Left",
            Player.FACING_FRONT_LEFT_ID: playerSpriteDir + "/FrontLeft"
                }
        return Player(pos = SAVED_DATA.PLAYER_POSITION, plr_parts_path = playerSpriteDir, plr_direction_path =
                      playerDirectionDirs) 

    def loadTestArea(self, _player) -> list[Area]:
        logger.info(f"Loading Test Area....")
        return [Area(name = "test", starting_map_idx=SAVED_DATA.CURRENT_MAP_INDEX, _player=_player)]

    def loadAreas(self, _player) -> list[Area]:
        logger.info(f"Loading Areas........")
        areas = []
        cwd = os.getcwd()
        try:
            areaDir = f"{cwd}/gamedata/Areas"
            # Code that loads areas
        except Exception as e:
            logger.error(f"Failed to load areas. error: {e}")

        logger.info(f"Loaded all Areas.")

        # areas.append(Area(name="test", starting_map_idx=0))
        return [Area(name="test", starting_map_idx=0, _player= _player)]

    def loadArea(self, idx : int) -> Area:
        return self.Areas[idx];

    def checkSceneState(self, currentScene):
        if not currentScene.state == SCENE_CONSTANTS.STATE_FINISHED:
            return None
        del self.currentScene 
        logger.debug(f"{currentScene=}")
        self.currentScene = self.loadArea(SAVED_DATA.CURRENT_AREA_INDEX)

    def run(self, screen):
        self.checkSceneState(currentScene=self.currentScene);
        self.currentScene.update(screen=screen)
