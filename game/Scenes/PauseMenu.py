import pygame
import os
import Font.FontPaths as FONT_PATHS
import globalVars.SettingsConstants as SETTINGS
import gamedata.Save.SavedData as SAVED_DATA
from game.utils.Button import Button, TextButton, TextAlignments
from game.Scenes.BaseScene import Scene, SceneStates, SceneTypes
class PauseMenu(Scene):
    availableSelectionModes = ("NONE", "MOUSE", "KEYBOARD" )
    MAX_SELECTED_BUTTON_IDX = 1
    def __init__(self, name: str, last_world_frame: pygame.Surface, time_last_paused):
        super().__init__(name)
        self.state = SceneStates.INITIALIZING
        self.lastWorldFrame = last_world_frame
        self.blackTransparentLayer = PauseMenu.loadBlackTransparentLayer(size= last_world_frame.get_size(), opacity=0)
        self.timeLastPaused = time_last_paused
        self.transparentLayerOpacity = 0
        self.timeLastAnimated = 0 
        self.state = SceneStates.ON_ANIMATION
        self.pausedFont = PauseMenu.turnStringToFontSurf(string = "PAUSE MENU", font_fp = FONT_PATHS.GOHU, base_size = SETTINGS.TILE_SIZE, anti_aliasing = True, color= (75, 0, 130)) 
        self.pausedFontPos = (SETTINGS.SCREEN_WIDTH/2 - self.pausedFont.get_width() / 2, 0)
        self.pausedFontOutline = PauseMenu.turnStringToFontSurf(string= "PAUSE MENU", font_fp = FONT_PATHS.GOHU, base_size = SETTINGS.TILE_SIZE, anti_aliasing= True, color=(186, 85, 211))
        self.timeLastUIKeystroke = 0
        self.lastMousePosition = self.mousePos = pygame.mouse.get_pos()
        self.buttons = PauseMenu.generateButtons()
        self.selectedButtonIdx = 0
        self.selectionMode = PauseMenu.availableSelectionModes[0] 


    @staticmethod
    def generateButtons() -> list[TextButton]:
        quitButton = TextButton("QUIT", "Quit Button", x= SETTINGS.TILE_SIZE,y=  3 * SETTINGS.SCREEN_HEIGHT / 4, width= 3* SETTINGS.TILE_SIZE, height = 2*SETTINGS.TILE_SIZE, fit_to_text= True, color= (136,8,8))
        settingsButton = TextButton("SETTINGS", "Settings Button", x= SETTINGS.TILE_SIZE, y= 2*SETTINGS.SCREEN_HEIGHT / 4, width = 3*SETTINGS.TILE_SIZE, height = 2 * SETTINGS.TILE_SIZE, fit_to_text= True, color= (20,52,164))
        settingsButton.animateTextWithOutline(color=(0, 150, 255))
        quitButton.animateTextWithOutline(color=(255, 0, 0))
        return [settingsButton,quitButton]

    def disableMouseForButtons(self):
        for button in self.buttons:
            
            button.disableMouse()

    def enableMouseForButtons(self):
        for button in self.buttons:
            button.enableMouse()

    ### button selection and animation logic for pause menu here for less for loops ###
    def render(self, screen):
        screen.blit(self.lastWorldFrame, (0,0))
        screen.blit(self.blackTransparentLayer, (0,0))
        screen.blit(self.pausedFontOutline, (self.pausedFontPos[0] - 2, self.pausedFontPos[1])) 
        screen.blit(self.pausedFontOutline, (self.pausedFontPos[0] + 2, self.pausedFontPos[1])) 
        screen.blit(self.pausedFontOutline, (self.pausedFontPos[0], self.pausedFontPos[1] - 2))
        screen.blit(self.pausedFontOutline, (self.pausedFontPos[0], self.pausedFontPos[1] + 2)) 
        screen.blit(self.pausedFont, self.pausedFontPos)
        self.renderButtons(self.buttons, screen)
           
    def renderButtons(self, buttons, screen):
        
        hoveringOnButton = False
        mousePosition = pygame.mouse.get_pos()
        if self.lastMousePosition != mousePosition:
            self.selectionMode = "MOUSE"
            self.lastMousePosition = mousePosition
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        if keys[SAVED_DATA.UI_MOVE_UP] or keys[SAVED_DATA.UI_MOVE_DOWN] or keys[SAVED_DATA.UI_MOVE_LEFT] or keys[SAVED_DATA.UI_MOVE_RIGHT]:
            self.selectionMode = "KEYBOARD"

        for index, button in enumerate(buttons):
            if not button.hover:
                button.setSelected(False)
                continue
            hoveringOnButton = True
            if self.selectionMode == "MOUSE":
                self.selectedButtonIdx = index
                buttons[self.selectedButtonIdx].setSelected(True)

        if self.selectionMode == "KEYBOARD":
            buttons[self.selectedButtonIdx].setSelected(False)
            selectStep = 0
            cooldown = 150
            if timenow - self.timeLastUIKeystroke >= cooldown:
            
                if keys[SAVED_DATA.UI_MOVE_UP]:
                    selectStep = 1
                    self.timeLastUIKeystroke = timenow        
                elif keys[SAVED_DATA.UI_MOVE_DOWN]:
                    selectStep = -1 
                    self.timeLastUIKeystroke = timenow        
                elif keys[SAVED_DATA.UI_MOVE_RIGHT]:
                    selectStep = 1
                    self.timeLastUIKeystroke = timenow        
                elif keys[SAVED_DATA.UI_MOVE_LEFT]:
                    selectStep = -1
                
                    self.timeLastUIKeystroke = timenow        
                if self.selectedButtonIdx + selectStep < 0:
                    self.selectedButtonIdx = PauseMenu.MAX_SELECTED_BUTTON_IDX
                elif self.selectedButtonIdx + selectStep > PauseMenu.MAX_SELECTED_BUTTON_IDX:
                    self.selectedButtonIdx = 0
                else:
                    self.selectedButtonIdx += selectStep
                
            buttons[self.selectedButtonIdx].setSelected(True)


        for button in buttons:
            if button.selected:
                button.animateTextToSize(size= 40, step= 3, shrink= False)
                button.animateTextToColor(color = (button.originalTextColor[0] - 30, button.originalTextColor[1] - 30, button.originalTextColor[2] - 30), speed = "medium")
                button.animateTextWithOutline()               
            else:
                if button.fontSize != button.originalFontSize:

                    button.animateTextToSize(size= button.originalFontSize, step= 10, shrink= True)
                if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
                if button.outlineColor != button.originalOutlineColor: button.animateTextWithOutline(color=button.originalOutlineColor)                
            button.update(screen)

        
        print(f"{self.selectionMode=}")
        print(f"{self.selectedButtonIdx=}")
        '''
        for index, button in enumerate(buttons):
            
            if button.hover: 
                hoveringOnButton = True
                self.selectedButtonIdx = index 
                button.animateTextToSize(size= 40, step= 3, shrink= False)
                button.animateTextToColor(color = (button.originalTextColor[0] - 30, button.originalTextColor[1] - 30, button.originalTextColor[2] - 30), speed = "medium")
                button.animateTextWithOutline()
            else:
                if button.fontSize != button.originalFontSize:

                    button.animateTextToSize(size= button.originalFontSize, step= 10, shrink= True)
                if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
                if button.outlineColor != button.originalOutlineColor: button.animateTextWithOutline(color=button.originalOutlineColor)                
            button.update(screen)
        ''' 
        
        mousePressed = pygame.mouse.get_pressed()
        if not hoveringOnButton and (mousePressed[0] or mousePressed[1] or mousePressed[2]):
            self.selectionMode = "NONE"
        
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
