import pygame
import os
import Font.FontPaths as FONT_PATHS
import globalVars.SettingsConstants as SETTINGS
from game.utils.Button import Button, TextButton, TextAlignments
from game.Scenes.BaseScene import Scene, SceneStates, SceneTypes
class PauseMenu(Scene):
    def __init__(self, name: str, last_world_frame: pygame.Surface, time_last_paused):
        super().__init__(name)
        self.state = SceneStates.INITIALIZING
        self.lastWorldFrame = last_world_frame
        self.blackTransparentLayer = PauseMenu.loadBlackTransparentLayer(size= last_world_frame.get_size(), opacity=0)
        self.timeLastPaused = time_last_paused
        self.transparentLayerOpacity = 0
        self.timeLastAnimated = 0 
        self.state = SceneStates.ON_ANIMATION
        self.pausedFont = PauseMenu.turnStringToFontSurf(string = "PAUSE MENU", font_fp = FONT_PATHS.GOHU, base_size = SETTINGS.TILE_SIZE, anti_aliasing = True) 
        self.pausedFontPos = (SETTINGS.SCREEN_WIDTH/2 - self.pausedFont.get_width() / 2, 0)

        self.buttons = PauseMenu.generateButtons()

    @staticmethod
    def generateButtons() -> list[TextButton]:
        quitButton = TextButton("QUIT", "Quit Button", x= SETTINGS.TILE_SIZE,y=  3 * SETTINGS.SCREEN_HEIGHT / 4, width= 3* SETTINGS.TILE_SIZE, height = 2*SETTINGS.TILE_SIZE, fit_to_text= True)
        settingsButton = TextButton("SETTINGS", "Settings Button", x= SETTINGS.TILE_SIZE, y= 2*SETTINGS.SCREEN_HEIGHT / 4, width = 3*SETTINGS.TILE_SIZE, height = 2 * SETTINGS.TILE_SIZE, fit_to_text= True)
        return [quitButton, settingsButton]

    def disableMouseForButtons(self):
        for button in self.buttons:
            
            button.disableMouse()

    def enableMouseForButtons(self):
        for button in self.buttons:
            button.enableMouse()

    def render(self, screen):
        screen.blit(self.lastWorldFrame, (0,0))
        screen.blit(self.blackTransparentLayer, (0,0))
        screen.blit(self.pausedFont, self.pausedFontPos)
        for button in self.buttons:
            if button.hover: 
                button.animateTextToSize(size= 40, step= 2, shrink= False)
                button.animateTextToColor(color = (200, 200, 200), speed = "medium")
            else:
                if button.fontSize != button.originalFontSize:
                    button.animateTextToSize(size= button.originalFontSize, step= 10, shrink= True)
                if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
            button.update(screen)
            

    @staticmethod
    def turnStringToFontSurf(string: str, font_fp: str, base_size=24,  color= (255,255,255), anti_aliasing = False):        
        return pygame.font.Font(font_fp, base_size).render(string, anti_aliasing, color)


    def animate(self):
        self.animateBackground(opacity= self.transparentLayerOpacity, time_last_animated = self.timeLastAnimated)

    def animateBackground(self, opacity: int, time_last_animated):
        cooldown = 10  # MILISECONDS 
        opacityStep = 5
        maxOpacity = 200
        timenow = pygame.time.get_ticks()
        if timenow - time_last_animated < cooldown:
            return None
        self.timeLastAnimated = timenow
        opacity = self.transparentLayerOpacity
        opacity += opacityStep
        self.blackTransparentLayer = PauseMenu.loadBlackTransparentLayer(size= self.blackTransparentLayer.get_size(), opacity= opacity)
        if opacity >= maxOpacity:
            self.setState(SceneStates.RUNNING)
        self.transparentLayerOpacity = opacity

    def update(self, screen):
        if self.state == SceneStates.ON_ANIMATION:
            self.animate()
        self.checkUnpauseSignal()
        self.render(screen)
   
    @staticmethod
    def loadBlackTransparentLayer(size: tuple, opacity: int):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((0,0,0,opacity))
        return surf

    def getTimeLastPaused(self): return self.timeLastPaused

    def checkUnpauseSignal(self):
        timenow = pygame.time.get_ticks()
        pauseCooldown = 300
        if timenow - self.timeLastPaused < pauseCooldown:
            return None

        pauseKey = pygame.K_x
        keys = pygame.key.get_pressed()
        if keys[pauseKey]:
            self.state = SceneStates.FINISHED
            self.timeLastPaused = timenow    
            self.ptrNextScene = SceneTypes.AREA
    def clear(self):
        pass
