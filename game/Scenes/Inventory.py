from game.Scenes.BaseScene import Scene, SceneStates, SceneTypes
from game.Scenes.Menu import Menu
from game.utils.Button import Button
import gamedata.Save.SavedData as SAVED_DATA
from debug.logger import logger
import pygame
from game.utils.Button import Button, TextButton
import os
import game.Item as ITEM
import globalVars.SettingsConstants as SETTINGS
import importlib
from bidict import bidict
import copy

class MenuSurface:
    def __init__(self, surface: pygame.Surface, position: tuple):
        self.rect = surface.get_rect(topleft=position)
        self.surf = surface
    def blitToScreen(self, screen: pygame.Surface):
        screen.blit(self.surf, (self.rect.x, self.rect.y))


class Inventory(Menu):
    def __init__(self, last_area_frame: pygame.Surface, last_scene_frame: pygame.Surface):
        self.name = SceneTypes.INVENTORY
        self.inventory = self.loadInventoryData()
        self.state = SceneStates.INITIALIZING
        self.heading = self.loadFontSurf("INVENTORY", SETTINGS.TILE_SIZE, True, color = (8,100,10)) 
        self.headingPosition = (SETTINGS.SCREEN_WIDTH/2 - self.heading.get_width()/2, 0)
        self.headingOutline = self.loadFontSurf("INVENTORY", SETTINGS.TILE_SIZE, True, color = (0, 200,0)) 
        self.categoryIndices = bidict() 
        self.originalMainButtons = self.generateMainButtons(inventory_data = self.inventory, screen_width = last_scene_frame.get_width())
        mainButtons = copy.deepcopy(self.originalMainButtons)
        super().__init__(name= "INVENTORY", last_area_frame= last_area_frame, main_buttons = mainButtons, last_scene_frame = last_scene_frame) 
        self.lastSelectedButtonIdx = [-1, -1]

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
        mainButtons = []
        categoryButtons = []
        ## loading category buttons
        index = 0
        for key in inventory_data:
            self.categoryIndices[key] = index
            button = TextButton(key, key, 0, 3 * SETTINGS.TILE_SIZE, 0, 0, fit_to_text = True, color = self.getCategoryButtonColor(key), font_path = SAVED_DATA.FONT_PATH)
            button.animateTextWithOutline(color= self.getCategoryButtonColor(key, True))
            categoryButtons.append(button)
            mainButtons.append([button])
            index += 1
        backButtonColor = 136, 8, 8
        backButtonColorOutline = (255, 0, 0)
        exitButton = TextButton("EXIT", "EXIT", 0, 3 * SETTINGS.TILE_SIZE, 0, 0, fit_to_text=True, color = backButtonColor, font_path = SAVED_DATA.FONT_PATH)
        exitButton.animateTextWithOutline(color=backButtonColorOutline)
        mainButtons.append([exitButton])
        categoryButtons.append(exitButton)
        self.categoryIndices["EXIT"] = index
        ## centering category buttons
        Inventory.centerButtonsHorizontal(categoryButtons, screen_width)
        return mainButtons

    def initializeSelectedButton(self, button: TextButton):
        button.animateTextWithOutline(color = (255, 255, 0))
        button.animateTextToColor(color = (button.originalTextColor[0] - 20, button.originalTextColor[1] - 20, button.originalTextColor[2] - 20), speed = "medium")

    def checkButtonPressed(self, name):
        if name == "NONE": return None
        match name:
            case "EXIT":
                for col in self.mainButtons: 
                    for button in col: 
                        button.setSelected(False)
                        button.setPressed(False)
                        button.disableMouse()
                self.uiLock = True
                self.state = SceneStates.FINISHING
                self.ptrNextScene = SceneTypes.PAUSE_MENU
                self.animation = Menu.animations[2]
                self.buttonPressedName = "NONE"

    def updateCurrentButtonList(self, current_buttons: list[list[TextButton]], last_selected_button_idx: list[int], current_selected_button_idx: list[int]):
        if last_selected_button_idx[0] == current_selected_button_idx[0]:
            return None
        current_buttons[last_selected_button_idx[0]] = copy.deepcopy(self.originalMainButtons[last_selected_button_idx[0]])
        current_buttons[current_selected_button_idx[0]] = self.loadItemsByCategoryIndex(self.categoryIndices, current_selected_button_idx[0], current_buttons[current_selected_button_idx[0]], self.inventory)
        self.lastSelectedButtonIdx = current_selected_button_idx[:] 
    def loadItemsByCategoryIndex(self, category_indices: bidict, current_index: int, category_list: list[TextButton], inventory: dict):
        ##categoryDict format: {Item1: Count1, Item2: Count2, ..., ItemN: CountN}
        category = category_indices.inverse[current_index]
        if category == "EXIT":
            return category_list 
        categoryDict = inventory[category]
        categoryButton = category_list[0]
        outlineColor = categoryButton.originalOutlineColor
        textColor = categoryButton.originalTextColor
        buttonX = categoryButton.rect.x
        paddingSpace = 3
        currentY = categoryButton.rect.y + categoryButton.getHeight() + paddingSpace
        for key in categoryDict:
            item = ITEM.ItemConstants.getItemNameById(int(key))
            itemCount = categoryDict[key]
            itemSurf = f"({itemCount}) {item}"
            button = TextButton(itemSurf, itemSurf, x=buttonX, y=currentY, width=0, height=0, fit_to_text=True, color = textColor, font_path = SAVED_DATA.FONT_PATH)
            button.animateTextWithOutline(outlineColor)
            category_list.append(button)
            currentY += currentY + button.getHeight() + paddingSpace
        return category_list


    def checkButtonSelected(self, current_buttons: list[list[TextButton]], selected_button_idx: list[int]):

        name = current_buttons[selected_button_idx[0]][selected_button_idx[1]]
        match name:
            case "BOOSTS":
                pass
            case "HEALING":
                pass

    def getCategoryButtonColor(self, category_name: str, outline= False) -> tuple:
        baseColor = (0, 0, 0)
        outlineColor = (0, 0, 0)
        match category_name:
            case "BOOSTS":
                baseColor = (242, 140, 40)
                outlineColor = (204, 85, 0)
            case "HEALING":
                baseColor = (218, 112, 214)
                outlineColor = (255, 182, 193)

        if outline: return outlineColor
        return baseColor

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

    def render(self, screen):
        super().render(screen)
        self.blitSurfaceAndOutline(screen, self.heading, self.headingOutline, self.headingPosition)
    
    def update(self, screen):
        super().update(screen)
        logger.debug(f"{self.currentButtons=}")
        logger.debug(f"{self.originalMainButtons}")
        self.updateCurrentButtonList(self.mainButtons, last_selected_button_idx=self.lastSelectedButtonIdx, current_selected_button_idx=self.selectedButtonIdx,)
        self.checkButtonPressed(self.buttonPressedName)

    
