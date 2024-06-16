from debug.logger import logger
from game.Scenes.Area import Area
import os
import pygame
import gamedata.Save.SavedData as SAVED_DATA
from game.Scenes.TitleScreen import TitleScreen
from game.Player import Player
from game.Scenes.BaseScene import SceneStates, Scene
from game.Scenes.PauseMenu import PauseMenu
from debug.DebugMenu import DebugMenu

class SceneHandler:
    def __init__(self, DEBUG= False, display_size=None):
        self.scenes = ()
        self.timeSceneLastChanged = pygame.time.get_ticks() 
        logger.debug(f"Class {SceneHandler=} initializing....")
        self.player = SceneHandler.loadPlayer()
        self.Areas = self.loadTestArea(_player= self.player);
        self.TitleScreen = TitleScreen(background=pygame.image.load(os.getcwd() + '/images/test/titleScreenBackground.png'))
        self.currentScene = self.TitleScreen
        self.currentArea = None
        self.sceneLastChanged = 0
        self.debugMenu = DebugMenu(mode= DEBUG, current_scene = self.currentScene, display_size= display_size)

        logger.debug(f"Class {SceneHandler=} intialized.")

    def getCurrentScene(self): return self.currentScene

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
        return self.Areas[idx]

    def checkSceneState(self, currentScene: Scene, debug: bool, screen):
        if not (currentScene.state == SceneStates.FINISHED or currentScene.state == SceneStates.PAUSED) or currentScene.state == 0 :
            return None
        timenow = pygame.time.get_ticks()
        sceneChangeCooldown = 200
        if timenow - self.timeSceneLastChanged < sceneChangeCooldown:
            return None
        
        self.timeSceneLastChanged = timenow
        if type(currentScene) == PauseMenu:
            ## PAUSE MENU FINISHED ##
            pauseCooldown = self.currentScene.getTimeLastPaused()
            self.currentScene.clear()
            del self.currentScene
            self.currentArea.setTimeLastPaused(pauseCooldown)
            self.currentScene = self.currentArea
            self.currentScene.setState(SceneStates.RUNNING)
            self.currentArea = None
            return None
        if self.currentScene.state == SceneStates.PAUSED:
            pauseMenu = self.loadPauseMenu(screen= screen, time_last_paused = timenow)
            self.currentArea = self.currentScene
            self.currentScene = pauseMenu
            return None
        self.currentScene.clear()
        del self.currentScene 
        logger.debug(f"{currentScene=}")
            
        self.currentScene = self.loadArea(SAVED_DATA.CURRENT_AREA_INDEX)
        if debug:
            self.debugMenu.setCurrentScene(self.currentScene)
            
    def loadPauseMenu(self, screen: pygame.Surface, time_last_paused) -> PauseMenu:
        return PauseMenu(name = "PauseMenu",last_world_frame= screen.copy(), time_last_paused= time_last_paused)
        
        
    def run(self, screen: pygame.Surface):
        self.currentScene.update(screen=screen)
        self.checkSceneState(currentScene=self.currentScene, debug=True, screen= screen)

    def runDebug(self, screen: pygame.Surface, clock: pygame.time.Clock):
        print(f"{self.currentScene=}")
        self.currentScene.update(screen=screen)
        self.debugMenu.run(screen=screen, clock= clock, currentScene= self.currentScene)
        self.checkSceneState(currentScene=self.currentScene, debug=True, screen= screen)

