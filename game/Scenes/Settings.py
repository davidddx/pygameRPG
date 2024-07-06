from game.Scenes.BaseScene import Scene, SceneStates,SceneTypes
import pygame
import gamedata.Save.SavedData as SAVED_DATA
import globalVars.SettingsConstants as SETTINGS
#from game.Scenes.PauseMenu import PauseMenu
from game.utils.Button import TextButton
from game.Scenes.Menu import Menu

class PossibleSubMenus:
    NONE = "NONE"
    FONT = "FONT"
    SCREEN_SIZE = "SCREEN_SIZE"


class Settings(Menu):
    def __init__(self, pause_menu_last_frame: pygame.Surface, last_area_frame: pygame.Surface, screen_size: tuple):
        self.screenSizeButtonId = 0
        self.fontButtonId = 0
        self.backToMenuButtonId = 0
        super().__init__(name= SceneTypes.SETTINGS,last_area_frame = last_area_frame, last_scene_frame= pause_menu_last_frame, main_buttons = self.generateMainButtons(screen_size))
        self.settingsFontOutline = self.turnStringToFontSurf(string= "SETTINGS", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing= True, color= (0, 150, 255))
        self.settingsFont = self.turnStringToFontSurf(string = "SETTINGS", font_fp = SAVED_DATA.FONT_PATH, base_size = SETTINGS.TILE_SIZE, anti_aliasing = True, color= (20, 52, 164)) 
        #self.settingsFontPos = (SETTINGS.SCREEN_WIDTH/2 - self.pausedFont.get_width() / 2, 0)
        fontPos = (SETTINGS.SCREEN_WIDTH/2 - self.settingsFont.get_width()/2, 0)
        self.addSurface(self.settingsFontOutline, (fontPos[0], fontPos[1] + 2))
        self.addSurface(self.settingsFontOutline, (fontPos[0] - 2, fontPos[1]))
        self.addSurface(self.settingsFontOutline, (fontPos[0] + 2, fontPos[1]))
        self.addSurface(self.settingsFontOutline, (fontPos[0], fontPos[1] - 2))
        self.addSurface(self.settingsFont, fontPos)
        self.testRect = None

    def update(self, screen: pygame.Surface):
        super().update(screen)
        self.checkButtonPressed(self.buttonPressedName, screen)
        self.checkExitSignal() 

    def checkExitSignal(self):
        if self.uiLock: return None
        if self.state != SceneStates.RUNNING: return None 
        exitKey = pygame.K_f
        keys = pygame.key.get_pressed()
        if keys[exitKey]:
            for button in self.mainButtons: 
                button.setSelected(False)
                button.setPressed(False)
                button.disableMouse()
            self.uiLock = True
            self.state = SceneStates.FINISHING
            self.ptrNextScene = SceneTypes.PAUSE_MENU
            self.animation = Menu.animations[2]


    def checkButtonPressed(self, name: str, screen: pygame.Surface):
        if name == "NONE": return None
        match name:
            case "BACK_TO_MENU":
                for button in self.mainButtons: 
                    button.setSelected(False)
                    button.setPressed(False)
                    button.disableMouse()
                self.uiLock = True
                self.state = SceneStates.FINISHING
                self.ptrNextScene = SceneTypes.PAUSE_MENU
                self.animation = Menu.animations[2]
                self.buttonPressedName = "NONE"
            case "FONT":
                self.fadeOutUnselectedButtons(self.selectedButtonIdx)
                self.focusOnSubMenu(Settings.generateSubButtons(parent_button = self.mainButtons[self.fontButtonId], screen_size= screen.get_size()))
                self.buttonPressedName = "NONE"
            case "SCREEN_SIZE":
                self.fadeOutUnselectedButtons(self.selectedButtonIdx)
                self.focusOnSubMenu(Settings.generateSubButtons(parent_button = self.mainButtons[self.screenSizeButtonId], screen_size= screen.get_size()))

                self.buttonPressedName = "NONE"
    @staticmethod
    def generateSubButtons(parent_button: TextButton, screen_size: tuple) -> list:
        name = parent_button.getName()
        #rect = top_button.getRect()
        yValue = 0 
        xValue= screen_size[0] / 2 
        subButtonColor = (100, 149, 207)
        subButtonOutlineColor = (240, 255, 255)
        backButtonColor = (215, 43, 23)


        def setButtonsPos(buttons: list[TextButton], starting_x, x_step, starting_y, y_step, rect_y_at_center= False, rect_x_at_center=False, screen_height=0, screen_width = 0):
            if rect_y_at_center: 
                subMenuHeight = 0
                rectWidth = 0
                sumButtonHeights = 0
                for button in buttons: sumButtonHeights += button.getHeight() + y_step/2
                for button in buttons: 
                    subMenuHeight += button.getHeight() + y_step/2 
                    rectWidth = max(rectWidth, button.getWidth())
                subMenuHeight -= y_step/2
                starting_y = screen_height/2 - subMenuHeight/2
            for button in buttons:
                button.setY(starting_y)
                button.setX(starting_x - button.getWidth()/2)
                starting_y += y_step
                starting_x += x_step
        def setButtonsOutline(buttons: list[TextButton], color: tuple[int,int,int], name):
            for button in buttons: 
                if button.getName() != name + ".BACK": 
                    button.animateTextWithOutline(color= color)

                    continue
                button.animateTextWithOutline(color = (250, 128, 114))
        match name:
            case "SCREEN_SIZE":
                smallButton = TextButton("SMALL", name + ".SMALL", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor)
                mediumButton = TextButton("MEDIUM", name + ".MEDIUM", xValue, yValue, 0, 0, fit_to_text = True, color = subButtonColor)
                largeButton = TextButton("LARGE", name + ".LARGE", xValue, yValue, 0, 0, fit_to_text = True, color = subButtonColor)
                fullscreenButton = TextButton("FULLSCREEN", name + ".FULLSCREEN", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor)
                backButton = TextButton("BACK", name + ".BACK", xValue, yValue, 0, 0, fit_to_text=True, color= backButtonColor)
                buttons = [smallButton, mediumButton, largeButton, fullscreenButton, backButton]
                setButtonsPos(buttons, starting_x = xValue , x_step = 0, starting_y = 0, rect_y_at_center = True, y_step = 2 * buttons[0].getHeight(), screen_height = screen_size[1])
                setButtonsOutline(buttons, subButtonOutlineColor, name)

                return buttons 
            case "FONT":
                font1Button = TextButton("FONT 1", name + ".1", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor)
                font1Button.setX(xValue - font1Button.getWidth()/2)
                yValue += 2 * font1Button.getHeight()
                font2Button = TextButton("FONT 2", name + ".2", xValue, yValue, 0, 0, fit_to_text = True, color=subButtonColor)
                font2Button.setX(xValue - font2Button.getWidth()/2)
                yValue += 2 * font2Button.getHeight()
                font3Button = TextButton("FONT 3", name + ".3", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor)
                font3Button.setX(xValue - font3Button.getWidth()/2)
                yValue += 2 * font3Button.getHeight()
                font4Button = TextButton("FONT 4", name + ".4", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor)
                font4Button.setX(xValue - font4Button.getWidth()/2)
                yValue += 2 * font4Button.getHeight()
                font5Button = TextButton("FONT 5", name + ".5", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor)
                font5Button.setX(xValue - font5Button.getWidth()/2)
                yValue += 2 * font5Button.getHeight()
                font6Button = TextButton("FONT 6", name + ".6", xValue, yValue, 0, 0, fit_to_text = True, color= subButtonColor)
                font6Button.setX(xValue - font6Button.getWidth()/2)
                buttons = [font1Button, font2Button, font3Button, font4Button, font5Button, font6Button]
                setButtonsPos(buttons, starting_x = xValue , x_step = 0, starting_y = 0, rect_y_at_center = True, y_step = 2 * buttons[0].getHeight(), screen_height = screen_size[1])
                setButtonsOutline(buttons, subButtonOutlineColor, name)

                return buttons 
            case _: return []

    def generateMainButtons(self, screen_size: tuple):
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
        self.fontButtonId = 0
        self.screenSizeButtonId = 1
        self.backToMenuButtonId = 2
        return [fontButton, screenSizeButton, backToMenuButton]



'''
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
'''
