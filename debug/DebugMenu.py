from debug.logger import logger
import pygame
from game.Scenes.BaseScene import Scene
from game.Scenes.TitleScreen import TitleScreen
from game.Scenes.Area import Area
from game.Scenes.Menu import Menu
from game.Scenes.PauseMenu import PauseMenu
from game.Scenes.Inventory import Inventory
from game.Scenes.Battle import Battle
import Font.FontPaths as FontPaths
import psutil
import os
import platform
class DebugMenu:
    def __init__(self, mode: bool, current_scene: Scene, display_size):
        self.mode = mode
        if not mode: return None
        surf = pygame.Surface((1,1))
        resourceInfoLen = 5
        systemInfoLen = 5
        self.displaySize = display_size
        self.currentResourceInfo = []
        self.systemResourceInfo = []
        for i in range(resourceInfoLen):
            self.currentResourceInfo.append(surf)
        for i in range(systemInfoLen):
            self.systemResourceInfo.append(surf)
        self.timeLastRenderedResourceInfo = 0
        self.currentScene = current_scene
        self.bottomYRight = 0
        self.bottomYLeft = 0
        self.timeDebugLastToggled = 0

    def setCurrentScene(self, scene: Scene):
        self.currentScene = scene

    @staticmethod
    def turnStringToFontSurf(string: str, font_fp: str, base_size=24,  color= (255,255,255)):        
        return pygame.font.Font(font_fp, base_size).render(string, False, color)


    def checkModeChange(self):
        timenow = pygame.time.get_ticks()
        modeSwitchCooldown = 300
        if timenow - self.timeDebugLastToggled < modeSwitchCooldown:
            return None
        toggleDebugKeyId = pygame.K_p
        keys = pygame.key.get_pressed()
        if not keys[toggleDebugKeyId]:
            return None
        self.timeDebugLastToggled = timenow
        self.mode = not self.mode


            
    def run(self, clock: pygame.time.Clock, screen: pygame.Surface, currentScene: Scene):
   
        self.checkModeChange()
        if not self.mode: return None
        self.renderCurrentSceneMenu(clock= clock,screen=screen, current_scene= currentScene)
    
    def renderCurrentSceneMenu(self, clock: pygame.time.Clock, screen: pygame.Surface, current_scene: Scene):
        coolDown = 500
        timenow = pygame.time.get_ticks()

        if timenow - self.timeLastRenderedResourceInfo >= coolDown:
        
            currentFontFp = FontPaths.GOHU
            title = DebugMenu.turnStringToFontSurf(string=f"#### SYSTEM STATISTICS ####", font_fp = currentFontFp)
            sysMemoryUsage = DebugMenu.turnStringToFontSurf(string=f"MEMORY USAGE (%): {round(psutil.virtual_memory().percent, 2)}", font_fp = currentFontFp)
            sysCpuUsage = DebugMenu.turnStringToFontSurf(string=f"CPU USAGE (%): {round(psutil.cpu_percent(), 2)}", font_fp= currentFontFp)
            currentOS = DebugMenu.turnStringToFontSurf(string=f"OPERATING SYSTEM: {platform.system()} {platform.release()}", font_fp = currentFontFp)
            displaySize = DebugMenu.turnStringToFontSurf(string=f"DISPLAY SIZE: {self.displaySize}", font_fp = currentFontFp)
            self.systemResourceInfo[0] = title
            self.systemResourceInfo[1] = sysMemoryUsage
            self.systemResourceInfo[2] = sysCpuUsage
            self.systemResourceInfo[3] = currentOS
            self.systemResourceInfo[4] = displaySize
            # process specific
            process = psutil.Process(os.getpid())
            processTitleFont = DebugMenu.turnStringToFontSurf(string="#### PROCESS STATISTICS ####", font_fp=currentFontFp)
            processNameFont = DebugMenu.turnStringToFontSurf(string= f"PROCESS NAME: {process.name()}",font_fp= currentFontFp)
            fpsFont = DebugMenu.turnStringToFontSurf(string= f"FPS: {int(clock.get_fps())}", font_fp=currentFontFp)
            timeFont = DebugMenu.turnStringToFontSurf(string= f"TIME BETWEEN FRAMES (ms): {int(clock.get_time())}", font_fp = currentFontFp)
            memoryUsage = DebugMenu.turnStringToFontSurf(string= f"MEMORY USAGE (%):{round(process.memory_percent(), 2)}", font_fp = currentFontFp) 
            self.currentResourceInfo[0] = processTitleFont
            self.currentResourceInfo[1] = fpsFont
            self.currentResourceInfo[2] = timeFont
            self.currentResourceInfo[3] = memoryUsage
            self.currentResourceInfo[4] = processNameFont
            self.timeLastRenderedResourceInfo = timenow

        self.blitDebugInfoFromList(screen= screen, startingPoint= [0,0], info=
                                        self.systemResourceInfo, padding = (0, 0), direction= (0, -1), allignRight=False)

        self.blitDebugInfoFromList(screen=screen, startingPoint= [screen.get_width(), 0], info= self.currentResourceInfo, padding = (0, 0), direction = (0,-1), allignRight=True)
        #currentY = 0
        
        #for resource in self.currentResourceInfo:
        #    screen.blit(resource, (screen.get_width() - resource.get_width(), currentY))
        #    currentY += resource.get_height()
        try:
            DebugMenu.renderCurrentSceneDebug(screen= screen, currentScene = self.currentScene, startingPoint = [0, self.bottomYRight])
        except Exception as e:
            logger.error({e})
            return None
    @staticmethod
    def blitErrorMsg(error_msg: str, screen: pygame.Surface):
        font = FontPaths.GOHU
        # default error message position is bottom left of screen
        errorMsgSurf =DebugMenu.turnStringToFontSurf(string= error_msg, font_fp= font)
        screen.blit(errorMsgSurf, (0, screen.get_height() + errorMsgSurf.get_height()))
    
    def blitDebugInfoFromList(self,screen: pygame.Surface, startingPoint: list[int], info: list[pygame.Surface], padding: tuple[int, int], direction: tuple[int, int],
                              allignRight=True):
        if len(startingPoint) != 2: 
            DebugMenu.blitErrorMsg(error_msg=f"argument for startingPoint is {len(startingPoint)} != 2",  screen= screen)
        for piece in info: 
            if allignRight and direction[0] == 0:
                screen.blit(piece, (startingPoint[0] - piece.get_width(), startingPoint[1] ))
            else:
                screen.blit(piece, (startingPoint[0], startingPoint[1]))
            if direction[0] == 1:
                startingPoint[0] += piece.get_width()
            elif direction[0] == -1:
                startingPoint[0] -= piece.get_width()

            if direction[1] == 1:
                startingPoint[1] -= piece.get_height()
            elif direction[1] == -1:
                startingPoint[1] += piece.get_height()

        if allignRight: self.bottomYRight = startingPoint[1]
        else: self.bottomYLeft = startingPoint[1]

    @staticmethod
    def renderCurrentSceneDebug(screen: pygame.Surface, currentScene: Scene, startingPoint: list[int]):
        fontFp = FontPaths.GOHU
        sceneType = "SCENE TYPE: "
        surfaceList = []
        surfaceList.append("#### SCENE INFO ####")
        surfaceList.append(f"STATE: {currentScene.getState()}")
        if type(currentScene) == Area:
            surfaceList.append(sceneType + "AREA")
            surfaceList.append(f"CURRENT MAP ID: {currentScene.getCurrentMapId()}")
            player = currentScene.getPlayer()
            surfaceList.append(f"PLAYER MOVEMENT STATE: {player.getMovementState()}")
            surfaceList.append(f"PLAYER MOVEMENT DIRECTION: {player.getMovementDirection()}")
            surfaceList.append(f"PLAYER FACING DIRECTION: {player.getFacingDirection()}")
            surfaceList.append(f"PLAYER INPUT STTE: {player.getInputState()}")
        elif type(currentScene) == TitleScreen:
            surfaceList.append(sceneType + "TITLESCREEN")
        elif isinstance(currentScene, Menu):
            surfaceList.append(sceneType + f"{type(currentScene)}")
            logger.debug(f"{currentScene.selectedButtonIdx=}")
            surfaceList.append(f"UI LOCK: {currentScene.uiLock}")
            surfaceList.append(f"SELECTION MODE: {currentScene.selectionMode}")
            surfaceList.append(f"SELECTED BUTTON IDX: {currentScene.selectedButtonIdx}")
            surfaceList.append(f"SELECTED MAIN BUTTON IDX: {currentScene.selectedMainButtonIdx}")
            surfaceList.append(f"SELECTED OTHER BUTTON IDX: {currentScene.selectedOtherButtonIdx}")

            if type(currentScene) == Inventory:
                surfaceList.append(f"LAST SELECTED BUTTON IDX: {currentScene.lastSelectedButtonIdx}")
                surfaceList.append(f"buttonPressedName: {currentScene.buttonPressedName}")
        elif type(currentScene) == Battle:
            surfaceList.append(f"CURRENT BUTTON IDX: {currentScene.currentButtonIdx}")
            surfaceList.append(f"BUTTON INDICES: {currentScene.buttonIndices}")
            surfaceList.append(f"CURRENT BUTTON MENU: {currentScene.currentButtonMenu}")
            surfaceList.append(f"UI LOCK: {currentScene.uiLock}")
            surfaceList.append(f"BUTTON PRESSED NAME: {currentScene.buttonPressedName}")
            buttonNames = "["
            buttonPositions = "["
            buttonLerping = "["
            for button in currentScene.currentButtons:
                buttonNames = buttonNames + button.name
                buttonPositions+= f"{(button.rect.x, button.rect.y)}"
                buttonLerping += str(button.textAnimationInfo.getLerpXY())
                buttonNames += ', '
                buttonPositions += ", "
                buttonLerping += ", "
            buttonNames += ']'
            buttonPositions += "]"
            buttonLerping += "]"
            surfaceList.append(f"BUTTON NAMES: {buttonNames}")
            surfaceList.append(f"BUTTON POSITIONS: {buttonPositions}")
            surfaceList.append(f"BUTTON LERPING: {buttonLerping}")
            surfaceList.append(f"BUTTON INDICES: {currentScene.buttonIndices}")
        for surface in surfaceList:
            surface = DebugMenu.turnStringToFontSurf(string= surface, font_fp = fontFp)
            screen.blit(surface, (startingPoint[0], startingPoint[1]))
            startingPoint[1] += surface.get_height()

