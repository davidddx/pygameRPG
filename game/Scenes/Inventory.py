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
from game.Item import ItemConstants

class Inventory(Menu):
    def __init__(self, last_area_frame: pygame.Surface, last_scene_frame: pygame.Surface):
        self.nonItemButtonNames = []
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
        self.buttonDescriptionSurfacePtr = None
        self.descriptionTextPos = [0, 0]
        self.lastFrameOpacity = self.opacity
        self.categoryButtonNames = self.initializeCategoryButtonNames(self.nonItemButtonNames) 
        self.subMenuPromptSurf = None
        self.descriptionOpacity = 255
    def initializeCategoryButtonNames(self, non_item_button_names):
        categoryButtonNames = []
        for name in non_item_button_names:
            if name == "EXIT":
                continue
            categoryButtonNames.append(name)
        return categoryButtonNames
            

    def generateSubMenuButtons(self, screen_size, pressed_button_category):
        logger.debug(f"{pressed_button_category=}")
        backButtonColor = 136, 8, 8
        backButtonOutline = 255, 0, 0 
        buttonColor = self.getCategoryButtonColor(pressed_button_category, outline=False)
        buttonOutlineColor = self.getCategoryButtonColor(pressed_button_category, outline=True)
        useButton = TextButton("USE", "USE", 0, 0, 0, 0, fit_to_text=True, color= buttonColor)
        discardButton = TextButton("DISCARD", "DISCARD", 0, 0, 0, 0, fit_to_text= True, color= buttonColor)
        backButton = TextButton("BACK", "BACK", 0, 0, 0, 0, fit_to_text= True, color = backButtonColor)
        buttons = [[useButton, discardButton, backButton]]

        yValue = 0 
        xValue= screen_size[0] / 2 
        for row in buttons:
            for button in row:
                button.setY(yValue)
                yValue += 2 * button.getHeight()
                button.setX(xValue - button.getWidth())
                if button.name != "BACK":
                    button.animateTextWithOutline(buttonOutlineColor)
                    continue
                button.animateTextWithOutline(backButtonOutline)

        yValue -= 2 * buttons[0][len(buttons[0]) - 1].getHeight()

        def setButtonsPos(buttons: list[list[TextButton]], starting_x, x_step, starting_y, y_step, rect_y_at_center= False, rect_x_at_center=False, screen_height=0, screen_width = 0):
            if rect_y_at_center: 
                subMenuHeight = 0
                rectWidth = 0
                sumButtonHeights = 0
                for column in buttons: 
                    for button in column: sumButtonHeights += button.getHeight() + y_step/2
                for column in buttons: 
                    for button in column:
                        subMenuHeight += button.getHeight() + y_step/2 
                        rectWidth = max(rectWidth, button.getWidth())
                    subMenuHeight -= y_step/2
                    starting_y = screen_height/2 - subMenuHeight/2
            for column in buttons:
                for button in column:
                    button.setY(starting_y)
                    button.setX(starting_x - button.getWidth()/2)
                    starting_y += y_step
                    starting_x += x_step

        setButtonsPos(buttons, starting_x = xValue , x_step = 0, starting_y = 0, rect_y_at_center = True, y_step = 2 * buttons[0][0].getHeight(), screen_height = screen_size[1])


        return buttons

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
            self.nonItemButtonNames.append(key)
            self.categoryIndices[key] = index
            button = TextButton(key, key, 0, 3 * SETTINGS.TILE_SIZE, 0, 0, fit_to_text = True, color = self.getCategoryButtonColor(key), font_path = SAVED_DATA.FONT_PATH)
            button.animateTextWithOutline(color= self.getCategoryButtonColor(key, True))
            categoryButtons.append(button)
            mainButtons.append([button])
            index += 1
        backButtonColor = 136, 8, 8
        backButtonColorOutline = (255, 0, 0)
        exitButton = TextButton("EXIT", "EXIT", 0, 3 * SETTINGS.TILE_SIZE, 0, 0, fit_to_text=True, color = backButtonColor, font_path = SAVED_DATA.FONT_PATH)
        self.nonItemButtonNames.append("EXIT")
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

    def checkButtonPressed(self, name, screen_size):
        if name == "NONE": return None

        if not self.onSubMenu:
            if name in self.categoryButtonNames: 
                self.buttonPressedName = "NONE"
                return None
            if name == "EXIT":
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
                return None

            # button pressed name must be an item name if edge cases not satisfied
            self.fadeOutUnselectedButtons(self.selectedButtonIdx)
            itemName = name.partition(' ')[2]
            self.subMenuPromptSurface = self.turnStringToFontSurf(itemName, SAVED_DATA.FONT_PATH)
            subMenuButtons = self.generateSubMenuButtons(screen_size, ItemConstants.getCategoryByName(itemName))
            self.focusOnSubMenu(subMenuButtons)
            self.descriptionOpacity = 100
            self.buttonPressedName = "NONE"
            return None

        # checking sub menu buttons

        if name == "BACK":
            self.focusOffSubMenu() 
            self.fadeAllButtons(resulting_opacity = 255)
            self.descriptionOpacity = 255
            self.buttonPressedName = "NONE"
            return None

        if name == "USE":
            itemName = self.mainButtons[self.selectedMainButtonIdx[0]][self.selectedMainButtonIdx[1]].getName().partition(' ')[2]  
            logger.debug(f"Using item {itemName=}. {self.inventory=}")
            self.addItemToInventory(inventory= self.inventory, item_name=itemName, step=-1)
            logger.debug(f"Used item {itemName=}. {self.inventory=}")
            self.buttonPressedName = "NONE"
            return None

        if name == "DISCARD":
            itemName = self.mainButtons[self.selectedMainButtonIdx[0]][self.selectedMainButtonIdx[1]].getName().partition(' ')[2]  
            logger.debug(f"Discarding item {itemName=}. {self.inventory=}")
            self.addItemToInventory(inventory= self.inventory, item_name=itemName, step=-1)
            logger.debug(f"Discarded item {itemName=}. {self.inventory=}")
            self.buttonPressedName = "NONE"

            return None

    def addItemToInventory(self, inventory: dict, step: int, item_id=None, item_name=None):

        def addItem(item_id, step):
            category_inventory = inventory[ItemConstants.getCategoryById(item_id)] 
            num = category_inventory[str(item_id)]
            if num + step < 0 or num + step > 99:
                return None
            category_inventory[str(item_id)] += step
            logger.debug(f"added {step=} to item with {item_id=}, {category_inventory=}")
        if item_id is None and item_name is None: return None

        if item_id is not None:
            if not ItemConstants.checkValidItemId(item_id):
                logger.error("Could not add item to inventory: item id invalid")

            if item_name is not None:
                if item_name != ItemConstants.getItemNameById(item_id):
                    return None
            addItem(item_id, step)
            return None

        if item_name is not None:
            if item_id is not None:
                if item_name != ItemConstants.getItemNameById(item_id):
                    return None
            item_id = ItemConstants.getItemIdByName(item_name)
            addItem(item_id, step)
            return None
            


    def updateCurrentButtonList(self, current_buttons: list[list[TextButton]], last_selected_button_idx: list[int], current_selected_button_idx: list[int]):
        if last_selected_button_idx == current_selected_button_idx:
            return None
        self.lastSelectedButtonIdx[1] = current_selected_button_idx[1] 
        if last_selected_button_idx[0] == current_selected_button_idx[0]:
            return None
        current_buttons[last_selected_button_idx[0]] = copy.deepcopy(self.originalMainButtons[last_selected_button_idx[0]])
        current_buttons[current_selected_button_idx[0]] = self.loadItemsByCategoryIndex(self.categoryIndices, current_selected_button_idx[0], current_buttons[current_selected_button_idx[0]], self.inventory)
        self.lastSelectedButtonIdx[0] = current_selected_button_idx[0]

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
                        button.animateTextWithOutline(color = (255, 255, 0))
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
        dummyScreen = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dummyScreen.set_alpha(self.lastFrameOpacity)
        self.blitSurfaceAndOutline(dummyScreen, self.heading, self.headingOutline, self.headingPosition)
        self.renderDescription(dummyScreen, self.selectedButtonIdx, self.lastSelectedButtonIdx, self.currentButtons) 
        screen.blit(dummyScreen, (0,0))
        self.lastFrameOpacity = self.opacity

    def getCurrentButtonDescription(self, selected_button_idx, last_selected_button_idx, current_buttons, screen_size):
        if selected_button_idx == last_selected_button_idx:
            if self.buttonDescriptionSurfacePtr is not None:
                self.buttonDescriptionSurfacePtr.set_alpha(self.descriptionOpacity)
                return self.buttonDescriptionSurfacePtr
        if self.onSubMenu:
            self.buttonDescriptionSurfacePtr.set_alpha(self.descriptionOpacity)
            return self.buttonDescriptionSurfacePtr
        currentButton =  current_buttons[selected_button_idx[0]][selected_button_idx[1]]
        buttonName = currentButton.getName()
        descriptionText = ""
        logger.debug(f"{buttonName=}")
        
        if buttonName in self.nonItemButtonNames:
            categoryDescription = ""
            match buttonName:
                case "EXIT":
                    categoryDescription = " Exit from Inventory Menu" 
                case "BOOSTS":
                    categoryDescription = " Boost stats"
                case "HEALING":
                    categoryDescription = " Increase character hp" 
                case _:
                    categoryDescription = " Unknown functionality..."
            descriptionText = buttonName + ":" + categoryDescription
        else:
            descriptionText = buttonName.partition(' ')[2] + ": " + ItemConstants.getDescriptionByName(buttonName.partition(' ')[2])
        logger.debug(f"{descriptionText=}")
        self.buttonDescriptionSurfacePtr = self.turnStringToFontSurf(descriptionText, SAVED_DATA.FONT_PATH, color = (255, 255, 255), base_size=28)

        self.buttonDescriptionSurfacePtr.set_alpha(self.descriptionOpacity)
        self.descriptionTextPos[0] = screen_size[0]/2 - self.buttonDescriptionSurfacePtr.get_width()/2
        return self.buttonDescriptionSurfacePtr

    def renderDescription(self, screen, selected_button_idx, last_selected_button_idx, current_buttons):
        if selected_button_idx != last_selected_button_idx:
            logger.debug(f"this is where i change description surf")
        headerColor = 220, 220, 220 
        headerOutlineColor = 220, 220, 220
        descriptionHeader = self.turnStringToFontSurf("DESCRIPTION", SAVED_DATA.FONT_PATH, 30, color=headerColor)
        descriptionHeaderOutline = self.turnStringToFontSurf("DESCRIPTION", SAVED_DATA.FONT_PATH, 30, color=headerOutlineColor)
        descriptionHeaderPos = (screen.get_width()/2 - descriptionHeader.get_width()/2,screen.get_height() - 5 * SETTINGS.TILE_SIZE)

        self.descriptionTextPos[1] = descriptionHeaderPos[1] + descriptionHeader.get_height() 
        descriptionHeader.set_alpha(self.descriptionOpacity)
        descriptionHeaderOutline.set_alpha(self.descriptionOpacity)
        self.blitSurfaceAndOutline(screen, descriptionHeader, descriptionHeaderOutline, descriptionHeaderPos)
        screen.blit(descriptionHeader, descriptionHeaderPos) 
        paddingSpace = 10
        description = self.getCurrentButtonDescription(selected_button_idx, last_selected_button_idx, current_buttons, screen.get_size())
        screen.blit(description, (self.descriptionTextPos[0], self.descriptionTextPos[1] + paddingSpace))

    def update(self, screen):
        logger.debug(f"{self.onSubMenu=}")
        super().update(screen)
        logger.debug(f"{self.currentButtons=}")
        logger.debug(f"{self.originalMainButtons}")
        self.updateCurrentButtonList(self.mainButtons, last_selected_button_idx=self.lastSelectedButtonIdx, current_selected_button_idx=self.selectedMainButtonIdx,)
        self.checkButtonPressed(self.buttonPressedName, screen.get_size())
    
