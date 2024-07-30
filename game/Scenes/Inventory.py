from game.Scenes.BaseScene import Scene, SceneStates
from game.Scenes.Menu import Menu
from game.utils.Button import Button
import gamedata.Save.SavedData as SAVED_DATA
from debug.logger import logger
import pygame
from game.utils.Button import Button, TextButton
import os
import globalVars.SettingsConstants as SETTINGS
import importlib

class Inventory(Menu):
    def __init__(self, last_area_frame: pygame.Surface, last_scene_frame: pygame.Surface):
        self.inventory = self.loadInventoryData()
        self.state = SceneStates.INITIALIZING
        self.heading = self.loadFontSurf("INVENTORY", SETTINGS.TILE_SIZE, True, color = (8,100,10)) 

        self.headingFontPos = (SETTINGS.SCREEN_WIDTH/2 - self.heading.get_width()/2, 0)
        self.headingOutline = self.loadFontSurf("INVENTORY", SETTINGS.TILE_SIZE, True, color = (0, 200,0)) 
        self.inventory = self.loadInventoryData()
        mainButtons = self.generateMainButtons(inventory_data = self.inventory, screen_width = last_scene_frame.get_width())
        super().__init__(name= "INVENTORY", last_area_frame= last_area_frame, main_buttons = mainButtons, last_scene_frame = last_scene_frame) 
    

    @staticmethod
    def centerButtonsHorizontal(buttons: list[Button], screen_width):
        totalWidth = 0
        height = 0
        paddingSpaceWidth = 40
        for button in buttons:
            height = button.getHeight()
            totalWidth += button.getWidth() + paddingSpaceWidth

        totalWidth -= paddingSpaceWidth

        rect = pygame.Rect(screen_width/2 - totalWidth/2, 3* SETTINGS.TILE_SIZE, totalWidth, height)


        xValue = rect.left 
        paddingSpaceWidth = 40
        paddingSpaceHeight = 10
        prevCenter = 0
        for button in buttons:
            button.setX(xValue)
            prevCenter = button.rect.center
            button.setDimensions(width= button.getWidth() , height = button.getHeight() + paddingSpaceHeight)
            button.rect.center = prevCenter
            xValue += button.getWidth() + paddingSpaceWidth

    def generateMainButtons(self, inventory_data: dict, screen_width) -> list[list[Button]]:
        categoryButtons = []
        ## loading category buttons
        for key in inventory_data:
            categoryButtons.append(TextButton(key, key, 0, 3 * SETTINGS.TILE_SIZE, 0, 0, fit_to_text=True, color = (0,0,0), font_path = SAVED_DATA.FONT_PATH))
        ## centering category buttons
        Inventory.centerButtonsHorizontal(categoryButtons, screen_width)
        return [categoryButtons]


    def loadInventoryData(self) -> dict:
        inventoryModule = importlib.import_module("gamedata.playerdata.Inventory")

        return inventoryModule.loadInventory()

    def animateButtons(self, current_buttons: list[list[TextButton]]):
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        for indexColumn, column in enumerate(current_buttons):
                
            for indexRow, button in enumerate(column):
                if [indexColumn, indexRow] == self.selectedButtonIdx:
                    button.animateTextToColor(color = (button.originalTextColor[0] - 20, button.originalTextColor[1] - 20, button.originalTextColor[2] - 20), speed = "medium")
                    if self.onSubMenu:
                        button.animateTextWithOutline(color=(255, 255, 190))
                    else:
                        button.animateTextWithOutline()
                    for key in SAVED_DATA.PLAYER_SELECTION_KEYS:

                        if keys[key] and not self.uiLock: 
                            self.timeButtonLastPressed = timenow
                            button.setPressed(True)
                            self.buttonPressedName = button.getName()
                    if pygame.mouse.get_pressed()[0] and button.hover and not self.uiLock:
                        self.timeButtonLastPressed = timenow
                        button.setPressed(True)
                        self.buttonPressedName = button.getName()
                    continue
                if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
                if button.outlineColor != button.originalOutlineColor: button.animateTextWithOutline(color=button.originalOutlineColor)

    
    def update(self, screen):
        super().update(screen)

    
