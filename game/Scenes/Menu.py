from game.Scenes.BaseScene import Scene, SceneStates
import pygame
import gamedata.Save.SavedData as SAVED_DATA
from game.utils.Button import TextButton
from game.Scenes.BaseScene import Scene, SceneStates

class Menu(Scene):
    selectionModes = ("NONE", "MOUSE", "KEYBOARD")
    animations = ("NONE", "FADE_IN", "FADE_OUT")
    noneAnimationId = 0
    fadeInAnimationId = 1
    fadeOutAnimationId = 2
    noneSelectionModeId = 0
    mouseSelectionModeId = 1
    keyboardSelectionModeId = 2

    def __init__(self, name: str, last_area_frame: pygame.Surface, main_buttons: list[TextButton], fade_in = True, opacity=0, last_scene_frame = None, other_buttons=None, selected_button_idx = -1, selection_mode = "NONE", on_main_buttons= True):
        super().__init__(name)
        self.state = SceneStates.INITIALIZING
        self.uiLock = True
        self.mainButtons = main_buttons
        self.otherButtons = other_buttons
        self.currentButtons = self.mainButtons
        self.selectedMainButtonIdx = -1
        self.selectedOtherButtonIdx = -1
        self.onSubMenu = False
        if on_main_buttons: 
            self.selectedMainButtonIdx = selected_button_idx
            self.selectedButtonIdx = selected_button_idx
        else: 
            self.selectedOtherButtonIdx = selected_button_idx
            self.selectedButtonIdx = self.selectedOtherButtonIdx
        self.lastSceneFrame = last_scene_frame
        self.selectedButtonIdx = self.selectedMainButtonIdx
        self.maxSelectedMainButtonIdx = len(main_buttons) - 1
        self.lastMousePosition = 0
        try:
            self.maxSelectedOtherButtonIdx = len(other_buttons) - 1
        except:
            self.maxSelectedOtherButtonIdx = 0
        self.maxSelectedCurrentButtonIdx = self.maxSelectedMainButtonIdx 
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
        self.surfacePositions = [] 
        self.timeLastUIKeystroke = 0
        if fade_in: self.state = SceneStates.ON_ANIMATION

    def enableMouse(self):
        for button in self.currentButtons: button.enableMouse()

    def disableMouse(self):
        for button in self.currentButtons: button.disableMouse()

    def setOtherButtons(self, other_buttons: list[TextButton]):
        self.otherButtons = other_buttons
        self.selectedOtherButtonIdx = 0
        self.maxSelectedOtherButtonIdx = len(other_buttons) - 1

    def setPositiveUiKeys(self, positive_ui_keys: list[int]):
        self.positiveUIKeys = positive_ui_keys

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
        for button in self.mainButtons:
            button.update(dummyScreen)
        if self.otherButtons is not None:
            for button in self.otherButtons:
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
        print(f"{self.buttonPressedName=}")
        print(f"{self.selectionMode=}")
        print(f"{self.selectedButtonIdx=}")
        print(f"{self.uiLock=}")
        print(f"{self.state=}")
        print(f"{type(self)=}")
        print(f"{self.opacity=}")
        self.updateSelectionMode(self.currentButtons, self.positiveUIKeys, self.negativeUIKeys)
        self.animateButtons(self.currentButtons)
        if self.animation != Menu.animations[Menu.noneAnimationId]:
            self.animate()
        self.render(screen)

    def animateButtons(self, current_buttons: list[TextButton]):
        keys = pygame.key.get_pressed()

        for index, button in enumerate(current_buttons):
            if index == self.selectedButtonIdx:
                button.animateTextToSize(size= 40, step= 3, shrink= False)
                button.animateTextToColor(color = (button.originalTextColor[0] - 20, button.originalTextColor[1] - 20, button.originalTextColor[2] - 20), speed = "medium")
                button.animateTextWithOutline()
                
                if keys[SAVED_DATA.PLAYER_SELECTION_KEY_ID] and not self.uiLock: 
                    if self.buttonPressedName == "NONE":
                        button.setPressed(True)
                        self.buttonPressedName = button.getName()
                if pygame.mouse.get_pressed()[0] and button.hover and not self.uiLock:
                    if self.buttonPressedName == "NONE":
                        button.setPressed(True)
                        self.buttonPressedName = button.getName()
                continue
            if button.fontSize != button.originalFontSize:

                button.animateTextToSize(size= button.originalFontSize, step= 10, shrink= True)
            if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
            if button.outlineColor != button.originalOutlineColor: button.animateTextWithOutline(color=button.originalOutlineColor)                

    def updateSelectionMode(self, current_buttons: list[TextButton], positive_ui_keys, negative_ui_keys):
        if self.uiLock: return None
        if self.state != SceneStates.RUNNING: return None
        hoveringOnButton = False
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        for key in positive_ui_keys:
            if keys[key]:
                self.selectionMode = "KEYBOARD"
        for key in negative_ui_keys:
            if keys[key]:
                self.selectionMode = "KEYBOARD"
        mousePos = pygame.mouse.get_pos()
        if self.lastMousePosition != mousePos:
            self.selectionMode = "MOUSE"
        self.lastMousePosition = mousePos
        if self.state == SceneStates.FINISHING:
            self.selectionMode = "NONE"
        for index, button in enumerate(current_buttons):
            if not button.hover:
                continue
            hoveringOnButton = True
            if self.selectionMode == "MOUSE":
                self.selectedButtonIdx = index
        if not hoveringOnButton:
            if self.selectionMode == "MOUSE":
                self.selectionMode = "NONE"
        if self.selectionMode == "KEYBOARD":
            selectStep = 0
            cooldown = 150
            if timenow - self.timeLastUIKeystroke >= cooldown:
                for positive_ui_key in positive_ui_keys:
                    if keys[positive_ui_key]:
                        selectStep = 1
                        self.timeLastUIKeystroke = timenow
                for negative_ui_key in negative_ui_keys:
                    if keys[negative_ui_key]:
                        selectStep = -1
                        self.timeLastUIKeystroke = timenow
                if self.selectedButtonIdx + selectStep < 0:
                    self.selectedButtonIdx = self.maxSelectedCurrentButtonIdx
                elif self.selectedButtonIdx + selectStep > self.maxSelectedCurrentButtonIdx:
                    self.selectedButtonIdx = 0
                else:
                    self.selectedButtonIdx += selectStep

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

    def fadeOutUnselectedButtons(self,selected_button_idx: int, resulting_opacity = 100):

        for index, button in enumerate(self.currentButtons):
            if index == selected_button_idx: continue
            button.setTextSurfaceAlpha(resulting_opacity)
            button.setTextSurfaceOutlineAlpha(resulting_opacity)
           
    def disableMouseForMainButtons(self):
        for button in self.mainButtons:
            button.disableMouse()

    def enableMouseForMainButtons(self):
        for button in self.mainButtons:
            button.enableMouse()

    def enableMouseForCurrentButtons(self):
        for button in self.currentButtons:
            button.enableMouse()

    def disableMouseForCurrentButtons(self):
        for button in self.currentButtons:
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
            self.selectedButtonIdx = self.selectedOtherButtonIdx
            self.maxSelectedCurrentButtonIdx = self.maxSelectedOtherButtonIdx
            self.onSubMenu = True

    def turnStringToFontSurf(self, string: str, font_fp: str, base_size=24, anti_aliasing= False, color = (0,0,0)):
        return pygame.font.Font(font_fp, base_size).render(string, anti_aliasing, color)

    def clear(self): pass


