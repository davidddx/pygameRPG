from debug.logger import logger
import pygame
from game.Scenes.BaseScene import Scene
from game.Scenes.TitleScreen import TitleScreen
from game.Scenes.Area import Area
import Font.FontPaths as FontPaths
import psutil
import os
import platform
class DebugMenu:
    def __init__(self, mode: bool):
        self.mode = mode
        if not mode: return None
        surf = pygame.Surface((1,1))
        resourceInfoLen = 5
        systemInfoLen = 4
        self.currentResourceInfo = []
        self.systemResourceInfo = []
        for i in range(resourceInfoLen):
            self.currentResourceInfo.append(surf)
        for i in range(systemInfoLen):
            self.systemResourceInfo.append(surf)
        self.timeLastRenderedResourceInfo = 0

    @staticmethod
    def turnStringToFontSurf(scale: int, string: str, font_fp: str, base_size=24,  color= (255,255,255)):        
        return pygame.font.Font(font_fp, base_size * scale).render(string, False, color)

    def run(self, clock: pygame.time.Clock, screen: pygame.Surface, scale: int, currentScene: Scene):
        if not self.mode: return None
        self.renderCurrentSceneMenu(clock= clock, scale= scale, screen=screen, current_scene= currentScene)
    
    
    def renderCurrentSceneMenu(self, clock: pygame.time.Clock, scale: int, screen: pygame.Surface, current_scene: Scene):
        coolDown = 500
        timenow = pygame.time.get_ticks()

        if timenow - self.timeLastRenderedResourceInfo >= coolDown:
        
            currentFontFp = FontPaths.GOHU
            title = DebugMenu.turnStringToFontSurf(scale= scale, string=f"#### SYSTEM STATISTICS ####", font_fp = currentFontFp)
            sysMemoryUsage = DebugMenu.turnStringToFontSurf(scale= scale,
                                                            string=f"MEMORY USAGE (%): {round(psutil.virtual_memory().percent, 2)}", font_fp =
                                                            currentFontFp)
            sysCpuUsage = DebugMenu.turnStringToFontSurf(scale= scale, 
                                                         string=f"CPU USAGE (%): {round(psutil.cpu_percent(), 2)}",
                                                         font_fp= currentFontFp)
            currentOs = DebugMenu.turnStringToFontSurf(scale= scale, string=f"OPERATING SYSTEM: {platform.system()} {platform.release()}", font_fp = currentFontFp)
            self.systemResourceInfo[0] = title
            self.systemResourceInfo[1] = sysMemoryUsage
            self.systemResourceInfo[2] = sysCpuUsage
            self.systemResourceInfo[3] = currentOs
            # process specific
            process = psutil.Process(os.getpid())
            processTitleFont = DebugMenu.turnStringToFontSurf(scale= scale, string="#### PROCESS STATISTICS ####", font_fp=
                                                              currentFontFp)
            processNameFont = DebugMenu.turnStringToFontSurf(scale= scale, string= f"PROCESS NAME: {process.name()}",
                                                             font_fp= currentFontFp)
            fpsFont = DebugMenu.turnStringToFontSurf(scale= scale, string= f"FPS: {int(clock.get_fps())}", font_fp=
                                                 currentFontFp)
            timeFont = DebugMenu.turnStringToFontSurf(scale= scale, string= f"TIME BETWEEN FRAMES (ms): {int(clock.get_time())}", font_fp = currentFontFp)
            memoryUsage = DebugMenu.turnStringToFontSurf(scale = scale, string= f"MEMORY USAGE (%):{round(process.memory_percent(), 2)}", font_fp = currentFontFp) 
            self.currentResourceInfo[0] = processTitleFont
            self.currentResourceInfo[1] = fpsFont
            self.currentResourceInfo[2] = timeFont
            self.currentResourceInfo[3] = memoryUsage
            self.currentResourceInfo[4] = processNameFont
            self.timeLastRenderedResourceInfo = timenow

        DebugMenu.blitDebugInfoFromList(screen= screen, scale= scale, startingPoint= [0,0], info=
                                        self.systemResourceInfo, padding = (0, 0), direction= (0, -1), allignRight=False)

        DebugMenu.blitDebugInfoFromList(screen=screen, scale= scale, startingPoint= [screen.get_width(), 0], info= self.currentResourceInfo, padding = (0, 0), direction = (0,-1), allignRight=True)
        #currentY = 0
        
        #for resource in self.currentResourceInfo:
        #    screen.blit(resource, (screen.get_width() - resource.get_width(), currentY))
        #    currentY += resource.get_height()

        if type(current_scene) == TitleScreen:
            pass 
        elif type(current_scene) == Area:
            pass
        else:
            pass
    @staticmethod
    def blitErrorMsg(error_msg: str, scale: int, screen: pygame.Surface):
        font = FontPaths.GOHU
        # default error message position is bottom left of screen
        errorMsgSurf =DebugMenu.turnStringToFontSurf(scale= scale, string= error_msg, font_fp= font)
        screen.blit(errorMsgSurf, (0, screen.get_height() + errorMsgSurf.get_height()))
    
    @staticmethod
    def blitDebugInfoFromList(screen: pygame.Surface, scale:int, startingPoint: list[int], 
                              info: list[pygame.Surface], padding: tuple[int, int], direction: tuple[int, int],
                              allignRight=True):
        if len(startingPoint) != 2: 
            DebugMenu.blitErrorMsg(error_msg=
        f"argument for startingPoint is {len(startingPoint)} != 2", scale= scale, screen= screen)
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
            

