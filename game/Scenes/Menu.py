from game.Scenes.BaseScene import Scene, SceneStates
import pygame
import gamedata.Save.SavedData as SAVED_DATA
from game.utils.Button import TextButton, Button
from game.Scenes.BaseScene import Scene, SceneStates
from debug.logger import logger

class Menu(Scene):
    selectionModes = ("NONE", "MOUSE", "KEYBOARD")
    animations = ("NONE", "FADE_IN", "FADE_OUT")
    noneAnimationId = 0
    fadeInAnimationId = 1
    fadeOutAnimationId = 2
    noneSelectionModeId = 0
    mouseSelectionModeId = 1
    keyboardSelectionModeId = 2
    def __init__(self, name: str, last_area_frame: pygame.Surface, main_buttons: list[list[Button]], fade_in = True, opacity=0, last_scene_frame = None, other_buttons=None, selected_button_idx = (0, 0), selection_mode = "NONE", on_main_buttons= True):

        super().__init__(name)
        self.timeInitialized = pygame.time.get_ticks()
        self.timeButtonLastPressed = 0
        self.state = SceneStates.INITIALIZING
        self.uiLock = True
        self.mainButtons = main_buttons
        self.otherButtons = other_buttons
        self.currentButtons = self.mainButtons
        self.selectedMainButtonIdx = [-1, -1] 
        self.selectedOtherButtonIdx = [-1, -1]
        self.onSubMenu = False
        if on_main_buttons: 
            self.selectedMainButtonIdx = [selected_button_idx[0], selected_button_idx[1]]
            self.selectedButtonIdx = [selected_button_idx[0], selected_button_idx[1]]
        else: 
            self.selectedOtherButtonIdx = [selected_button_idx[0], selected_button_idx[1]]
            self.selectedButtonIdx = [selected_button_idx[0], selected_button_idx[1]]
        self.lastSceneFrame = last_scene_frame
        self.selectedButtonIdx = self.selectedMainButtonIdx
        self.lastMousePosition = 0
        self.selectionMode = selection_mode
        self.buttonPressedName = "NONE"
        self.opacity = opacity
        self.disableMouse()
        if not fade_in: 
            self.opacity = 255
            self.state = SceneStates.RUNNING
            self.enableMouse()
            self.uiLock = False
        self.dummyScreen = pygame.Surface(last_area_frame.get_size(), pygame.SRCALPHA)
        self.dummyScreen.set_alpha(opacity)
        self.lastAreaFrame = last_area_frame
        self.background = Menu.loadBackground(last_area_frame.get_size(), 200)
        self.animation = Menu.initializeAnimation(fade_in)
        self.surfaces = []
        self.positiveUIKeys = [pygame.K_s, pygame.K_DOWN]
        self.negativeUIKeys = [pygame.K_w, pygame.K_UP]
        self.positiveUIKeysRow = [pygame.K_a, pygame.K_LEFT]
        self.negativeUIKeysRow = [pygame.K_d, pygame.K_RIGHT]
        self.surfacePositions = [] 
        self.timeLastUIKeystroke = 0
        if fade_in: self.state = SceneStates.ON_ANIMATION

    def getMaxIndex(self, my_list: list[list], index: int):
        return [len(my_list) - 1, len(my_list[index]) - 1]

    def enableMouse(self):
        for column in self.currentButtons: 
            for button in column: button.enableMouse()

    def disableMouse(self):
        for column in self.currentButtons: 
            for button in column: button.disableMouse()
            
    def setOtherButtons(self, other_buttons: list[list[Button]]):
        self.otherButtons = other_buttons
        self.selectedOtherButtonIdx = [0,0]
        
    def clearSurfaces(self): 
        self.surfaces.clear()
        self.surfacePositions.clear()

    def setPositiveUiKeys(self, positive_ui_keys: list[int]):
        self.positiveUIKeys = positive_ui_keys

    def setPositiveKeys(self, positive_list_jump_keys: list[int]):
        self.positiveButtonListJumpKeys = positive_list_jump_keys

    def setNegativeListJumpKeys(self, negative_list_jump_keys: list[int]):
        self.negativeButtonListJumpKeys = negative_list_jump_keys

    def setNegativeUIKeys(self, negative_ui_keys: list[int]):
        self.negativeUIKeys = negative_ui_keys

    def render(self, screen: pygame.Surface):
        screen.blit(self.lastAreaFrame, (0,0))
        if self.opacity != 255 and type(self.lastSceneFrame) == pygame.Surface:
            self.lastSceneFrame.set_alpha(255 - self.opacity)
            screen.blit(self.lastSceneFrame, (0,0))
        dummyScreen = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dummyScreen.set_alpha(self.opacity)
        dummyScreen.blit(self.background, (0,0))
        try:
            for index, surface in enumerate(self.surfaces):
                dummyScreen.blit(surface, self.surfacePositions[index])
        finally:
            pass
        for column in self.mainButtons:
            for button in column: button.update(dummyScreen)

        if self.otherButtons is not None:
            for column in self.otherButtons:
                for button in column:
                    button.update(dummyScreen)
        screen.blit(dummyScreen, (0,0))
    
    def addSurface(self, surface: pygame.Surface, position: tuple):
        self.surfaces.append(surface)
        self.surfacePositions.append(position)

    def animate(self, opacity_step = 10):
        match self.animation:
            case "NONE": 
                return None
            case "FADE_IN": 
                self.fadeScene(self.opacity, opacity_step)
                if self.opacity == 255: self.enableMouse()
                return None
            case "FADE_OUT": 
                self.fadeScene(self.opacity, -opacity_step)
                if self.opacity == 0 and self.state == SceneStates.FINISHING:
                    self.state = SceneStates.FINISHED
                return None

    def update(self, screen):
        self.updateSelectionMode(self.currentButtons, self.positiveUIKeys, self.negativeUIKeys,  self.positiveUIKeysRow, self.negativeUIKeysRow)
        self.checkUILock(self.timeButtonLastPressed)
        self.animateButtons(self.currentButtons)
        if self.animation != Menu.animations[Menu.noneAnimationId]:
            self.animate()
        self.render(screen)

    def checkUILock(self, time_button_last_pressed):
        timenow = pygame.time.get_ticks()
        buttonPressCooldown = 200
        if timenow -  time_button_last_pressed <= buttonPressCooldown:
            self.uiLock = True
            return None
        if timenow - self.timeInitialized<= buttonPressCooldown:
            self.uiLock = True
            return None
        self.uiLock = False

    def animateButtons(self, current_buttons: list[list[TextButton]]):
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        for indexColumn, column in enumerate(current_buttons):
                
            for indexRow, button in enumerate(column):
                if [indexColumn, indexRow] == self.selectedButtonIdx:
                    button.animateTextToSize(size= 40, step= 3, shrink= False)
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
                if button.fontSize != button.originalFontSize:
                    button.animateTextToSize(size= button.originalFontSize, step= 10, shrink= True)
                if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
                if button.outlineColor != button.originalOutlineColor: button.animateTextWithOutline(color=button.originalOutlineColor)

    def updateSelectionMode(self, current_buttons: list[list[Button]], positive_ui_keys, negative_ui_keys, row_positive_ui_keys, row_negative_ui_keys):
        if self.uiLock: return None
        if self.state != SceneStates.RUNNING: return None
        hoveringOnButton = False
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        for key in positive_ui_keys:
            if not keys[key]: continue
            self.selectionMode = "KEYBOARD"
        for key in negative_ui_keys:
            if not keys[key]: continue
            self.selectionMode = "KEYBOARD"
        for key in row_positive_ui_keys: 
            if not keys[key]: continue
            self.selectionMode = "KEYBOARD"
        for key in row_negative_ui_keys:
            if not keys[key]: continue
            self.selectionMode = "KEYBOARD"
        mousePos = pygame.mouse.get_pos()
        if self.lastMousePosition != mousePos:
            self.selectionMode = "MOUSE"
        self.lastMousePosition = mousePos
        if self.state == SceneStates.FINISHING:
            self.selectionMode = "NONE"
        for index1, column in enumerate(current_buttons):

            for index2, button in enumerate(column):
                if not button.hover:
                    continue
                hoveringOnButton = True
                if self.selectionMode == "MOUSE":
                    self.selectedButtonIdx = [index1, index2]
        if not hoveringOnButton:
            if self.selectionMode == "MOUSE":
                self.selectionMode = "NONE"
        if self.selectionMode == "KEYBOARD":
            selectStepX = selectStepY = 0
            cooldown = 150
            if timenow - self.timeLastUIKeystroke >= cooldown:
                for positive_ui_key in positive_ui_keys:
                    if keys[positive_ui_key]:
                        selectStepY = 1
                        self.timeLastUIKeystroke = timenow
                for negative_ui_key in negative_ui_keys:
                    if keys[negative_ui_key]:
                        selectStepY = -1
                        self.timeLastUIKeystroke = timenow
                for key in row_positive_ui_keys:
                    if keys[key]:
                        selectStepX = 1
                        self.timeLastUIKeystroke = timenow
                for key in row_negative_ui_keys:
                    if keys[key]:
                        selectStepX = -1
                        self.timeLastUIKeystroke = timenow
                logger.debug(f"{selectStepX=}, {selectStepY=}")
                prevIndices = [self.selectedButtonIdx[0], self.selectedButtonIdx[1]]
                logger.debug(f"{prevIndices=}")
                if self.selectedButtonIdx[0] + selectStepX < 0:
                    self.selectedButtonIdx[0] = len(current_buttons) - 1 
                elif self.selectedButtonIdx[0] + selectStepX > len(current_buttons) - 1:
                    self.selectedButtonIdx[0] = 0
                else:
                    self.selectedButtonIdx[0] += selectStepX
                
                if self.selectedButtonIdx[1] + selectStepY < 0:
                    self.selectedButtonIdx[1] = len(current_buttons[self.selectedButtonIdx[0]])-1
                elif self.selectedButtonIdx[1] + selectStepY > len(current_buttons[self.selectedButtonIdx[0]]) - 1:
                    self.selectedButtonIdx[1] = 0 
                else:
                    self.selectedButtonIdx[1] += selectStepY
                selectedButtonDestination = self.selectedButtonIdx

                logger.debug(f"{selectedButtonDestination=}")
                try:
                    current_buttons[self.selectedButtonIdx[0]][self.selectedButtonIdx[1]] 
                except:
                    self.selectedButtonIdx = prevIndices
                '''
                if self.selectedButtonIdx[0] + selectStepX < 0:
                    self.selectedButtonIdx[0] = len(current_buttons) - 1 
                elif self.selectedButtonIdx[0] + selectStepX > len(current_buttons) - 1:
                    self.selectedButtonIdx[0] = 0
                else:
                    self.selectedButtonIdx[0] += selectStepX
                
                if self.selectedButtonIdx[1] + selectStepY < 0:
                    self.selectedButtonIdx[1] = len(current_buttons[self.selectedButtonIdx[0]])-1
                elif self.selectedButtonIdx[1] + selectStepY > len(current_buttons[self.selectedButtonIdx[0]]) - 1:
                    self.selectedButtonIdx[1] = 0 
                else:
                    self.selectedButtonIdx[1] += selectStepY
                '''


    def fadeScene(self, opacity, opacityStep):
        opacity += opacityStep
        if opacityStep < 0:
            if opacity <= 0:
                self.opacity = 0
                self.animation = Menu.animations[Menu.noneAnimationId] 
                if self.state == SceneStates.FINISHING: self.state = SceneStates.FINISHED
                return None
        elif opacityStep > 0:
            if opacity >= 255:
                self.opacity = 255
                self.animation = Menu.animations[Menu.noneAnimationId]
                self.uiLock = False
                self.state = SceneStates.RUNNING
                self.enableMouseForCurrentButtons()
                return None
        else: return None
        self.opacity = opacity

    def fadeOutUnselectedButtons(self,selected_button_idx: list[list[int]], resulting_opacity = 100):
        for index1, column in enumerate(self.currentButtons):
            for index2, button in enumerate(column):
                if [index1, index2] == selected_button_idx: continue
                button.setTextSurfaceAlpha(resulting_opacity)
                button.setTextSurfaceOutlineAlpha(resulting_opacity)
               
    def fadeAllButtons(self, resulting_opacity = 255):
        for column in self.currentButtons:
            for button in column:
                button.setTextSurfaceAlpha(resulting_opacity)
                button.setTextSurfaceOutlineAlpha(resulting_opacity)
           
    def disableMouseForMainButtons(self):
        for column in self.mainButtons:
            for button in column:
                button.disableMouse()

    def enableMouseForMainButtons(self):
        for column in self.mainButtons:
            for button in column:
                button.enableMouse()

    def enableMouseForCurrentButtons(self):
        for column in self.currentButtons:
            for button in column:
                button.enableMouse()

    def disableMouseForCurrentButtons(self):
        for column in self.currentButtons:
            for button in column:
                button.disableMouse()

    @staticmethod
    def loadBackground(size: tuple, opacity: int):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((0,0,0))
        surf.set_alpha(opacity)
        return surf 

    @staticmethod
    def initializeAnimation(fade_in=False):
        if fade_in: return Menu.animations[Menu.fadeInAnimationId]
        return Menu.animations[Menu.noneAnimationId]

    def focusOnSubMenu(self, buttons: list):
        if not self.onSubMenu:
            self.setOtherButtons(buttons)
            self.currentButtons = self.otherButtons 
            self.selectedMainButtonIdx = self.selectedButtonIdx
            self.selectedButtonIdx = self.selectedOtherButtonIdx
            self.onSubMenu = True

    def focusOffSubMenu(self):
        if self.onSubMenu:
            self.otherButtons.clear()
            self.currentButtons = self.mainButtons
            self.selectedButtonIdx = self.selectedMainButtonIdx
            self.onSubMenu = False

    def getSelectedButton(self) -> Button:
        return self.currentButtons[self.selectedButtonIdx[0]][self.selectedButtonIdx[1]]

    def turnStringToFontSurf(self, string: str, font_fp: str, base_size=24, anti_aliasing= False, color = (0,0,0)):
        return pygame.font.Font(font_fp, base_size).render(string, anti_aliasing, color)

    def loadFontSurf(self, string: str, base_size=24, anti_aliasing=False, color=(0,0,0)):
        return self.turnStringToFontSurf(string, SAVED_DATA.FONT_PATH, base_size, anti_aliasing, color)

    def clear(self): pass


