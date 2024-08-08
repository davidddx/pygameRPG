from debug.logger import logger
from game.Scenes.Area import Area
import os
import pygame
import gamedata.Save.SavedData as SAVED_DATA
from game.Scenes.TitleScreen import TitleScreen
from game.Scenes.Inventory import Inventory
from game.Player import Player
from game.Scenes.BaseScene import SceneStates, Scene, SceneTypes
from game.Scenes.PauseMenu import PauseMenu
from game.Scenes.Settings import Settings
from debug.DebugMenu import DebugMenu

class SceneHandler:
    def __init__(self, DEBUG= False, display_size=None):
        self.scenes = ()
        self.finished = False
        self.timeSceneLastChanged = pygame.time.get_ticks() 
        logger.debug(f"Class {SceneHandler=} initializing....")
        self.player = SceneHandler.loadPlayer()
        self.Areas = self.loadTestArea(_player= self.player);
        self.TitleScreen = TitleScreen(background=pygame.image.load(os.getcwd() + '/images/test/titleScreenBackground.png'))
        self.currentScene = self.TitleScreen
        self.currentArea = None
        self.sceneLastChanged = 0
        self.debugMenu = DebugMenu(mode= DEBUG, current_scene = self.currentScene, display_size= display_size)
        self.lastAreaFrame = None
        self.lastSceneFrame = None
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
    '''
    def checkSceneState(self, currentScene: Scene, debug: bool, screen):
        if not (currentScene.state == SceneStates.FINISHED or currentScene.state == SceneStates.PAUSED) or currentScene.state == 0 :
            if not currentScene.state == SceneStates.QUIT_GAME:
                return None
            self.finished = True
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
    ''' 

    def checkSceneStateTest(self, current_scene : Scene, screen, debug=False):
        if current_scene.state == SceneStates.INITIALIZING or current_scene.state == SceneStates.RUNNING or current_scene.state == SceneStates.ON_ANIMATION or current_scene.state == SceneStates.FINISHING:
            return None
        if current_scene.state == SceneStates.QUIT_GAME:
            self.finished = True
            logger.info("Game Process Finished. Closing....")
            return None
        timenow = pygame.time.get_ticks()
        sceneChangeCooldown = 200
        if timenow - self.timeSceneLastChanged < sceneChangeCooldown:
            return None
        self.timeSceneLastChanged = timenow
        nextScenePtr = current_scene.getPtrNextScene()
        self.lastSceneFrame = pygame.Surface(screen.get_size(), pygame.SRCALPHA) 
        self.lastSceneFrame.blit(screen.copy(), (0,0))
        if type(current_scene) == Area: self.lastAreaFrame = screen.copy()
        nextScene = self.loadNextScene(current_scene= current_scene, next_scene_ptr= nextScenePtr, screen= screen, timenow= timenow)
        # Case where pausing area
        if type(current_scene) == Area: 
            if nextScenePtr == SceneTypes.PAUSE_MENU:
                self.currentArea = self.currentScene
                
                self.currentScene = nextScene 
                if debug: self.debugMenu.setCurrentScene(self.currentScene)

                return None               

        # Case where pause menu switches to area  
        if type(current_scene) == PauseMenu and nextScenePtr == SceneTypes.AREA:
            pauseCooldown = self.currentScene.getTimeLastPaused()
            self.currentArea.setTimeLastPaused(pauseCooldown)
            self.currentScene = self.currentArea
            self.currentScene.setState(SceneStates.RUNNING)
            self.currentArea = None
            if debug: self.debugMenu.setCurrentScene(self.currentScene)
            return None

        ## Finished edge cases
        current_scene.clear()
        del current_scene
        current_scene = nextScene
        self.currentScene = current_scene
        logger.debug(f"{current_scene=}") 
        if debug: self.debugMenu.setCurrentScene(current_scene)

    def loadNextScene(self, current_scene: Scene, next_scene_ptr: str, screen, timenow):
        match next_scene_ptr:
            case SceneTypes.PAUSE_MENU: 
                if type(current_scene) == Area:
                    return self.loadPauseMenu(screen, timenow, fade_in= True, selected_button_idx= [0,0])
                elif type(current_scene) == Settings:
                    return self.loadPauseMenu(screen, timenow, fade_in = False, selected_button_idx = [0,1], selection_mode = "KEYBOARD")
                return self.loadPauseMenu(screen, timenow)
            case SceneTypes.SETTINGS: return self.loadSettings(screen.get_size(), self.lastSceneFrame)
            case SceneTypes.INVENTORY: return Inventory(self.lastAreaFrame, self.lastSceneFrame)
            case SceneTypes.AREA: return self.loadArea(SAVED_DATA.CURRENT_AREA_INDEX) 

    def loadSettings(self, screen_size, last_pause_menu_frame: pygame.Surface):
        return Settings(self.lastSceneFrame, self.lastAreaFrame, screen_size)

    def loadPauseMenu(self, screen: pygame.Surface, time_last_paused, fade_in=False, selected_button_idx = [-1,-1], selection_mode = "NONE") -> PauseMenu:
        return PauseMenu(name = "PauseMenu",last_world_frame= self.lastAreaFrame, time_last_paused= time_last_paused, fade_in= fade_in, selected_button_idx = selected_button_idx, selection_mode = selection_mode)
        
        
    def logSceneInfo(self, current_scene : Scene):
        logger.debug(f"Current Scene State: {current_scene.state=}")
        logger.debug(f"Current Scene Name: {current_scene.name=}")
        logger.debug(f"Current Scene PtrNextScene: {current_scene.ptrNextScene=}")

    def run(self, screen: pygame.Surface):
        self.currentScene.update(screen=screen)
        self.checkSceneState(currentScene=self.currentScene, debug=True, screen= screen)

    def runDebug(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.currentScene.update(screen=screen)
        self.debugMenu.run(screen=screen, clock= clock, currentScene= self.currentScene)
        self.checkSceneStateTest(current_scene=self.currentScene, debug=True, screen= screen)
        self.logSceneInfo(self.currentScene)
