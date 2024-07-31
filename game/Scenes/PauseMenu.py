import pygame

import os
import Font.FontPaths as FONT_PATHS
import globalVars.SettingsConstants as SETTINGS
import gamedata.Save.SavedData as SAVED_DATA
from game.utils.Button import Button, TextButton, TextAlignments
from game.Scenes.BaseScene import Scene, SceneStates, SceneTypes
from game.Scenes.Menu import Menu

class PauseMenu(Menu):
    def __init__(self, name: str, last_world_frame: pygame.Surface, time_last_paused, fade_in=True, selected_button_idx=(0,0), selection_mode = "NONE"):
        super().__init__(name, last_world_frame, PauseMenu.loadButtons(), fade_in, 0, selected_button_idx = selected_button_idx, selection_mode = selection_mode)
        self.timeLastPaused = time_last_paused
        self.maxSelectedButtonIdx = [0,1]
        self.pausedFontOutline = self.turnStringToFontSurf(string= "PAUSE MENU", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing= True, color=(186, 85, 211))
        self.pausedFont = self.turnStringToFontSurf(string = "PAUSE MENU", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing = True, color= (75, 0, 130)) 
        self.pausedFontPos = (SETTINGS.SCREEN_WIDTH/2 - self.pausedFont.get_width() / 2, 0)
        pausedFontPos = (SETTINGS.SCREEN_WIDTH/2 - self.pausedFont.get_width()/2, 0)
        self.addSurface(self.pausedFontOutline, (pausedFontPos[0], pausedFontPos[1] + 2))
        self.addSurface(self.pausedFontOutline, (pausedFontPos[0] - 2, pausedFontPos[1]))
        self.addSurface(self.pausedFontOutline, (pausedFontPos[0] + 2, pausedFontPos[1]))
        self.addSurface(self.pausedFontOutline, (pausedFontPos[0], pausedFontPos[1] - 2))
        self.addSurface(self.pausedFont, pausedFontPos)

    @staticmethod
    def loadButtons() -> list[list[TextButton]]:
        
        quitButton = TextButton("QUIT", "QUIT", x= 6 * SETTINGS.TILE_SIZE,y=  3 * SETTINGS.SCREEN_HEIGHT / 4, width= 3* SETTINGS.TILE_SIZE, height = 2*SETTINGS.TILE_SIZE, fit_to_text= True, color= (136,8,8), font_path = SAVED_DATA.FONT_PATH)
        settingsButton = TextButton("SETTINGS", SceneTypes.SETTINGS, x= SETTINGS.TILE_SIZE, y= 2*SETTINGS.SCREEN_HEIGHT / 4, width = 3*SETTINGS.TILE_SIZE, height = 2 * SETTINGS.TILE_SIZE, fit_to_text= True, color= (20,52,164), font_path = SAVED_DATA.FONT_PATH)
        inventoryButton = TextButton("INVENTORY", "INVENTORY", x= SETTINGS.TILE_SIZE, y = SETTINGS.SCREEN_HEIGHT/4, width = 3 * SETTINGS.TILE_SIZE, height = SETTINGS.TILE_SIZE, fit_to_text=True, color = (8,100,10), font_path = SAVED_DATA.FONT_PATH)

        backButton = TextButton("UNPAUSE", "UNPAUSE", x = SETTINGS.TILE_SIZE, y= 3*SETTINGS.SCREEN_HEIGHT/4, width=3, height=3, fit_to_text=True, color = (75, 0, 130), font_path = SAVED_DATA.FONT_PATH)
        settingsButton.animateTextWithOutline(color=(0, 150, 255))
        backButton.animateTextWithOutline(color=(186, 85, 211))
        quitButton.animateTextWithOutline(color=(255, 0, 0))
        inventoryButton.animateTextWithOutline(color = (0, 200,0))


        return [[inventoryButton, settingsButton, backButton], [quitButton]]

    def getTimeLastPaused(self): return self.timeLastPaused

    def checkUnpauseSignal(self):
        if self.state != SceneStates.RUNNING: return None 
        timenow = pygame.time.get_ticks()
        pauseCooldown = 300
        if timenow - self.timeLastPaused <= pauseCooldown:
            return None
        pauseKey = pygame.K_x
        keys = pygame.key.get_pressed()
        if keys[pauseKey]:
            for column in self.mainButtons:
                for button in column:
                    button.setSelected(False)
                    button.setPressed(False)
                    button.disableMouse()
            self.uiLock = True
            self.state = SceneStates.FINISHING
            self.timeLastPaused = timenow    
            self.ptrNextScene = SceneTypes.AREA
            self.animation = Menu.animations[2]

    def checkButtonPressed(self, name: str):
        if name == "NONE": return None
        match name:
            case SceneTypes.SETTINGS:
                self.state=SceneStates.FINISHED
                self.ptrNextScene = SceneTypes.SETTINGS
            case SceneTypes.INVENTORY:
                self.state = SceneStates.FINISHED
                self.ptrNextScene = SceneTypes.INVENTORY

            case "UNPAUSE":
                timenow = pygame.time.get_ticks()
                pauseCooldown = 300
                if timenow - self.timeLastPaused <= pauseCooldown:
                    return None
                for column in self.mainButtons:
                    for button in column:
                        button.setSelected(False)
                        button.setPressed(False)
                        button.disableMouse()
                self.uiLock = True
                self.state = SceneStates.FINISHING
                self.timeLastPaused = timenow   
                self.ptrNextScene = SceneTypes.AREA
                self.animation = Menu.animations[2]

            case "QUIT":
                self.state=SceneStates.QUIT_GAME
           
    def update(self, screen: pygame.Surface):
        super().update(screen)
        self.checkButtonPressed(self.buttonPressedName)
        self.checkUnpauseSignal()

