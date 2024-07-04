from game.Scenes.BaseScene import Scene, SceneStates,SceneTypes
import pygame
import gamedata.Save.SavedData as SAVED_DATA
from game.Scenes.PauseMenu import PauseMenu
from game.utils.Button import TextButton

class PossibleSubMenus:
    NONE = "NONE"
    FONT = "FONT"
    SCREEN_SIZE = "SCREEN_SIZE"

class Settings(Scene):
    def __init__(self, pause_menu_last_frame: pygame.Surface, last_area_frame: pygame.Surface, screen_size: tuple):
        super().__init__(name = SceneTypes.SETTINGS)
        self.timeLastUIKeystroke = 0
        self.state = SceneStates.ON_ANIMATION
        self.onSubMenu = False
        self.animatingSceneIn = True
        self.buttonPressedName = "NONE"
        self.maxSelectedButtonIdx = 2
        self.selectedButtonIdx = -1
        self.pauseMenuLastFrame = pause_menu_last_frame
        self.lastAreaFrame = last_area_frame
        size = 48
        self.settingsSurface = Settings.loadFontSurface("SETTINGS", size, (20, 52, 164), True)
        self.settingsSurfaceOutline = Settings.loadFontSurface("SETTINGS", size, (0, 150, 255), True)
        self.settingsSurfacePosition = (screen_size[0] / 2 - self.settingsSurface.get_width()/2, 0)
        self.lastMousePosition = (0,0)
        self.animatingSceneOut = False
        self.blackBackground = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.blackBackground.fill((0,0,0,200))
        self.mainButtons = Settings.loadButtons(screen_size)
        self.subMenuButtons = []
        self.subMenuButtonPressed = "NONE"
        self.opacity = 0
        self.subMenu = "NONE"
        self.selectedSubMenuButtonIdx = 0
        self.timeLastSubMenu = 0

    def clear(self):
        pass

    @staticmethod
    def loadButtons(screen_size: tuple):
        settingsButtonColor = (20, 30, 200)
        settingsButtonColorOutline = (100, 130, 215)
        backToMenuButtonColor = 136, 8, 8
        backToMenuButtonColorOutline = (255, 0, 0)
        fontButton = TextButton("FONT", "FONT", x= 48, y = screen_size[1] /4, width = 3*48, height = 2*48, fit_to_text = True, color = settingsButtonColor)
        screenSizeButton = TextButton("SCREEN SIZE", "SCREEN_SIZE", x= 48, y = 2 * screen_size[1] / 4, width = 3*48, height = 2*48, fit_to_text = True, color = settingsButtonColor)
        screenSizeButton.animateTextWithOutline(settingsButtonColorOutline)
        fontButton.animateTextWithOutline(settingsButtonColorOutline)
        backToMenuButton = TextButton("BACK TO MENU", "BACK_TO_MENU", x= 48, y= 3 * screen_size[1]/4, width= 3 * 48, height = 2 * 48, fit_to_text = True, color=backToMenuButtonColor)

        backToMenuButton.animateTextWithOutline(backToMenuButtonColorOutline)
        return [fontButton, screenSizeButton, backToMenuButton]

    
    def loadFontButtons(self, screen_size: tuple):
        buttonColor = (20, 30, 200)
        buttonColorOutline = (100, 130, 215)
        buttonxOffset = self.mainButtons[0].rect.width + self.mainButtons[0].getRect().width/4
        font1Button = TextButton("FONT1", "FONT1", x= 48 + buttonxOffset, y = screen_size[1] / 4,width = 3*48, height = 2*48, fit_to_text = True, color = buttonColor)
        font1Button.setFont("GOHU")
        font1Button.updateTextSurface()
        buttonxOffset += font1Button.rect.width + font1Button.rect.width/4
        font2Button = TextButton("FONT2", "FONT2", x= 48 + buttonxOffset, y = screen_size[1] / 4,width = 3*48, height = 2*48, fit_to_text = True, color = buttonColor)
        font2Button.setFont("FIRA_CODE")
        font2Button.updateTextSurface()
        buttonxOffset += font2Button.rect.width + font2Button.rect.width/4
        font3Button = TextButton("FONT3", "FONT3", x= 48 + buttonxOffset, y = screen_size[1] / 4,width = 3*48, height = 2*48, fit_to_text = True, color = buttonColor)
        font3Button.setFont("MONOFUR")
        font3Button.updateTextSurface()
        buttonxOffset += font3Button.rect.width + font3Button.rect.width/4
        font4Button = TextButton("FONT4", "FONT4", x= 48 + buttonxOffset, y = screen_size[1] / 4,width = 3*48, height = 2*48, fit_to_text = True, color = buttonColor)
        font4Button.setFont("AGAVE")
        font4Button.updateTextSurface()
        buttonxOffset += font4Button.rect.width + font4Button.rect.width/4
        font5Button = TextButton("FONT5", "FONT5", x= 48 + buttonxOffset, y = screen_size[1] / 4,width = 3*48, height = 2*48, fit_to_text = True, color = buttonColor)
        font5Button.setFont("CASKAYDIA")
        font5Button.updateTextSurface()
        buttonxOffset += font5Button.rect.width + font5Button.rect.width/4
        font6Button = TextButton("FONT6", "FONT6", x= 48 + buttonxOffset, y = screen_size[1] / 4,width = 3*48, height = 2*48, fit_to_text = True, color = buttonColor)
        font6Button.setFont("ANONYMICE_PRO")
        font6Button.updateTextSurface()

        return [font1Button, font2Button, font3Button, font4Button, font5Button, font6Button]
    @staticmethod
    def loadScreenSizeButtons(screen_size: tuple):
        pass

    def renderSubMenu(self, screen: pygame.Surface):
        buttons = self.subMenuButtons
        for i in range(len(buttons)):
            if i != self.selectedButtonIdx:
                buttons[i].setSelected(False)
                continue
            buttons[i].setSelected(True)
        for button in buttons:
            if button.selected:
                button.animateTextToSize(size= 40, step= 3, shrink= False)
                button.animateTextToColor(color = (button.originalTextColor[0] - 20, button.originalTextColor[1] - 20, button.originalTextColor[2] - 20), speed = "medium")
                button.animateTextWithOutline()
                if keys[SAVED_DATA.PLAYER_SELECTION_KEY_ID]: 
                    button.togglePressed()

                    self.buttonPressedName = button.getName()
            else:
                if button.fontSize != button.originalFontSize:

                    button.animateTextToSize(size= button.originalFontSize, step= 10, shrink= True)
                if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
                if button.outlineColor != button.originalOutlineColor: button.animateTextWithOutline(color=button.originalOutlineColor)                
        for button in buttons: button.update(screen)

    @staticmethod
    def disableMouseForButtons(buttons: list[TextButton]):
        for button in buttons:
            button.disableMouse()

    @staticmethod
    def enableMouseForButtons(buttons: list[TextButton]):
        for button in buttons:
            button.enableMouse()



    def update(self, screen: pygame.Surface):
        self.render(screen)
        self.checkSceneState()
        self.checkButtonPressed(self.buttonPressedName, screen.get_size())

    def render(self, screen):
        screen.blit(self.lastAreaFrame, (0,0))
        screen.blit(self.blackBackground, (0,0))
        if self.state == SceneStates.ON_ANIMATION: 
            dummyScreen = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            self.animate(screen, dummyScreen)
            dummyScreen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0] + 2, self.settingsSurfacePosition[1]))
            dummyScreen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0] - 2, self.settingsSurfacePosition[1]))
            dummyScreen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0], self.settingsSurfacePosition[1] + 2))
            dummyScreen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0], self.settingsSurfacePosition[1] - 2))
            dummyScreen.blit(self.settingsSurface, self.settingsSurfacePosition)
            self.renderButtons(self.mainButtons, dummyScreen) 
            screen.blit(dummyScreen, (0,0))
            return None

        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0]-2, self.settingsSurfacePosition[1]))
        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0]+2, self.settingsSurfacePosition[1]))
        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0], self.settingsSurfacePosition[1]-2))
        screen.blit(self.settingsSurfaceOutline, (self.settingsSurfacePosition[0], self.settingsSurfacePosition[1]+ 2))
        screen.blit(self.settingsSurface, self.settingsSurfacePosition)
        self.renderButtons(self.mainButtons, screen)

    def renderButtons(self, buttons, screen):
        hoveringOnButton = False
        keys = pygame.key.get_pressed()
        timenow = pygame.time.get_ticks()
        if keys[SAVED_DATA.UI_MOVE_UP] or keys[SAVED_DATA.UI_MOVE_DOWN] or keys[SAVED_DATA.UI_MOVE_LEFT] or keys[SAVED_DATA.UI_MOVE_RIGHT]:
            self.selectionMode = "KEYBOARD"
        mousePos = pygame.mouse.get_pos()
        if self.lastMousePosition != mousePos:
            self.lastMousePosition = mousePos
            self.selectionMode = "MOUSE"
        if self.state == SceneStates.FINISHING:
            self.selectionMode = "NONE"

        for index, button in enumerate(buttons):
            if not button.hover:
                continue
            hoveringOnButton = True
            self.selectedButtonIdx = index
        if not hoveringOnButton and self.selectionMode == "MOUSE": self.selectionMode = "NONE"
        if self.subMenu == "NONE":
            if self.selectionMode == "KEYBOARD":
                selectStep = 0
                cooldown = 150
                if timenow - self.timeLastUIKeystroke >= cooldown:
                
                    if keys[SAVED_DATA.UI_MOVE_UP]:
                        selectStep = -1
                        self.timeLastUIKeystroke = timenow        
                    elif keys[SAVED_DATA.UI_MOVE_DOWN]:
                        selectStep = 1 
                        self.timeLastUIKeystroke = timenow        
                    elif keys[SAVED_DATA.UI_MOVE_RIGHT]:
                        selectStep = 1
                        self.timeLastUIKeystroke = timenow        
                    elif keys[SAVED_DATA.UI_MOVE_LEFT]:
                        selectStep = -1
                        self.timeLastUIKeystroke = timenow        
                    if self.selectedButtonIdx + selectStep < 0:
                        self.selectedButtonIdx = self.maxSelectedButtonIdx
                    elif self.selectedButtonIdx + selectStep > self.maxSelectedButtonIdx:
                        self.selectedButtonIdx = 0
                    else:
                        self.selectedButtonIdx += selectStep


        for i in range(len(buttons)):
            if i != self.selectedButtonIdx:
                buttons[i].setSelected(False)
                continue
            buttons[i].setSelected(True)
        for button in buttons:
            if button.selected:
                button.animateTextToSize(size= 40, step= 3, shrink= False)
                button.animateTextToColor(color = (button.originalTextColor[0] - 20, button.originalTextColor[1] - 20, button.originalTextColor[2] - 20), speed = "medium")
                button.animateTextWithOutline()
                if keys[SAVED_DATA.PLAYER_SELECTION_KEY_ID]: 
                    button.togglePressed()

                    self.buttonPressedName = button.getName()
            else:
                if button.fontSize != button.originalFontSize:

                    button.animateTextToSize(size= button.originalFontSize, step= 10, shrink= True)
                if button.textColor != button.originalTextColor: button.animateTextToColor(color = button.originalTextColor, speed = "medium")
                if button.outlineColor != button.originalOutlineColor: button.animateTextWithOutline(color=button.originalOutlineColor)                
            if button.pressed:
                self.renderSubMenu(screen)
            button.update(screen)
            if self.buttonPressedName == "NONE" and button.getPressed(): self.buttonPressedName = button.getName()
        
        mousePressed = pygame.mouse.get_pressed()
        if not hoveringOnButton and (mousePressed[0] or mousePressed[1] or mousePressed[2]):
            self.selectedButtonIdx = -1 

    @staticmethod
    def loadFontSurface(string: str, size=24, color= (255,255,255), anti_aliasing= False):
        return Settings.turnStringToFontSurf(string, SAVED_DATA.FONT_PATH,size, color, anti_aliasing)

    @staticmethod
    def turnStringToFontSurf(string: str, font_fp: str, base_size=24,  color= (255,255,255), anti_aliasing = False):        
        return pygame.font.Font(font_fp, base_size).render(string, anti_aliasing, color)

    def animate(self, screen, dummy_screen):
        if self.animatingSceneIn:
            self.animateSceneIn(screen, dummy_screen, self.pauseMenuLastFrame)
        if self.animatingSceneOut:
            self.animateSceneOut(screen, dummy_screen, self.pauseMenuLastFrame)

    def animateSceneIn(self, screen:pygame.Surface, dummy_screen: pygame.Surface, pause_menu_last_frame: pygame.Surface):
        opacityStep = 5
        self.opacity += opacityStep
        if self.opacity >= 255:
            pause_menu_last_frame.set_alpha(0)
            dummy_screen.set_alpha(255)
            screen.blit(self.pauseMenuLastFrame, (0,0))
            self.animatingSceneIn = False
            self.state = SceneStates.RUNNING
            return None
        pause_menu_last_frame.set_alpha(255 - self.opacity)
        screen.blit(pause_menu_last_frame, (0,0))
        dummy_screen.set_alpha(self.opacity)

    def animateSceneOut(self, screen: pygame.Surface, dummy_screen: pygame.Surface, pause_menu_last_frame: pygame.Surface):
        opacityStep = 5
        self.opacity -= opacityStep
        if self.opacity <= 0:
            pause_menu_last_frame.set_alpha(255)
            dummy_screen.set_alpha(0)
            screen.blit(self.pauseMenuLastFrame, (0,0))
            self.animatingSceneIn = False
            self.state = SceneStates.FINISHED
            return None
        pause_menu_last_frame.set_alpha(255 - self.opacity)
        screen.blit(pause_menu_last_frame, (0,0))
        dummy_screen.set_alpha(self.opacity)

    def checkButtonPressed(self, name: str, screen_size: tuple):
        if self.state != SceneStates.RUNNING: return None
        print(f"{name=}")
        if self.onSubMenu: return None
        match name:
            case "NONE": return None
            case "BACK_TO_MENU": 
                self.state = SceneStates.ON_ANIMATION
                self.animatingSceneOut = True
                self.ptrNextScene = SceneTypes.PAUSE_MENU 

            case "FONT":
                self.subMenu = PossibleSubMenus.FONT
                Settings.disableMouseForButtons(self.mainButtons)
                if self.subMenuButtons == []:
                    self.subMenuButtons = self.loadFontButtons(screen_size)
            case "SCREEN_SIZE": 
                self.subMenu = PossibleSubMenus.SCREEN_SIZE
                Settings.disableMouseForButtons(self.mainButtons)


    def checkSceneState(self):
        if self.state != SceneStates.RUNNING: return None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.state = SceneStates.ON_ANIMATION
            self.animatingSceneOut = True
            self.ptrNextScene = SceneTypes.PAUSE_MENU 
